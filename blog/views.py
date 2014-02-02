"""This is the bulk of the views and controls for this flask blog"""
from blog import app

@app.route('/')
@app.route('/index')
def index():
    return "This will be an index"
