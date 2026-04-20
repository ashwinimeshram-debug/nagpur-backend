import datetime

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db, mail   # ✅ FIXED
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from flask_jwt_extended import JWTManager
import os
from routes.cms_routes import cms_bp
from routes.contact_routes import contact_bp
from models.models import Admin  # adjust if your model name is different
from werkzeug.security import generate_password_hash


jwt = JWTManager()

app = Flask(__name__)
app.config.from_object(Config)

# 🔐 MAIL CONFIG
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "info@nagpurrealtyhub.com"
app.config["MAIL_PASSWORD"] = "your_app_password"
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")

# INIT EXTENSIONS
mail.init_app(app)
db.init_app(app)
jwt.init_app(app)

# 🌐 CORS
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"]
)

# 📦 REGISTER ROUTES
app.register_blueprint(public_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(cms_bp, url_prefix="/api")
app.register_blueprint(contact_bp)

# 🏠 ROOT
@app.route("/")
def home():
    return "Nagpur Realty Hub API is Running 🚀"

# ❌ 404
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

# 📁 FILE SERVING
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

with app.app_context():
    db.create_all()
if not Admin.query.filter_by(username="admin").first():
        admin = Admin(
            username="admin",
            email="admin@gmail.com",  # ✅ REQUIRED
            name="Admin",             # ✅ safe to add
            password=generate_password_hash("qwerty@123"),
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created successfully")


# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)