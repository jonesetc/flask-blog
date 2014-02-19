"""These are utility functions for the blog"""
import os
from functools import partial

from flask import render_template

from blog import app, login
from blog.models import Tag, User, Post


def get_all_tags():
    """
    Gets a list of all tags in the DB

    :return: :rtype: list
    """
    return Tag.query.all()


def get_all_users():
    """
    Gets a list of all users in the DB

    :return: :rtype: list
    """
    return User.query.all()


def get_all_posts():
    """
    Gets a list of all posts in the DB

    :return: :rtype: list
    """
    return Post.query.all()

# get the blog name for the templates
blog_name = app.config.get('BLOG_NAME', 'flask-blog')

# Create a partially applied version of render_template. This way all templates will have info for navigation
render_template_with_models = partial(render_template, blog_name=blog_name, users=get_all_users, tags=get_all_tags,
                                      posts=get_all_posts)


def get_static_files(static_dir):
    """
    Gets a list of tuples representing all valid static files in the specified folder for use in admin pages

    :param static_dir: Which static directory to look in
    :return: :rtype: list
    """
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', static_dir)
    return [(f, f) for f in os.listdir(dir)] + [('', '')]


def get_latest_posts(num):
    """
    Gets a list of the latest posts

    :param num: Number of posts to return
    :return: :rtype: list
    """
    return Post.query.order_by(Post.date.desc()).limit(num)


@login.user_loader
def get_user(userid):
    """
    Get a User object

    :param userid: The shortname of the user to fetch
    :return: :rtype: User
    """
    return User.query.filter_by(shortname=userid).first()


def get_post(slug):
    """
    Get a Post object

    :param slug: The slug of the post to fetch
    :return: :rtype: Post
    """
    return Post.query.filter_by(slug=slug).first()