from app import db

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)  # ✅ Change to nullable=True
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=True)
    role = db.Column(db.String(20), nullable=False, default="user")

