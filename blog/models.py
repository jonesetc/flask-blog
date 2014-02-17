"""These are the models for the blog"""
from datetime import date

from blog import app, bcrypt, db

# Medium object for creating the many-to-many relationship between tags and posts
tags = db.Table('tags',
                db.Column('tag_slug', db.String, db.ForeignKey('tag.slug')),
                db.Column('post_slug', db.String, db.ForeignKey('post.slug'))
)


class Post(db.Model):
    """
    A post on the blog

    :key slug: Slug of this post (KEY)
    :key date: Date of this post
    :key title: Title of this post
    :key lead: The first two sentences of the post for display on selection pages
    :key body_md: Markdown version of this post
    :key body_html: HTML version of this post (generated automatically from markdown)
    :key css_file: Optional name of the custom css file (optional)
    :key js_file: Optional name of the custom css file (optional)
    :key user_shortname: Shortname of the user who posted this
    :key user: User who posted this
    :key tags: Tags for this post
    """
    slug = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    title = db.Column(db.String)
    lead = db.Column(db.Text)
    body_md = db.Column(db.Text)
    body_html = db.Column(db.Text)
    css_file = db.Column(db.String, default=None, nullable=True)
    js_file = db.Column(db.String, default=None, nullable=True)
    user_shortname = db.Column(db.String, db.ForeignKey('user.shortname'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts'))

    def __str__(self):
        """
        Return a string representation of the object

        :return: :rtype: str
        """
        return self.title


class Tag(db.Model):
    """
    A tag for a post

    :key slug: Slug of this tag (KEY)
    :key name: Title of this tag
    :key posts: Posts associated with this tag
    """
    slug = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)


    def __str__(self):
        """
        Return a string representation of the object

        :return: :rtype: str
        """
        return self.name


class User(db.Model):
    """
    A user of the blog

    :key shortname: Shortname of this user (KEY)
    :key name: Name of this user
    :key url: URL of this user (optional)
    :key about_md: Markdown version of user's about section (optional)
    :key about_html: HTML version of user's about section (optional)
    :key css_file: Optional name of the custom css file (optional)
    :key js_file: Optional name of the custom js file (optional)
    :key password_hash: Hash of this user
    :key posts: Posts by this user
    :key services: Services of this user
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
        """
        Return a string representation of the object

        :return: :rtype: str
        """
        return self.name

    def is_active(self):
        """
        Method required for flask-login to check if a user is active

        :return: :rtype: boolean
        """
        return True

    def get_id(self):
        """
        Get the unique identifier for this user

        :return: :rtype: str
        """
        return self.shortname

    def is_authenticated(self):
        """
        Method required for flask-login to check if a user is authenticated

        :return: :rtype: boolean
        """
        return True

    def is_anonymous(self):
        """
        Method required for flask-login to check if a user is anonymous

        :return: :rtype: boolean
        """
        return False

    def check_password(self, password):
        """
        Take a password attempt and see if it matches with the hash on record

        :param password: The password attempt
        :return: :rtype: boolean
        """
        return bcrypt.check_password_hash(self.password_hash, password)


class Service(db.Model):
    """
    A service for a user

    :key id: ID of this service (KEY)
    :key name: Name of this service
    :key icon_file: Icon file of this service
    :key url: URL of this user
    :key css_class: Optional css class of this icon (Optional)
    :key user_shortname: Shortname of this service's user
    :key user: This service's user
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    icon_file = db.Column(db.String)
    url = db.Column(db.String)
    css_class = db.Column(db.String, default=None, nullable=True)
    user_shortname = db.Column(db.String, db.ForeignKey('user.shortname'))

    def __str__(self):
        """
        Return a string representation of the object

        :return: :rtype: str
        """
        return "{0} @ {1}".format(str(self.user), self.name)


def create_db_default_user():
    """
    Create a default user and all tables for the the DB
    """

    # Create the user, be sure to create a new user and remove this one immediately
    name = app.config.get('DEFAULT_USER', 'admin')
    password = app.config.get('DEFAULT_PASSWORD', 'admin')
    password_hash = bcrypt.generate_password_hash(password)
    default_user = User(name=name, shortname=name, password_hash=password_hash)

    # Create the db and then add the user in
    db.create_all()
    db.session.add(default_user)
    db.session.commit()