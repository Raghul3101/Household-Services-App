import os
from celery import Celery
from backend.app import create_app  # Import Flask app factory

app = create_app()
app.app_context().push()  # Ensure Celery runs in Flask context

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)
    return celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
)

celery = make_celery(app)