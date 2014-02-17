"""These are the models for the blog"""
from datetime import date

from blog import app, bcrypt, db

tags = db.Table('tags',
    db.Column('tag_slug', db.String, db.ForeignKey('tag.slug')),
    db.Column('post_slug', db.String, db.ForeignKey('post.slug'))
)

class Post(db.Model):
    """
    A post on the blog

    :param str slug: Slug of this post (KEY)
    :param datetime.date date: Date of this post
    :param str title: Title of this post
    :param str body_md: Markdown version of this post
    :param str body_html: HTML version of this post (generated automatically from markdown)
    :param str css_file: Optional name of the custom css file
    :param str js_file: Optional name of the custom css file
    :param str user_shortname: Shortname of the user who posted this
    :param User user: User who posted this
    """
    slug = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    title = db.Column(db.String)
    body_md = db.Column(db.Text)
    body_html = db.Column(db.Text)
    css_file = db.Column(db.String, default=None, nullable=True)
    js_file = db.Column(db.String, default=None, nullable=True)
    user_shortname = db.Column(db.String, db.ForeignKey('user.shortname'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('posts'))

    def __str__(self):
        return self.title

class Tag(db.Model):
    """
    A tag for a post

    :param str slug: Slug of this tag (KEY)
    :param str name: Title of this tag
    """
    slug = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __str__(self):
        return self.name

class User(db.Model):
    """
    A user of the blog

    :param str shortname: Shortname of this user (KEY)
    :param str name: Name of this user
    :param str url: URL of this user
    :param str about_md: Markdown version of user's about section
    :param str about_html: HTML version of user's about section (generated automatically from markdown)
    :param str css_file: Optional name of the custom css file
    :param str js_file: Optional name of the custom js file
    :param str password_hash: Hash of this user (bcrypt & salt)
    :param list posts: Posts by this user
    :param list services: Services of this user
    """
    shortname = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String, default=None, nullable=True)
    about_md = db.Column(db.Text, default=None, nullable=True)
    about_html = db.Column(db.Text, default=None, nullable=True)
    css_file = db.Column(db.String, default=None, nullable=True)
    js_file = db.Column(db.String, default=None, nullable=True)
    password_hash = db.Column(db.String)
    posts = db.relationship('Post', backref=db.backref('user'))
    services = db.relationship('Service', backref=db.backref('user'))

    def __str__(self):
        return self.name

    def is_active(self):
        return True

    def get_id(self):
        return self.shortname

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Service(db.Model):
    """
    A service for a user

    :param int id: ID of this service (KEY)
    :param str name: Name of this service
    :param str icon_file: Icon file of this service
    :param str url: URL of this user
    :param str alt_text: Optional alt-text for the icon
    :param str css_class: Optional css class of this icon
    :param str user_shortname: Shortname of this service's user
    :param User user: This service's user
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    icon_file = db.Column(db.String)
    url = db.Column(db.String)
    alt_text = db.Column(db.String, default=None, nullable=True)
    css_class = db.Column(db.String, default=None, nullable=True)
    user_shortname = db.Column(db.String, db.ForeignKey('user.shortname'))

    def __str__(self):
        return "{0} @ {1}".format(str(self.user), self.name)

def create_db_default_user():
    # Create the user, be sure to create a new user and remove this one immediately
    name = app.config.get('DEFAULT_NAME', 'admin')
    password = app.config.get('DEFAULT_PASSWORD', 'admin')
    password_hash = bcrypt.generate_password_hash(password)
    default_user = User(name=name, shortname=name, password_hash=password_hash)

    # Create the db and then add the user in
    db.create_all()
    db.session.add(default_user)
    db.session.commit()