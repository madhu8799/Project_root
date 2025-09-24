import os

class Config:
    # Example (PostgreSQL):
    # postgresql+psycopg2://USER:PASSWORD@HOST:5432/DBNAME
    # Example (MySQL):
    # mysql+pymysql://USER:PASSWORD@HOST:3306/DBNAME
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql+psycopg2://appuser:secret@db-host:5432/rootsolutions")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),  # seconds
    }
    # Flask secret key (sessions/CSRF if used later)
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-prod")
