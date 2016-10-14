from flask_security.forms import RegisterForm, Required, ValidationError
from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import TextField, SubmitField, FloatField, PasswordField
from flask_wtf.html5 import EmailField
from .models import Users

def validate_username(form, field):
    username = Users.query.filter(Users.username == field.data).first()
    if username is not None:
        raise ValidationError("A user with that username already exists")

class ExtendedConfirmRegisterForm(RegisterForm):
    username = TextField("Username", [Required(), validate_username])

class BitcoinWalletForm(Form):
    create = SubmitField("Create a wallet")

class BitcoinWithdrawlForm(Form):
    submit = SubmitField("Widthdrawl")
    amount = FloatField("Amount", validators=[DataRequired()])
    address = TextField("Address", validators=[DataRequired()])

class ProfileForm(Form):
    username = TextField("Username", validators=[DataRequired])
    email = EmailField("Email Address", [Required()])
    password = PasswordField("Password", [Required()])
    avatar = TextField("Avatar")
    submit = SubmitField("Change")
    
