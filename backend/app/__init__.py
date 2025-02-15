from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_migrate import Migrate
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Load configuration
    app.config.from_object('app.config.Config')

    # ✅ Explicitly define a session type in case it's missing
    if not app.config.get("SESSION_TYPE"):
        app.config["SESSION_TYPE"] = "filesystem"  # Default fallback

    Session(app)  # ✅ Initialize Flask-Session

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # ✅ Register Blueprints (Avoid duplicate registration)
    from app.routes import auth
    if "auth" not in app.blueprints:
        app.register_blueprint(auth, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app
