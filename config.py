import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key-12345')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///calendar.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False