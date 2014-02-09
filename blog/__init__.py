"""This is a blog"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
admin = Admin(app)
CsrfProtect(app)

from blog import views, models