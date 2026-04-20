from flask import Blueprint, request, jsonify, current_app
from models.models import db, Property, Admin, Contact
from datetime import datetime
import bcrypt
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies
)
from models.models import Property, PropertyImage
import os
from werkzeug.utils import secure_filename
import time
import secrets
from flask_mail import Message
from extensions import mail



admin_bp = Blueprint("admin", __name__)

# =========================
# 🔐 ADMIN LOGIN (NO JWT REQUIRED)
# =========================
@admin_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    admin = Admin.query.filter_by(username=data["username"]).first()

    if not admin:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        admin.password.encode("utf-8")
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🔥 CREATE JWT TOKEN
    # access_token = create_access_token(identity={
    #     "id": admin.id,
    #     "username": admin.username,
    #     "role": "admin"
    # })

    access_token = create_access_token(identity=str(admin.id))

    response = jsonify({"message": "Login successful"})

    # 🍪 SET COOKIE
    set_access_cookies(response, access_token)

    return response


# =========================
# 🚪 API for auto-redirect:
# =========================
@admin_bp.route("/check-auth", methods=["GET"])
@jwt_required()
def check_auth():
    current_admin = get_jwt_identity()
    return jsonify({
        "message": "Authenticated",
        "admin_id": current_admin
    })



# =========================
# 🚪 LOGOUT
# =========================
@admin_bp.route("/logout", methods=["POST"])
# @jwt_required()
def logout():
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response


# =========================
# 📋 GET ALL PROPERTIES
# =========================
@admin_bp.route("/properties", methods=["GET"])
@jwt_required()
def get_all_properties():
    current_admin = get_jwt_identity()
    # current_admin_id = get_jwt_identity()
    # print(current_admin_id)

    properties = Property.query.order_by(Property.created_at.desc()).all()

    result = []
    for p in properties:
        result.append({
            "id": p.id,
            "listing_id": p.listing_id,
            "title": p.title,
            "status": p.status,
            "is_active": p.is_active,
            "is_closed": p.is_closed,
            "is_featured": p.is_featured,
            "is_verified": p.is_verified,
            "created_at": p.created_at
        })

    return jsonify(result)


# =========================
# ✅ APPROVE PROPERTY
# =========================
@admin_bp.route("/approve/<int:id>", methods=["POST"])
@jwt_required()
def approve_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.status = "approved"
    property.is_active = True

    db.session.commit()

    return jsonify({"message": "Property approved"})


# =========================
# ❌ REJECT PROPERTY
# =========================
@admin_bp.route("/reject/<int:id>", methods=["POST"])
@jwt_required()
def reject_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.status = "rejected"
    property.is_active = False

    db.session.commit()

    return jsonify({"message": "Property rejected"})


# =========================
# 🔄 CLOSE PROPERTY
# =========================
@admin_bp.route("/close/<int:id>", methods=["POST"])
@jwt_required()
def close_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.is_closed = True
    property.is_active = False
    property.closed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Property marked as closed"})


# =========================
# 🔁 REOPEN PROPERTY
# =========================
@admin_bp.route("/reopen/<int:id>", methods=["POST"])
@jwt_required()
def reopen_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.is_closed = False
    property.is_active = True
    property.closed_at = None

    db.session.commit()

    return jsonify({"message": "Property reopened"})


