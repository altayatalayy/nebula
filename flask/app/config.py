import secrets
import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5000

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SHARE_FOLDER = './share'
    IGNORED_FILES = '|'.join(['.*\.swp$'])

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db.sqlite'
