import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "sqlite:///peer.db"

    MAIL_USERNAME = "jeffreiher@gmail.com"
    MAIL_PASSWORD = "7797finn"
    MAIL_DEFAULT_SENDER = '"Jeff" <jeffreiher@gmail.com>'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
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