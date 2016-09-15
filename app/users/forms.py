from flask_security.forms import RegisterForm, Required
from wtforms import TextField

class ExtendedConfirmRegisterForm(RegisterForm):
    username = TextField("Username", [Required()])