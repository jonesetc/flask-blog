from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired

from blog.models import User, load_user

def validate_login(form, field):
        user = load_user(form.shortname.data)

        if user is None:
            raise ValidationError('Invalid user')
        elif not user.check_password(form.password.data):
            raise ValidationError('Bad password')

class LoginForm(Form):
    shortname = TextField('Short Name', validators=[DataRequired(), validate_login])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember login')