# =========================
# ⭐ TOGGLE FEATURED
# =========================
@admin_bp.route("/feature/<int:id>", methods=["POST"])
@jwt_required()
def toggle_featured(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.is_featured = not property.is_featured

    db.session.commit()

    return jsonify({
        "message": "Featured status updated",
        "is_featured": property.is_featured
    })


# =========================
# ✅ TOGGLE VERIFIED
# =========================
@admin_bp.route("/verify/<int:id>", methods=["POST"])
@jwt_required()
def toggle_verified(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    property.is_verified = not property.is_verified

    db.session.commit()

    return jsonify({
        "message": "Verified status updated",
        "is_verified": property.is_verified
    })

# @admin_bp.route("/property/<int:id>", methods=["GET"])
# @jwt_required()
# def get_property(id):
#     property = Property.query.get(id)

#     if not property:
#         return jsonify({"error": "Property not found"}), 404

#     return jsonify({
#         "id": property.id,
#         "listing_id": property.listing_id,
#         "title": property.title,
#         "description": property.description,
#         "price": property.price,
#         "location": property.location,
#         "city": property.city,
#         "state": property.state,
#         "pincode": property.pincode,
#         "property_type": property.property_type,
#         "bedrooms": property.bedrooms,
#         "bathrooms": property.bathrooms,
#         "area": property.area,
#         "status": property.status,
#         "is_closed": property.is_closed,
#         "is_featured": property.is_featured,
#         "created_at": property.created_at
#     })

@admin_bp.route("/property/<int:id>", methods=["PUT"])
@jwt_required()
def update_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    data = request.json

    property.title = data.get("title", property.title)
    property.description = data.get("description", property.description)
    property.price = data.get("price", property.price)
    property.location = data.get("location", property.location)
    # property.city = data.get("city", property.city)
    # property.state = data.get("state", property.state)
    # property.pincode = data.get("pincode", property.pincode)
    # property.bedrooms = data.get("bedrooms", property.bedrooms)
    # property.bathrooms = data.get("bathrooms", property.bathrooms)
    # property.area = data.get("area", property.area)

    db.session.commit()

    return jsonify({"message": "Property updated"})

# @admin_bp.route("/property/<int:id>", methods=["GET"])
# @jwt_required()
# def get_property(id):
#     property = Property.query.get(id)

#     if not property:
#         return jsonify({"error": "Property not found"}), 404

#     images = PropertyImage.query.filter_by(property_id=id)\
#         .order_by(PropertyImage.order.asc()).all()

#     image_list = [
#         {"id": img.id, "url": img.image_url}
#         for img in images
#     ]

#     return jsonify({
#         "id": property.id,
#         "listing_id": property.listing_id,
#         "title": property.title,
#         "description": property.description,
#         "price": property.price,
#         "location": property.location,
#         # "city": property.city,
#         # "state": property.state,
#         # "pincode": property.pincode,
#         # "bedrooms": property.bedrooms,
#         # "bathrooms": property.bathrooms,
#         # "area": property.area,
#         "status": property.status,
#         "is_closed": property.is_closed,
#         "is_featured": property.is_featured,

#         # ✅ SEND IMAGES ARRAY
#         "images": image_list
#     })

@admin_bp.route("/property/<int:id>", methods=["GET"])
@jwt_required()
def get_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    # ✅ FETCH CONTACT USING property_id
    contact = Contact.query.filter_by(property_id=id).first()
    

    images = PropertyImage.query.filter_by(property_id=id)\
        .order_by(PropertyImage.order.asc()).all()

    image_list = [
        {"id": img.id, "url": img.image_url}
        for img in images
    ]

    return jsonify({
        "id": property.id,
        "title": property.title,
        "description": property.description,
        "price": property.price,
        "location": property.location,

        # ✅ FIXED
        "name": contact.name if contact else None,
        "email": contact.email if contact else None,
        "phone": contact.mobile if contact else None,

        "images": image_list
    })

@admin_bp.route("/property/<int:id>/contacts", methods=["GET"])
@jwt_required()
def get_property_contacts(id):
    # 🔍 Check property exists
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    # 📞 Fetch contacts
    contacts = Contact.query.filter_by(property_id=id).all()

    # 🧾 Format response
    contact_list = []
    for contact in contacts:
        contact_list.append({
            "id": contact.id,
            "name": contact.name,
            "mobile": contact.mobile,
            "email": contact.email,
            "created_at": contact.created_at.strftime("%Y-%m-%d %H:%M:%S") if contact.created_at else None
        })

    return jsonify({
        "property_id": id,
        "total_contacts": len(contact_list),
        "contacts": contact_list
    }), 200



@admin_bp.route("/property-nav/<int:id>", methods=["GET"])
@jwt_required()
def property_navigation(id):
    prev_property = Property.query.filter(Property.id < id).order_by(Property.id.desc()).first()
    next_property = Property.query.filter(Property.id > id).order_by(Property.id.asc()).first()

    return jsonify({
        "prev_id": prev_property.id if prev_property else None,
        "next_id": next_property.id if next_property else None
    })


@admin_bp.route("/upload-image/<int:property_id>", methods=["POST"])
@jwt_required()
def upload_image(property_id):
    if "image" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["image"]

    filename = f"{int(time.time())}_{secure_filename(file.filename)}"

    upload_path = os.path.join("uploads", filename)
    file.save(upload_path)

    new_image = PropertyImage(
        property_id=property_id,
        image_url=f"uploads/{filename}"
    )

    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "Image uploaded"})

