"""This is the bulk of the views and controls for this flask blog"""
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import login_user, logout_user, login_required, current_user
from markdown import markdown
from flask import redirect, url_for, request, abort
from wtforms import SelectField, BooleanField

from blog import app, db, admin, bcrypt
from blog.models import User, Post, Tag, Service
from blog.forms import LoginForm
from blog.utils import render_template_with_models, get_static_files, get_latest_posts, get_user, get_post

@app.route('/')
def index_view():
    latest_posts = get_latest_posts(5)
    return render_template_with_models('latest_posts.html', latest_posts=latest_posts)

@app.route('/profile/<string:name>/')
def profile_view(name):
    user = get_user(name)
    if user is None:
        abort(404)
    return render_template_with_models('profile.html', user=user)

@app.route('/user/<string:name>/')
def user_view(name):
    user = get_user(name)
    if user is None:
        abort(404)
    user_posts = sorted(user.posts, key=lambda x: x.date)
    return render_template_with_models('user_posts.html', user=user, user_posts=user_posts)

@app.route('/post/<string:slug>/')
def post_view(slug):
    post = get_post(slug)
    if post is None:
        abort(404)
    user = get_user(post.user_shortname)
    services = user.services
    return render_template_with_models('post.html', post=post, user=user, services=services)

@app.route('/tag/<string:slug>/')
def tag_view(slug):
    tag = Tag.query.filter_by(slug=slug).first()
    if tag is None:
        abort(404)
    tag_posts = sorted(tag.posts, key=lambda x: x.date)
    return render_template_with_models('tag_posts.html', tag=tag, tag_posts=tag_posts)

@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = get_user(form.data['shortname'])
        login_user(user)
        return redirect(url_for('index_view'))
    return render_template_with_models('login.html', form=form)

@app.route("/logout/")
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index_view'))

@app.errorhandler(404)
def not_found(error):
    return render_template_with_models('error.html', code=404), 404

class UserView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('shortname', 'name', 'url', 'convert', 'about_md', 'about_html', 'css_file', 'js_file', 'password_hash')
    column_exclude_list = ('password_hash', 'about_md', 'about_html')

    form_overrides = dict(js_file=SelectField, css_file=SelectField)
    form_args = dict(
        js_file=dict(
            choices=get_static_files('js')
        ),
        css_file=dict(
            choices=get_static_files('css')
        ))

    form_extra_fields = dict(
        convert=BooleanField('Convert Markdown')
    )

    def on_model_change(self, form, model, is_created):
        if form.data['convert']:
            model.about_html = markdown(model.about_md, output_format='html5')

        if is_created:
            model.password_hash = bcrypt.generate_password_hash(model.password_hash)

    def is_accessible(self):
        return current_user.is_authenticated()

class PostView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('slug', 'date', 'title', 'body_md', 'convert', 'body_html', 'css_file', 'js_file', 'tags', 'user',)
    column_list = ('slug', 'date', 'title', 'css_file', 'js_file', 'tags', 'user')

    form_overrides = dict(js_file=SelectField, css_file=SelectField)
    form_args = dict(
        js_file=dict(
            choices=get_static_files('js')
        ),
        css_file=dict(
            choices=get_static_files('css')
        ))

    form_extra_fields = {
        'convert': BooleanField('Convert Markdown')
    }

    def on_model_change(self, form, model, is_created):
        if form.data['convert']:
            model.body_html = markdown(model.body_md, output_format='html5')

    def is_accessible(self):
        return current_user.is_authenticated()

class TagView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('slug', 'name')

    def is_accessible(self):
        return current_user.is_authenticated()

class ServiceView(ModelView):
    # Override displayed fields
    column_display_pk = True
    form_columns = ('name', 'icon_file', 'alt_text', 'css_class', 'user', 'url')

    form_overrides = dict(icon_file=SelectField)
    form_args = dict(
        icon_file=dict(
            choices=get_static_files('img')
        ))

    def is_accessible(self):
        return current_user.is_authenticated()

admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(ServiceView(Service, db.session))