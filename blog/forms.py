from wtforms import Form, TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired

from blog.utils import get_user

def validate_login(form, field):
        user = get_user(form.shortname.data)

        if user is None:
            raise ValidationError('Invalid user')
        elif not user.check_password(form.password.data):
            raise ValidationError('Bad password')

class LoginForm(Form):
    shortname = TextField('Short Name', validators=[DataRequired(), validate_login])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember login')