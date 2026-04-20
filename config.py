import os

class Config:
    # 🔐 SECRET KEYS
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "super-secret-key-1234567890-very-secure-key"
    )

    # 🗄️ DATABASE (Render PostgreSQL)
    db_url = os.getenv("DATABASE_URL")

    # Fix Render postgres:// issue
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📁 Uploads
    UPLOAD_FOLDER = "uploads"

    # 🔐 JWT CONFIG (COOKIE BASED AUTH)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

    # 🔥 PRODUCTION SETTINGS (Render HTTPS)
    JWT_COOKIE_SECURE = True          # MUST for HTTPS
    JWT_COOKIE_SAMESITE = "None"      # Required for cross-origin
    JWT_COOKIE_CSRF_PROTECT = False   # Keep false for now (simpler setup)

# # import os

# # class Config:
# #     SECRET_KEY = "your_secret_key"
    
# #     DB_USER = "root"
# #     DB_PASSWORD = ""
# #     DB_HOST = "localhost"
# #     DB_NAME = "nagpur_realty_hub"
    
# #     SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# #     UPLOAD_FOLDER = "uploads"

# #     # 🔐 JWT CONFIG (ADD THIS)
# #     JWT_SECRET_KEY = "super-secret-jwt-key"  # change in production
# #     JWT_TOKEN_LOCATION = ["cookies"]
# #     JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
# #     JWT_COOKIE_SECURE = False  # True in production (HTTPS)
# #     JWT_COOKIE_CSRF_PROTECT = False  # Enable later for security

# import os

# class Config:
#     SECRET_KEY = "your_secret_key"
    
#     DB_USER = "root"
#     DB_PASSWORD = ""
#     DB_HOST = "localhost"
#     DB_NAME = "nagpur_realty_hub"
    
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     UPLOAD_FOLDER = "uploads"

#     # 🔐 JWT CONFIG
#     JWT_SECRET_KEY = "super-secret-key-1234567890-very-secure-key"
#     JWT_TOKEN_LOCATION = ["cookies"]
#     JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

#     JWT_COOKIE_SECURE = True          # ✅ Dev (True in production)
#     JWT_COOKIE_CSRF_PROTECT = False    # ✅ Disable for now (fixes your error)
#     JWT_COOKIE_SAMESITE = "None"        # ✅ IMPORTANT for Chrome
#     JWT_COOKIE_CSRF_PROTECT = False  # Enable later for security