import datetime
import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db, mail
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from routes.cms_routes import cms_bp
from routes.contact_routes import contact_bp
from flask_jwt_extended import JWTManager

jwt = JWTManager()

app = Flask(__name__)
app.config.from_object(Config)

# =========================
# 🔐 MAIL CONFIG
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "info@nagpurrealtyhub.com"
app.config["MAIL_PASSWORD"] = "your_app_password"

# =========================
# 📁 UPLOAD CONFIG
# =========================
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")

# =========================
# 🔐 JWT CONFIG (FIXED)
# =========================
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True  # REQUIRED for HTTPS (Render)
app.config["JWT_COOKIE_SAMESITE"] = "None"  # REQUIRED for cross-origin
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

# 🔥 VERY IMPORTANT (MISSING BEFORE)
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"

# =========================
# INIT EXTENSIONS
# =========================
mail.init_app(app)
db.init_app(app)
jwt.init_app(app)

# =========================
# 🌐 CORS (FIXED)
# =========================
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:3000",
        "https://nagpurrealtyhub.com",  # future frontend
    ],
)

# =========================
# 📦 REGISTER ROUTES
# =========================
app.register_blueprint(public_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(cms_bp, url_prefix="/api")
app.register_blueprint(contact_bp)

# =========================
# 🏠 ROOT
# =========================
@app.route("/")
def home():
    return "Nagpur Realty Hub API is Running 🚀"

# =========================
# ❌ 404
# =========================
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

# =========================
# 📁 FILE SERVING
# =========================
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)