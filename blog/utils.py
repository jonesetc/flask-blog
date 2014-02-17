import os
from functools import partial

from flask import render_template

from blog import login
from blog.models import Tag, User, Post, Service

def get_all_tags():
    return Tag.query.all()

def get_all_users():
    return User.query.all()

def get_all_posts():
    return Post.query.all()

render_template_with_models = partial(render_template, users=get_all_users, tags=get_all_tags, posts=get_all_posts)

def get_static_files(static_dir):
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', static_dir)
    return [(f, f) for f in os.listdir(dir)] + [('', '')]

def get_latest_posts(num):
    return Post.query.order_by(Post.date.desc()).limit(num)

@login.user_loader
def get_user(userid):
    return User.query.filter_by(shortname=userid).first()

def get_post(slug):
    return Post.query.filter_by(slug=slug).first()