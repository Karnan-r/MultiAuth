from datetime import timedelta
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///multiauth.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # ✅ Flask-Session Configuration
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_FILE_DIR = os.path.join(os.getcwd(), "flask_sessions")
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "flasksession_"
