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
    UPLOADED_PHOTOS_DEST = "/var/www/peer_flask/img"
    RESIZE_ROOT = "/var/www/peer_flask/img"
    # RESIZE_URL = "http://35.160.159.170/_uploads/photos/"
    RESIZE_URL = "http://q6rrzsynk7asslo7.onion/_uploads/photos/"