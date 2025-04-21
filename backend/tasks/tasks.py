from backend.tasks.celery_worker import celery
from flask_mail import Mail, Message
from backend.app import create_app
from backend import db
from backend.models.models import Request, Professional
from datetime import datetime

app = create_app()
app.app_context().push()

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='guest123master@gmail.com',
    MAIL_PASSWORD='guest@54321'
)

mail = Mail(app)

@celery.task
def send_daily_reminders():
    with app.app_context():
        today = datetime.today().date()
        pending_requests = Request.query.filter_by(status='requested').all()

        for request in pending_requests:
            professional = Professional.query.get(request.professional_id)
            if professional and professional.email:
                msg = Message(
                    subject="Reminder: Pending Service Request",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[professional.email],
                    body=f"Dear {professional.name},\n\nYou have pending service requests. Please visit the platform to respond.\n\nThank you!"
                )
                mail.send(msg)
                print(f"📧 Reminder sent to {professional.email}")

    return "Daily reminders sent!"
