"""This is where we initialize all of the packages we will use and create the app object"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
admin = Admin(app, name=app.config.get('BLOG_NAME', 'blog'))

app.wsgi_app = ProxyFix(app.wsgi_app)

from blog import views