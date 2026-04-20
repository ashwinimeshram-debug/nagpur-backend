import os
from datetime import timedelta

class Config:
    SECRET_KEY = "your_secret_key"

    DB_USER = "root"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_NAME = "nagpur_realty_hub"

    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"

    # 🔐 JWT CONFIG (PRODUCTION READY)
    JWT_SECRET_KEY = "super-secret-jwt-key"

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

    # 🔥 TOKEN EXPIRY (IMPORTANT)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # 🔒 COOKIE SECURITY
    JWT_COOKIE_SECURE = False  # ⚠️ CHANGE TO True IN PRODUCTION (HTTPS)
    JWT_COOKIE_SAMESITE = "Lax"

    # 🔥 CSRF PROTECTION (ENABLE IN PRODUCTION)
    JWT_COOKIE_CSRF_PROTECT = False  # 👉 set True later with frontend support

    # 🔒 PREVENT JAVASCRIPT ACCESS
    JWT_COOKIE_HTTPONLY = True