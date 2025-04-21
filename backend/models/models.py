from backend import db
from sqlalchemy.sql import func

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.Boolean, default=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fname": self.fname,
            "lname": self.lname,
            "phone": self.phone,
            "address": self.address,
            "pincode": self.pincode,
            "flag": self.flag,
        }


class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    experience = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, default=func.current_date())
    address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, default=3, nullable=True)
    flag = db.Column(db.String(30), default='waiting', nullable=False)  # waiting, approved, rejected

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fname": self.fname,
            "lname": self.lname,
            "service": self.service,
            "phone": self.phone,
            "experience": self.experience,
            "date_created": self.date_created.strftime('%Y-%m-%d') if self.date_created else None,
            "address": self.address,
            "pincode": self.pincode,
            "rating": self.rating,
            "flag": self.flag,
        }


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "price": self.price,
            "description": self.description,
        }


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    request_date = db.Column(db.Date, default=func.current_date(), nullable=False)
    completion_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='requested', nullable=False)
    service = db.relationship('Service', backref='request', lazy=True)
    customer = db.relationship('Customer', backref='request', lazy=True)
    professional = db.relationship('Professional', backref='request', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "customer_id": self.customer_id,
            "professional_id": self.professional_id,
            "request_date": self.request_date.strftime('%Y-%m-%d') if self.request_date else None,
            "completion_date": self.completion_date.strftime('%Y-%m-%d') if self.completion_date else None,
            "status": self.status,
            "service": self.service.serialize() if self.service else None,
            "customer": self.customer.serialize() if self.customer else None,
            "professional": self.professional.serialize() if self.professional else None,
        }
