from flask_wtf import Form
from wtforms.validators import InputRequired, Email, NumberRange, Length, ValidationError, EqualTo
from wtforms import TextField, SubmitField, FloatField, PasswordField, BooleanField
from flask_wtf.html5 import EmailField
from .models import Users

def validate_username(form, field):
    username = Users.query.filter(Users.username == field.data).one_or_none()
    if username is not None:
        raise ValidationError("A user with that username already exists")

def positve_bitcoin(form, field):
    if field.data < 0:
        raise ValidationError("Only positive values please.")

class LoginForm(Form):
    username = TextField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterForm(Form):
    username = TextField("Username",  [InputRequired(), validate_username])
    email = EmailField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long.")])
    password_confirm = PasswordField("Confirm", [InputRequired(), EqualTo("password", message="Your passwords don't match.")])
    submit = SubmitField("Register")

class RecoverPasswordForm(Form):
    email = EmailField("Email", [InputRequired(), Email()])
    submit = SubmitField("Reset Password")

class SendEmailConfirmForm(Form):
    email = EmailField("Email", [InputRequired(), Email()])
    submit = SubmitField("Resend confirmation")

class ChangePasswordForm(Form):
    password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long.")])
    new_password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long.")])
    new_password_confirm = PasswordField("Confirm", [InputRequired(), EqualTo("new_password", message="Your passwords don't match.")])
    submit = SubmitField("Register")





class ProfileForm(Form):
    username = TextField("Username",  [InputRequired(), validate_username])
    email = EmailField("Email", [InputRequired(), Email()])
    # password = PasswordField("Password")
    avatar = TextField("Avatar")
    submit = SubmitField("Update")
    
class BitcoinWalletForm(Form):
    create = SubmitField("Create a wallet")

class BitcoinWithdrawlForm(Form):
    amount = FloatField("Bitcoin Amount", [InputRequired(), positve_bitcoin])
    address = TextField("Bitcoin Address", [InputRequired(), Length(min=8, message="That address doesn't appear to be long enough.")])
    submit = SubmitField("Widthdrawl")
