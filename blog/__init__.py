"""This is a blog"""
from flask import Flask

app = Flask(__name__)
from blog import views