from flask_security.forms import RegisterForm, Required, ValidationError
from wtforms import TextField
from .models import Users

def validate_username(form, field):
    username = Users.query.filter(Users.username == field.data).first()
    if username is not None:
        raise ValidationError("A user with that username already exists")

class ExtendedConfirmRegisterForm(RegisterForm):
    username = TextField("Username", [Required(), validate_username])