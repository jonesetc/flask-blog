"""This is where we initialize all of the packages we will use and create the app object"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.admin import Admin

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
admin = Admin(app, name=app.config.get('BLOG_NAME', 'blog'))

from blog import views