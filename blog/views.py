"""This is the bulk of the views and controls for this flask blog"""
from blog import app

@app.route('/')
def index_view():
    return "This will be an index"


@app.route('/profile/<string:name>')
def profile_view(name):
    return "This will be a profile for the user named " + name

@app.route('/user/<string:name>')
def user_view(name):
    return "This will be posts with the user named " + name

@app.route('/post/<string:slug>')
def post_view(slug):
    return "This will be a post with the slug " + slug

@app.route('/tag/<string:slug>')
def tag_view(slug):
    return "This will be posts with the tag slug " + slug