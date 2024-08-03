class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONPLACEHOLDER_BASE_URL = 'https://jsonplaceholder.typicode.com'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_user:password@db:5432/flask_db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_user:password@db:5432/flask_db_prod'
