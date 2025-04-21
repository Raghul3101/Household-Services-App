from flask import render_template,render_template_string, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
import jwt
from flask_cors import cross_origin, CORS
from flask_restful import Api, Resource
from backend import app, db
from backend.models.models import Customer, Professional, Service, Request
from sqlalchemy import case
from sqlalchemy.sql import func
from datetime import datetime, date, timedelta
import json

api = Api(app)

# --------------------------------Login and Register-----------------------------------------

@app.route('/api/user-details', methods=['GET'])
@jwt_required()
def get_user_details():
    user = get_jwt_identity()
    return jsonify(user), 200

@app.route('/login', methods=['POST'])
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if user is a Customer
    customer = Customer.query.filter_by(email=email).first()
    if customer and customer.password == password:
        access_token = create_access_token(identity=json.dumps({
            "email": customer.email,
            "role": "customer",
            "id": customer.id
        }))
        return jsonify({
            "message": "Login successful",
            "user_type": "customer",
            "id": customer.id,
            "access_token": access_token
        }), 200

    # Check if user is a Service Professional
    professional = Professional.query.filter_by(email=email).first()
    if professional and professional.password == password:
        access_token = create_access_token(identity=json.dumps({
            "email": professional.email,
            "role": "professional",
            "id": professional.id
        }))
        return jsonify({
            "message": "Login successful",
            "user_type": "professional",
            "id": professional.id,
            "status": professional.flag,
            "access_token": access_token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/api/register-customer', methods=['GET','POST'])
def register_customer():
    try:
        data = request.json  # Get JSON data from the request
        fname = data.get('fname')
        lname = data.get('lname')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        address = data.get('address')
        pincode = data.get('pincode')   
        print('Yes')
        if not fname or not email or not password or not phone or not address:
            return jsonify({"message": "Missing required fields"}), 400

        new_customer = Customer(fname=fname, lname=lname, email=email, password=password, phone=phone, address=address, pincode=pincode)
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        print(f"Error: {str(e)}")  
        return jsonify({"message": "Error registering user", "error": str(e)}), 500

@app.route('/api/register-professional', methods=['POST'])
def register_professional():
    data = request.json

    fname = data.get('fname')
    lname = data.get('lname')
    email = data.get('email')
    password = data.get('password')
    service = data.get('service')
    phone = data.get('phone')
    experience = data.get('experience')
    address = data.get('address')
    pincode = data.get('pincode')

    new_professional = Professional(
        fname=fname, lname=lname, email=email, password=password, 
        service=service, phone=phone, experience=experience, 
        address=address, pincode=pincode
    )

    db.session.add(new_professional)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@app.route('/api/get-categories', methods=['GET'])
def get_categories():
    categories = list(set([service.category.title() for service in Service.query.distinct(Service.category)]))
    print(categories)
    return jsonify({'categories': categories})

@app.route('/api/get-services', methods=['GET'])
def get_services():
    category = request.args.get('category')
    services = Service.query.filter_by(category=category).all()
    service_list = [{"id": service.id, "name": service.name} for service in services]
    return jsonify({"services": service_list})

@app.route('/api/customer', methods=['GET'])
@jwt_required()
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def get_customer():
    try:
        user = json.loads(get_jwt_identity())

        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        user_email = user["email"]
        if not user_email:
            return jsonify({"error": "Unauthorized"}), 401

        customer = Customer.query.filter_by(email=user_email).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        print(f"✅ Found Customer: {customer.fname}")
        return jsonify({"name": customer.fname, "flag": customer.flag})

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

# Fetch services under a category
@app.route('/api/services/<category>', methods=['GET'])
def get_services_by_category(category):
    print(category.lower())
    services = (
        db.session.query(Service, Professional)
        .join(Professional, Service.name == Professional.service)
        .filter(Service.category.ilike(category.title()))
        .all()
    )

    if not services:
        return jsonify({"services": []})

    service_list = [
        {
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "rating": professional.rating,
        }
        for service, professional in services
    ]

    return jsonify({"services": service_list})

# Book a service
@app.route('/api/book-service', methods=['GET','POST'])
@jwt_required()
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def book_service():

    # Get logged-in user from JWT token
    user = json.loads(get_jwt_identity())

    # Fetch customer details from database
    customer = Customer.query.filter_by(email=user["email"]).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Get service_id from request body
    data = request.get_json()

    if not data or "service_id" not in data:
        return jsonify({"error": "service_id is required"}), 400

    service_id = data["service_id"]

    # Fetch service details
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    # Find a professional offering this service
    professional = Professional.query.filter_by(service=service.name).first()
    if not professional:
        return jsonify({"error": "No professionals available for this service"}), 404

    # Create a new booking request
    new_request = Request(
        customer_id=user["id"],
        professional_id=professional.id,
        service_id=service.id,
        status="requested",
    )

    db.session.add(new_request)
    db.session.commit()

    print("✅ Booking Request Successfully Created!")
    print(f"🟢 New Service Request Created - ID: {new_request.id}")  # Add this log
    return jsonify({"message": f"Service '{service.name}' booked successfully!"})


@app.route('/api/service-history', methods=['GET'])
@jwt_required()
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def get_service_history():
    try:
        user = json.loads(get_jwt_identity())
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        user_email = user["email"]
        if not user_email:
            return jsonify({"error": "Unauthorized"}), 401

        customer = Customer.query.filter_by(email=user_email).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        service_history = (
            db.session.query(Request, Service, Professional)
            .join(Service, Service.id == Request.service_id)
            .join(Professional, Professional.id == Request.professional_id)
            .filter(Request.customer_id == customer.id)
            .all()
        )

        if not service_history:
            return jsonify({"history": []})

        history_list = [
            {
                "service_name": service.name,
                "price": service.price,
                "professional_name": professional.fname,
                "professional_phone": professional.phone,
                "status": request.status,
                "date": request.request_date,
                "requestId": request.id,
            }
            for request, service, professional in service_history
        ][::-1]

        return jsonify({"history": history_list})

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/close_service', methods=['GET','POST'])
@jwt_required()
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def close_service():
    if request.is_json:
        data = request.get_json()
        print(f"🔍 Received Data: {data}")
        request_id = data.get('request_id')
        new_rating = int(data.get('rating'))
    else:
        return jsonify({"msg": "Request body must be JSON"}), 400

    if not request_id or request_id <= 0:
        return jsonify({"msg": "Invalid request ID"}), 400

    service_req = Request.query.get(request_id)
    if service_req:
        print(f"🔍 Found Service Request: {service_req}")
        professional = Professional.query.get(service_req.professional_id)

        if professional:
            print(f"🔍 Found Professional: {professional}")
            current_rating = professional.rating
            average_rating = (current_rating + new_rating) // 2
            professional.rating = average_rating
            service_req.status = 'closed'
            service_req.completion_date = date.today()
            db.session.commit()
            print(f"🟢 Updated Status to 'closed' for Request ID: {request_id}")
            return jsonify({"msg": "Service request successfully closed", "new_rating": average_rating}), 200
        else:
            print(f"🔴 Professional not found for Request ID: {request_id}")
            return jsonify({"msg": "Professional not found for this service request"}), 404
    else:
        print(f"🔴 Service Request not found: {request_id}")
        return jsonify({"msg": "Service request not found"}), 404


@app.route('/api/search-customer', methods=['GET', 'POST'])
def search_customer():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    if not search_type or not query:
        return jsonify({"error": "Both 'search_type' and 'query' are required."}), 400

    results = []
    try:
        if search_type == "name":
            results = db.session.query(Service, Professional).join(
                Professional, Service.name == Professional.service
            ).filter(Service.name.ilike(f"%{query}%")).all()

        elif search_type == "pincode":
            results = db.session.query(Service, Professional).join(
                Professional, Service.name == Professional.service
            ).filter(Professional.pincode.ilike(f"%{int(query)}%")).all()

        elif search_type == "rating":
            results = db.session.query(Service, Professional).join(
                Professional, Service.name == Professional.service
            ).filter(Professional.rating >= int(query)).all()

        else:
            return jsonify({"error": "Invalid search type. Use 'name', 'pincode', or 'rating'."}), 400

        response = []
        for service, professional in results:
            response.append({
                "service": {
                    "id": service.id,
                    "category": service.category,
                    "name": service.name,
                    "price": service.price,
                    "description": service.description,
                },
                "professional": {
                    "id": professional.id,
                    "fname": professional.fname,
                    "lname": professional.lname,
                    "service": professional.service,
                    "pincode": professional.pincode,
                    "rating": professional.rating,
                    "experience": professional.experience,
                }
            })

        return jsonify({"results": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary-customer', methods=['GET'])
@jwt_required()
@cross_origin(origin="http://localhost:8080", supports_credentials=True)
def summary_customer():
    customer_data = json.loads(get_jwt_identity())
    customer_id = customer_data["id"]
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    closed = Request.query.filter_by(customer_id=customer.id, status='closed').count()
    accepted = Request.query.filter_by(customer_id=customer.id, status='accepted').count()
    rejected = Request.query.filter_by(customer_id=customer.id, status='rejected').count()
    requests = Request.query.filter_by(customer_id=customer.id, status='requested').count()
    requested = closed + accepted + rejected + requests
    data = {
        'id': customer.id,
        'name': customer.fname,
        'requested': requested,
        'accepted': accepted,
        'closed': closed,
        'rejected': rejected,
    }

    return jsonify(data)


# -----------------------PROFESSIONAL-----------------------------------------

@app.route('/api/professional-home', methods=['GET'])
def professional_home_api():
    user_email = request.args.get('email')

    if not user_email:
        return jsonify({"error": "Email is required"}), 400

    professional = Professional.query.filter_by(email=user_email).first()

    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    status_order = case(
        (Request.status == 'requested', 1),
        (Request.status == 'assigned', 2),
        else_=3
    )

    today_services = Request.query.filter(
        Request.professional.has(email=user_email),
        Request.status.in_(["requested", "accepted"])
    ).order_by(status_order).all()

    closed_services = Request.query.filter(
        Request.professional.has(email=user_email),
        Request.status == 'closed'
    ).all()

    return jsonify({
        "professional": {
            "fname": professional.fname,
            "flag": professional.flag  # "waiting", "accepted", or "rejected"
        },
        "todayServices": [
            {
                "id": service.id,
                "customer_name": service.customer.fname,
                "phone": service.customer.phone,
                "address": service.customer.address,
                "status": service.status
            } for service in today_services
        ],
        "closedServices": [
            {
                "id": service.id,
                "customer_name": service.customer.fname,
                "phone": service.customer.phone,
                "address": service.customer.address + ", " + str(service.customer.pincode),
                "request_date": service.request_date,
                "completion_date": service.completion_date
            } for service in closed_services
        ]
    })

@app.route('/api/professional-status', methods=['GET'])
def professional_status():
    email = request.args.get('email')
    professional = Professional.query.filter_by(email=email).first()

    if professional:
        return jsonify({"status": professional.flag})  # Return 'accepted', 'waiting', or 'rejected'
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/accept-request/<int:request_id>', methods=['POST'])
def accept_request_api(request_id):
    service_request = Request.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Request not found'}), 404

    service_request.status = 'accepted'
    db.session.commit()
    return jsonify({'message': 'Service request accepted successfully'})


@app.route('/api/reject-request/<int:request_id>', methods=['POST'])
def reject_request_api(request_id):
    service_request = Request.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Request not found'}), 404

    service_request.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Service request rejected successfully'})

@app.route('/search-professional', methods=['GET'])
@jwt_required()
def search_professional():
    """Render the professional search page."""

    user = json.loads(get_jwt_identity())  # user = {"email": "...", "role": "...", "id": ...}
    user_email = user["email"]

    professional = Professional.query.filter_by(email=user_email).first()
    
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    
    return jsonify({
        "professional": {
            "fname": professional.fname,
            "email": professional.email
        }
    }), 200

@app.route('/api/search-professional', methods=['GET'])
@jwt_required()
def api_search_professional():
    """API endpoint to search requests based on date, pincode, or location."""
    
    search_type = request.args.get('search_type')  # "date", "pincode", "location"
    query = request.args.get('query')

    if not search_type or not query:
        return jsonify({"error": "Both 'search_type' and 'query' are required."}), 400

    try:
        user = json.loads(get_jwt_identity())  # user = {"email": "...", "role": "...", "id": ...}
        user_email = user["email"]

        professional = Professional.query.filter_by(email=user_email).first()
        if not professional:
            return jsonify({"error": "Professional not found"}), 404

        query_result = Request.query.join(Professional).filter(Professional.email == user_email)

        if search_type == "date":
            try:
                search_date = datetime.strptime(query, "%Y-%m-%d").date()
                query_result = query_result.filter(Request.request_date == search_date)
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        elif search_type == "pincode":
            query_result = query_result.join(Customer).filter(Customer.pincode.ilike(f"%{query}%"))

        elif search_type == "location":
            query_result = query_result.join(Customer).filter(Customer.address.ilike(f"%{query}%"))

        else:
            return jsonify({"error": "Invalid search type. Use 'date', 'pincode', or 'location'."}), 400

        results = query_result.all()
        response = []

        for result in results:
            response.append({
                "id": result.id,
                "customer_name": f"{result.customer.fname} {result.customer.lname}",
                "phone": result.customer.phone,
                "location": result.customer.address,
                "request_date": result.request_date.strftime("%Y-%m-%d") if isinstance(result.request_date, (date, datetime)) else str(result.request_date),
                "status": result.status
            })

        return jsonify({"results": response}), 200

    except Exception as e:
        print(f"Error in api_search_professional: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500


@app.route('/api/professional-summary', methods=['GET'])
@jwt_required()
def professional_summary():
    """Fetch the summary of requests handled by a professional."""
    
    user = json.loads(get_jwt_identity())  # user = {"email": "...", "role": "...", "id": ...}
    email = user["email"]

    professional = Professional.query.filter_by(email=email).first()
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    closed = Request.query.filter_by(professional_id=professional.id, status='closed').count()
    accepted = Request.query.filter_by(professional_id=professional.id, status='accepted').count()
    rejected = Request.query.filter_by(professional_id=professional.id, status='rejected').count()
    received = closed + accepted + rejected
    rating = professional.rating

    return jsonify({
        "name": professional.fname,
        "received": received,
        "accepted": accepted,
        "closed": closed,
        "rejected": rejected,
        "rating": rating
    }), 200



@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))


@app.route('/computation')
def computation():
    
    return jsonify({"ans":a+b})

# ------------------ADMIN----------------------------------------------
@app.route('/api/admin-home', methods=['GET'])
def admin_home():
    professionals = [p.serialize() for p in Professional.query.all()]
    services = [s.serialize() for s in Service.query.all()]
    requests = [r.serialize() for r in Request.query.all()][::-1]
    customers = [c.serialize() for c in Customer.query.all()]
    
    return jsonify({
        "services": services,
        "professionals": professionals,
        "customers": customers,
        "requests": requests
    })

@app.route('/api/add-service', methods=['POST'])
def add_service():
    data = request.json
    if all(k in data for k in ("name", "category", "description", "price")):
        new_service = Service(
            name=data["name"],
            category=data["category"],
            description=data["description"],
            price=float(data["price"])
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"message": "Service added successfully!"}), 201
    return jsonify({"error": "All fields are required."}), 400

@app.route('/api/edit-service/<int:service_id>', methods=['POST'])
def edit_service(service_id):
    service = Service.query.get(service_id)
    if service:
        data = request.json
        service.description = data.get('description', service.description)
        service.price = data.get('price', service.price)
        db.session.commit()
        return jsonify({"message": "Service updated successfully"}), 200
    return jsonify({"error": "Service not found"}), 404

@app.route('/api/delete-service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully"}), 200
    return jsonify({"error": "Service not found"}), 404

@app.route('/api/professionals', methods=['GET'])
def get_professionals():
    professionals = Professional.query.all()
    professional_list = [
        {
            "id": p.id,
            "fname": p.fname,
            "experience": p.experience,
            "service": p.service,
            "phone": p.phone,
            "flag": p.flag
        } for p in professionals
    ]
    print(professional_list)
    return jsonify(professional_list)

@app.route('/api/approve_professional/<int:professional_id>', methods=['POST'])
def approve_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if professional:
        professional.flag = 'approved'
        db.session.commit()
        return jsonify({"message": "Professional approved", "status": "success"})
    return jsonify({"message": "Professional not found", "status": "error"}), 404

@app.route('/api/reject_professional/<int:professional_id>', methods=['POST'])
def reject_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if professional:
        professional.flag = 'rejected'
        db.session.commit()
        return jsonify({"message": "Professional rejected", "status": "warning"})
    return jsonify({"message": "Professional not found", "status": "error"}), 404

@app.route('/api/delete_professional/<int:professional_id>', methods=['DELETE'])
def delete_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if professional:
        Request.query.filter_by(professional_id=professional_id).delete()
        db.session.delete(professional)
        db.session.commit()
        return jsonify({"message": "Professional deleted", "status": "danger"})
    return jsonify({"message": "Professional not found", "status": "error"}), 404

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = [{
        "id": customer.id,
        "fname": customer.fname,
        "lname": customer.lname,
        "phone": customer.phone,
        "flag": customer.flag
    } for customer in customers]
    return jsonify({"customers": customer_list})


@app.route('/api/block_customer/<int:customer_id>', methods=['POST'])
def block_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.flag = True
        db.session.commit()
        return jsonify({"message": f"Customer {customer.fname} {customer.lname} has been blocked."}), 200
    return jsonify({"error": "Customer not found"}), 404


@app.route('/api/unblock_customer/<int:customer_id>', methods=['POST'])
def unblock_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.flag = False
        db.session.commit()
        return jsonify({"message": f"Customer {customer.fname} {customer.lname} has been unblocked."}), 200
    return jsonify({"error": "Customer not found"}), 404

@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    service_requests = Request.query.all()
    request_list = [{
        "id": req.id,
        "customer": req.customer.fname if req.customer else "N/A",
        "professional": req.professional.fname if req.professional else "N/A",
        "service_name": req.service.name if req.service else "N/A",
        "request_date": req.request_date.strftime("%Y-%m-%d"),
        "status": req.status
    } for req in service_requests]
    return jsonify({"requests": request_list})

@app.route('/api/search-admin', methods=['GET'])
def search_admin():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    if not search_type or not query:
        return jsonify({"error": "Both 'search_type' and 'query' are required."}), 400

    try:
        results = []
        if search_type == "customer":
            results = Customer.query.filter(
                Customer.fname.ilike(f"%{query}%") | 
                Customer.lname.ilike(f"%{query}%") |
                Customer.email.ilike(f"%{query}%")
            ).all()
        elif search_type == "professional":
            results = Professional.query.filter(
                Professional.fname.ilike(f"%{query}%") | 
                Professional.lname.ilike(f"%{query}%") |
                Professional.email.ilike(f"%{query}%")
            ).all()
        elif search_type == "service_request":
            try:
                search_date = datetime.strptime(query, "%Y-%m-%d").date()
                results = Request.query.filter(Request.request_date == search_date).all()
            except ValueError:
                results = Request.query.filter(
                    Request.status.ilike(f"%{query}%")
                ).all()
        else:
            return jsonify({"error": "Invalid search type."}), 400

        response = []
        for result in results:
            if isinstance(result, Customer):
                response.append({
                    "id": result.id,
                    "name": f"{result.fname} {result.lname}",
                    "email": result.email,
                    "phone": result.phone,
                })
            elif isinstance(result, Professional):
                response.append({
                    "id": result.id,
                    "name": f"{result.fname} {result.lname}",
                    "email": result.email,
                    "specialization": result.service,
                })
            elif isinstance(result, Request):
                response.append({
                    "id": result.id,
                    "request_date": result.request_date.strftime("%Y-%m-%d") if result.request_date else "N/A",
                    "status": result.status,
                    "customer_name": f"{result.customer.fname} {result.customer.lname}",
                    "professional_name": f"{result.professional.fname} {result.professional.lname}" if result.professional else "N/A"
                })

        return jsonify({"results": response}), 200

    except Exception as e:
        print(f"Error in searchAdmin: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500

@app.route('/api/admin-summary')
def summary_admin():
    professionals = len(Professional.query.all())
    customers = len(Customer.query.all())

    closed = Request.query.filter_by(status='closed').count()
    accepted = Request.query.filter_by(status='accepted').count()
    rejected = Request.query.filter_by(status='rejected').count()
    requested = Request.query.filter_by(status='requested').count()
    requests = closed + accepted + rejected + requested

    data = {
        'professionals': professionals,
        'customers': customers,
        'requests': requests,
        'accepted': accepted,
        'closed': closed,
        'rejected': rejected,
    }

    return jsonify(data)