from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, NumberRange, Length, ValidationError, EqualTo
from wtforms import TextField, SubmitField, FloatField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user 
from .models import Users

def validate_username(form, field):
    username = Users.query.filter(Users.username == field.data).one_or_none()
    if username is not None:
        raise ValidationError("A user with that username already exists.")

def validate_profile_username(form, field):
    username = Users.query.filter(Users.username == field.data).one_or_none()
    if username is not None and current_user.username != field.data:
        raise ValidationError("A user with that username already exists.")

def password_validator(form, field):
    """ passwords must have one lowercase letter, on uppercase letter and one digit. """
    password = list(field.data)
    password_length = len(password) 
    lowers = uppers = digits = 0 
    for c in password:
        if c.islower(): lowers+=1
        if c.isupper(): uppers+=1
        if c.isdigit(): digits+=1
    is_valid = password_length >= 12 and lowers and uppers and digits
    if not is_valid:
        raise ValidationError("You need 12 characters, at least one upper, lower, and one digit.")

def positve_bitcoin(form, field):
    if field.data < 0:
        raise ValidationError("Only positive values please.")

class LoginForm(FlaskForm):
    email = EmailField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = TextField("Username",  [InputRequired(), validate_username])#
    email = EmailField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long."), password_validator])
    password_confirm = PasswordField("Confirm", [InputRequired(), EqualTo("password", message="Your passwords don't match.")])
    submit = SubmitField("Register")

class RecoverPasswordForm(FlaskForm):
    email = EmailField("Email", [InputRequired(), Email()])
    submit = SubmitField("Reset Password")

class SendEmailConfirmForm(FlaskForm):
    email = EmailField("Email", [InputRequired(), Email()])
    submit = SubmitField("Resend confirmation")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long.")])
    new_password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long."), password_validator])
    new_password_confirm = PasswordField("Confirm", [InputRequired(), EqualTo("new_password", message="Your passwords don't match.")])
    submit = SubmitField("Change Password")

class ChangePasswordTokenForm(FlaskForm):
    password = PasswordField("Password", [InputRequired(), Length(min=12, message="The min password length is 12 chars long."), password_validator])
    password_confirm = PasswordField("Confirm", [InputRequired(), EqualTo("password", message="Your passwords don't match.")])
    submit = SubmitField("Change Password")

class ProfileForm(FlaskForm):
    username = TextField("Username",  [InputRequired(), validate_profile_username])
    email = EmailField("Email", [InputRequired(), Email()])
    avatar = FileField("Avatar", [FileAllowed(['jpg','png','JPG','PNG','JPEG'], "Images only!")])
    submit = SubmitField("Update")
    
class BitcoinWalletForm(FlaskForm):
    submit = SubmitField("Create a wallet")

class BitcoinWithdrawlForm(FlaskForm):
    amount = FloatField("Bitcoin Amount", [InputRequired(), positve_bitcoin])
    address = TextField("Bitcoin Address", [InputRequired(), Length(min=8, message="That address doesn't appear to be long enough.")])
    submit = SubmitField("Widthdrawl")

class DeleteUserForm(FlaskForm):
    submit = SubmitField("Delete Your Account")