@admin_bp.route("/delete-image/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(image_id):
    image = PropertyImage.query.get(image_id)

    if not image:
        return jsonify({"error": "Not found"}), 404

    # delete file
    try:
        os.remove(image.image_url)
    except:
        pass

    db.session.delete(image)
    db.session.commit()

    return jsonify({"message": "Deleted"})

@admin_bp.route("/upload-images/<int:property_id>", methods=["POST"])
@jwt_required()
def upload_images(property_id):
    files = request.files.getlist("images")

    if not files:
        return jsonify({"error": "No files"}), 400

    # get current max order
    last_image = PropertyImage.query.filter_by(property_id=property_id)\
        .order_by(PropertyImage.order.desc()).first()

    start_order = last_image.order + 1 if last_image else 1

    for i, file in enumerate(files):
        filename = f"{int(time.time())}_{secure_filename(file.filename)}"
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        new_image = PropertyImage(
            property_id=property_id,
            image_url=f"uploads/{filename}",
            order=start_order + i
        )

        db.session.add(new_image)

    db.session.commit()

    return jsonify({"message": "Images uploaded"})

@admin_bp.route("/reorder-images", methods=["POST"])
@jwt_required()
def reorder_images():
    data = request.json  # [{id:1, order:1}, ...]

    for item in data:
        img = PropertyImage.query.get(item["id"])
        if img:
            img.order = item["order"]

    db.session.commit()

    return jsonify({"message": "Reordered"})

@admin_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    data = request.json
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # check old password
    if not bcrypt.checkpw(
        data["old_password"].encode("utf-8"),
        admin.password.encode("utf-8")
    ):
        return jsonify({"error": "Old password incorrect"}), 400

    # update password
    new_password = bcrypt.hashpw(
        data["new_password"].encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    admin.password = new_password
    db.session.commit()

    return jsonify({"message": "Password updated"})

from datetime import datetime, timedelta
import secrets

@admin_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({"error": "Email not found"}), 404

    token = secrets.token_urlsafe(32)

    # 🔥 SET EXPIRY (15 min)
    expiry = datetime.utcnow() + timedelta(minutes=15)

    admin.reset_token = token
    admin.reset_token_expiry = expiry
    db.session.commit()

    reset_link = f"http://localhost:3000/reset-password/{token}"

    # 👉 Email sending will be below

    return send_reset_email(email, reset_link)

from datetime import datetime

@admin_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.json

    admin = Admin.query.filter_by(reset_token=token).first()

    if not admin:
        return jsonify({"error": "Invalid token"}), 400

    # 🔥 CHECK EXPIRY
    if admin.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Token expired"}), 400

    hashed_password = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    admin.password = hashed_password
    admin.reset_token = None
    admin.reset_token_expiry = None

    db.session.commit()

    return jsonify({"message": "Password reset successful"})

from extensions import mail
from flask_mail import Message

def send_reset_email(email, reset_link):
    msg = Message(
        subject="Reset Your Password - Nagpur Realty Hub",
        sender="your_email@gmail.com",
        recipients=[email]
    )

    # 🔥 HTML EMAIL
    msg.html = f"""
    <div style="font-family: Arial; padding:20px;">
        <h2 style="color:#2563eb;">Nagpur Realty Hub</h2>

        <p>Hello,</p>

        <p>You requested to reset your password.</p>

        <p style="margin:20px 0;">
            <a href="{reset_link}" 
               style="background:#2563eb;color:white;padding:10px 20px;
               text-decoration:none;border-radius:6px;">
               Reset Password
            </a>
        </p>

        <p>This link will expire in <b>15 minutes</b>.</p>

        <p>If you did not request this, ignore this email.</p>

        <hr>

        <small>© Nagpur Realty Hub</small>
    </div>
    """

    mail.send(msg)

    return jsonify({"message": "Reset link sent to email"})

@admin_bp.route("/property/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    if not property.is_closed:
        return jsonify({"error": "Property must be closed before deleting"}), 400

    # 🔥 Delete related contacts
    Contact.query.filter_by(property_id=id).delete()

    # 🔥 Delete related images (if exists)
    PropertyImage.query.filter_by(property_id=id).delete()

    db.session.delete(property)
    db.session.commit()

    return jsonify({"message": "Property deleted successfully"}), 200