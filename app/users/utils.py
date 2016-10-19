from itsdangerous import URLSafeTimedSerializer
from urlparse import urlparse, urljoin  
from app import app, mail 
from app.nfl.utils import make_salt
from app.users.models import Users
from flask import request, url_for, current_app, render_template
from flask_mail import Message 
from flask_login import current_user

def get_ip():
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    return user_ip

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def generate_confirmation_token(email):
    t_salt = "thdfsfwewewrwrwjsljfalii3333"
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=t_salt)

def confirm_token(token, expriation=3600):
    t_salt = "thdfsfwewewrwrwjsljfalii3333"
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=t_salt, max_age=expriation)
    except:
        return False
    return email 

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def profile_confirm_email():
    user = Users.query.filter_by(id=current_user.id).one()
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template("security/email/welcome.html", confirm_url=confirm_url, user=user)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)