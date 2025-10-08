import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/root.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.getenv("FLASK_ENV", "development")
