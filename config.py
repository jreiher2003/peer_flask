import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    CACHE_TYPE = "memcached"
    BCRYPT_LOG_ROUNDS = 12
    MAIL_SERVER = os.environ["MAIL_SERVER"]
    MAIL_PORT = os.environ["MAIL_PORT"]
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = '"Site Admin" <noreply@peer2peer.com>'
    SECURITY_UNAUTHORIZED_VIEW = "/login/"
    SECURITY_MSG_UNAUTHORIZED = ("Try loging in first", "danger")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

   
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_SUPPRESS_SEND = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    UPLOADED_PHOTOS_DEST = "/vagrant/peer_flask/app/static/img"
    RESIZE_ROOT = "/vagrant/peer_flask/app/static/img"
    RESIZE_URL = "http://localhost:8600/_uploads/photos/"
    

class ProductionConfig(BaseConfig):
    DEBUG = False
    UPLOADED_PHOTOS_DEST = "/home/www/peer_flask/app/static/img"
    RESIZE_ROOT = "/home/www/peer_flask/app/static/img"
    RESIZE_URL = "http://35.164.137.1/_uploads/photos/"