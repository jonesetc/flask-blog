"""This is the bulk of the views and controls for this flask blog"""
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import login_user, logout_user, login_required
from markdown import markdown
from flask import redirect, render_template, url_for, request

from blog import app, db, admin
from blog.models import User, Post, Tag, Service, load_user
from blog.forms import LoginForm

@app.route('/')
def index_view():
    return "This will be an index"

@app.route('/profile/<string:name>/')
def profile_view(name):
    return "This will be a profile for the user named " + name

@app.route('/user/<string:name>/')
def user_view(name):
    return "This will be posts with the user named " + name

@app.route('/post/<string:slug>/')
def post_view(slug):
    return "This will be a post with the slug " + slug

@app.route('/tag/<string:slug>/')
def tag_view(slug):
    return "This will be posts with the tag slug " + slug

@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = load_user(form.data['shortname'])
        login_user(user)
        return redirect(url_for('index_view'))
    print(form.data)
    return render_template('login.html', form=form)

@app.route("/logout/")
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index_view'))

class UserView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('shortname', 'name', 'url', 'about_md', 'about_html', 'css_file', 'js_file')
    column_exclude_list = ('password_hash', 'about_md', 'about_html')

    def on_model_change(self, form, model, is_created):
        if model.about_html:
            model.about_html = markdown(model.about_md, output_format='html5')

class PostView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('slug', 'date', 'title', 'body_md', 'body_html', 'css_file', 'js_file', 'tags', 'user')
    column_list = ('slug', 'date', 'title', 'css_file', 'js_file', 'tags', 'user')

    def on_model_change(self, form, model, is_created):
        model.body_html = markdown(model.body_md, output_format='html5')

class TagView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('slug', 'name')

class ServiceView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('name', 'icon_file', 'alt_text', 'css_class', 'user')

admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(ServiceView(Service, db.session))