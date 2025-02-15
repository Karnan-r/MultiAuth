from flask import Blueprint, request, redirect, session, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from requests_oauthlib import OAuth2Session
import os

from app import db
from app.models import User, Tenant

# ✅ Allow HTTP for OAuth in Development Mode
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  

auth = Blueprint("auth", __name__)

# ✅ Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v2/userinfo"

# ================================================
# 🔵 USER AUTHENTICATION ROUTES (JWT + Google OAuth)
# ================================================

# ✅ Route: Signup - First user in a tenant is admin
@auth.route("/api/signup", methods=["POST"])
def signup():
    data = request.json

    # ✅ Check if the email is already registered
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # ✅ Check if tenant exists, otherwise create a new tenant
    tenant_name = data.get("tenant_name", "DefaultTenant")
    tenant = Tenant.query.filter_by(name=tenant_name).first()
    if not tenant:
        tenant = Tenant(name=tenant_name)
        db.session.add(tenant)
        db.session.commit()

    # ✅ Assign "admin" role to first user in a tenant
    existing_users = User.query.filter_by(tenant_id=tenant.id).count()
    role = "admin" if existing_users == 0 else "user"

    # ✅ Create a new user
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        tenant_id=tenant.id,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully", "role": role, "tenant_id": tenant.id}), 201


# ✅ Route: Login - JWT includes tenant_id and role
@auth.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(
            identity=user.email, 
            additional_claims={"tenant_id": user.tenant_id, "role": user.role}
        )
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


# ✅ Route: Get Current User (Protected)
@auth.route("/api/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if user:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role
        }), 200
    
    return jsonify({"message": "User not found"}), 404


# ✅ Route: Get Users in Same Tenant (Admin Only)
@auth.route("/api/users", methods=["GET"])
@jwt_required()
def get_users():
    user_email = get_jwt_identity()
    admin_user = User.query.filter_by(email=user_email).first()

    if not admin_user or admin_user.role != "admin":
        return jsonify({"message": "Access forbidden"}), 403

    users = User.query.filter_by(tenant_id=admin_user.tenant_id).all()
    user_list = [{"name": u.name, "email": u.email, "role": u.role} for u in users]

    return jsonify(user_list), 200


# ✅ Route: Promote User to Admin (Admin Only)
@auth.route("/api/promote", methods=["POST"])
@jwt_required()
def promote_user():
    user_email = get_jwt_identity()
    data = request.json
    promote_email = data.get("email")

    admin_user = User.query.filter_by(email=user_email).first()
    if not admin_user or admin_user.role != "admin":
        return jsonify({"message": "Access forbidden"}), 403

    user_to_promote = User.query.filter_by(email=promote_email, tenant_id=admin_user.tenant_id).first()
    if not user_to_promote:
        return jsonify({"message": "User not found in your tenant"}), 404

    user_to_promote.role = "admin"
    db.session.commit()

    return jsonify({"message": f"{promote_email} has been promoted to admin"}), 200

# ================================================
# 🔴 GOOGLE OAUTH ROUTES (MANUAL IMPLEMENTATION)
# ================================================

# ✅ Route: Start Google OAuth Login
@auth.route("/login/google")
def google_login():
    print("🔵 Google Login route hit!")  # Debugging log

    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=url_for("auth.google_callback", _external=True),
                           scope=["openid", "email", "profile"])

    auth_url, state = google.authorization_url(GOOGLE_AUTH_URI)
    print(f"🔵 Redirecting to Google: {auth_url}")  # ✅ Print the Google URL

    session["oauth_state"] = state
    return redirect(auth_url)




# ✅ Route: Google OAuth Callback (Fixed)
@auth.route("/login/google/authorized")
def google_callback():
    google = OAuth2Session(GOOGLE_CLIENT_ID, state=session.get("oauth_state"), redirect_uri=url_for("auth.google_callback", _external=True))
    token = google.fetch_token(GOOGLE_TOKEN_URI, client_secret=GOOGLE_CLIENT_SECRET, authorization_response=request.url)

    if not token:
        return jsonify({"message": "Failed to fetch token"}), 403

    session["google_token"] = token
    user_info = google.get(GOOGLE_USERINFO_URI).json()

    # ✅ Check if user exists
    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        tenant = Tenant.query.filter_by(name="GoogleUsers").first()
        if not tenant:
            tenant = Tenant(name="GoogleUsers")
            db.session.add(tenant)
            db.session.commit()

        # ✅ Create user
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            password=None,
            tenant_id=tenant.id,
            role="user"
        )
        db.session.add(user)
        db.session.commit()

    # ✅ Generate JWT
    access_token = create_access_token(identity=user.email, additional_claims={"role": user.role, "tenant_id": user.tenant_id})

    # ✅ Redirect back to frontend with JWT token
    frontend_redirect_url = f"http://127.0.0.1:5173/oauth/callback?token={access_token}"
    return redirect(frontend_redirect_url)







# ✅ Route: Debug Token (Check if Google Token is Stored)
@auth.route("/debug_token")
def debug_token():
    token = session.get("google_token")
    print("🔵 Debugging Google OAuth Token:", token)
    return jsonify({"token": token})


# ✅ Route: Logout (Clears Google Token)
@auth.route("/logout")
def logout():
    session.pop("google_token", None)
    return jsonify({"message": "Logged out successfully"}), 200
