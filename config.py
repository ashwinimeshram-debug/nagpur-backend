# import os

# class Config:
#     SECRET_KEY = "your_secret_key"
    
#     DB_USER = "root"
#     DB_PASSWORD = ""
#     DB_HOST = "localhost"
#     DB_NAME = "nagpur_realty_hub"
    
#     SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     UPLOAD_FOLDER = "uploads"

#     # 🔐 JWT CONFIG (ADD THIS)
#     JWT_SECRET_KEY = "super-secret-jwt-key"  # change in production
#     JWT_TOKEN_LOCATION = ["cookies"]
#     JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
#     JWT_COOKIE_SECURE = False  # True in production (HTTPS)
#     JWT_COOKIE_CSRF_PROTECT = False  # Enable later for security

import os

class Config:
    SECRET_KEY = "your_secret_key"
    
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_NAME = "nagpur_realty_hub"
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = "uploads"

    # 🔐 JWT CONFIG
    JWT_SECRET_KEY = "super-secret-key-1234567890-very-secure-key"
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

    JWT_COOKIE_SECURE = False          # ✅ Dev (True in production)
    JWT_COOKIE_CSRF_PROTECT = False    # ✅ Disable for now (fixes your error)
    JWT_COOKIE_SAMESITE = "Lax"        # ✅ IMPORTANT for Chrome
    JWT_COOKIE_CSRF_PROTECT = False  # Enable later for security