import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "sqlite:///peer.db"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "jeffreiher@gmail.com"
    MAIL_PASSWORD = "7797finn"
    MAIL_DEFAULT_SENDER = '"Jeff" <jeffreiher@gmail.com>'
    
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True 
    # SECURITY_BLUEPRINT_NAME = "security"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'
    SECURITY_POST_LOGIN_VIEW = "/nfl/"

    USER_APP_NAME = "Peer2Peer"
 
    
   
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_SUPPRESS_SEND = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    

class ProductionConfig(BaseConfig):
    DEBUG = False