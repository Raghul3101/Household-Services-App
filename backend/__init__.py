from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
import jwt
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:8080"])
app.config['SECRET_KEY'] = 'c482ba3f2b73413d9638e3a710edfa35'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from backend.models import models
from backend.routes import routes

if __name__ == '__main__':
    app.run(debug=True)