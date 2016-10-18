from flask_security.forms import RegisterForm, ValidationError
from flask_wtf import Form
from wtforms.validators import DataRequired, InputRequired, Email, NumberRange, Length
from wtforms import TextField, SubmitField, FloatField, PasswordField
from flask_wtf.html5 import EmailField
from .models import Users

def validate_username(form, field):
    username = Users.query.filter(Users.username == field.data).first()
    if username is not None:
        raise ValidationError("A user with that username already exists")

def positve_bitcoin(form, field):
    if field.data < 0:
        raise ValidationError("Only positive values please.")

class ExtendedConfirmRegisterForm(RegisterForm):
    username = TextField("Username", [InputRequired(), validate_username])

class BitcoinWalletForm(Form):
    create = SubmitField("Create a wallet")

class BitcoinWithdrawlForm(Form):
    amount = FloatField("Bitcoin Amount", [InputRequired(), positve_bitcoin])
    address = TextField("Bitcoin Address", [InputRequired(), Length(min=8, message="That address doesn't appear to be long enough.")])
    submit = SubmitField("Widthdrawl")

class ProfileForm(Form):
    username = TextField("Username",  [InputRequired(), validate_username])
    email = EmailField("Email", [InputRequired(), Email()])
    # password = PasswordField("Password")
    avatar = TextField("Avatar")
    submit = SubmitField("Update")
    
