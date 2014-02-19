# flask-blog

This is a work in progress. It is a very simple blog built with flask. The end goal is to have a blog that supports multiple authors and basic search and filter operations.

## Setup

- Create a virtualenv
- Run `pip install -r requirements.txt`
- Create a file in the top directory named `config.py`
    - You must set `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`, `BLOG_NAME`, any other settings are optional
- Activate and start your virtualenv and run the `create_db_default_user` located in `blog/models`
- Start the development server with `python run.py`
- Now you can log in with the username and password `admin` at `localhost:5000/login/`
- Visit `localhost:5000/admin/`
    - Create a new user for yourself
    - Switch users
    - Remove the default user
    - Now start creating posts, users, tags, and services

## Notes

- Feel free to use this blog structure any way that you would like
- We have tried to keep things general when possible, but this isn't intended to be a base for any other blogs, so sometimes things are a bit hardcoded
- Always glad to hear any comments of pull requests, even if we're not striving for perfection

## Attributions

- The blog as it stands relies upon [Foundation](http://foundation.zurb.com/) for some great css gridding and js utilities
    - This means we're also relying upon [jQuery](http://jquery.com/)
- By default we're using [Open Sans](http://www.google.com/fonts/specimen/Open+Sans)