"""These are the forms for the blog"""
from wtforms import Form, TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired

from blog.utils import get_user


def validate_login(form, field):
    """
    Validation method to check that the user is valid and the password matches

    :param form: The form from the login template
    :param field: The Field this validator is attached to
    :raise ValidationError: Raises if the user is invalid or the password does not match
    """
    user = get_user(form.shortname.data)

    if user is None:
        raise ValidationError('Invalid user')
    elif not user.check_password(form.password.data):
        raise ValidationError('Bad password')


class LoginForm(Form):
    shortname = TextField('Short Name', validators=[DataRequired(), validate_login])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember login')