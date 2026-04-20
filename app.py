# from flask import Flask, send_from_directory
# from flask_cors import CORS
# from config import Config
# from models.models import db
# from routes.public_routes import public_bp
# from routes.admin_routes import admin_bp
# from flask_jwt_extended import JWTManager
# import os
# from extensions import mail
# from routes.cms_routes import cms_bp
# from models.cms_models import HeroSlide, Service, Advantage, Footer
# from routes.contact_routes import contact_bp



# # 🔐 INIT JWT
# jwt = JWTManager()

# # 🔥 CREATE APP
# app = Flask(__name__)
# app.config.from_object(Config)

# # 🔐 MAIL CONFIG
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = "your_email@gmail.com"
# app.config["MAIL_PASSWORD"] = "your_app_password"

# # ✅ THIS IS WHERE YOU ADD IT
# mail.init_app(app)

# # 🌐 CORS (IMPORTANT for cookies)
# CORS(
#     app,
#     supports_credentials=True,
#     origins=["http://localhost:3000"]
# )

# # 🗄️ INIT DATABASE
# db.init_app(app)

# # 🔐 INIT JWT WITH APP (🔥 THIS WAS MISSING)
# jwt.init_app(app)

# # 📦 REGISTER ROUTES
# app.register_blueprint(public_bp, url_prefix="/api")
# app.register_blueprint(admin_bp, url_prefix="/api/admin")
# app.register_blueprint(cms_bp, url_prefix="/api")
# app.register_blueprint(contact_bp)
# # app.register_blueprint(cms_bp, url_prefix="/api/cms")

# # 🏠 ROOT ROUTE
# @app.route("/")
# def home():
#     return "Nagpur Realty Hub API is Running 🚀"

# # ❌ 404 HANDLER
# @app.errorhandler(404)
# def not_found(e):
#     return {"error": "Route not found"}, 404

# # 📁 FILE SERVING
# UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# # 🚀 RUN APP
# if __name__ == "__main__":
#     app.run(debug=True)


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

# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)