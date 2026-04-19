from flask import Blueprint, request, jsonify
from models.models import db, Property, PropertyImage, Contact, Enquiry
from utils.helpers import generate_listing_id
import os
from werkzeug.utils import secure_filename
from datetime import datetime

public_bp = Blueprint("public", __name__)

UPLOAD_FOLDER = "uploads"


# =========================
# 📤 SUBMIT PROPERTY
# =========================

@public_bp.route("/submit-property", methods=["POST"])
def submit_property():
    data = request.form

    # Basic validation (removed mobile from required)
    required_fields = ["title", "transaction_type", "property_type", "price", "location", "name"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # Mobile OR Email validation
    if not data.get("mobile") and not data.get("email"):
        return jsonify({"error": "Mobile or Email is required"}), 400

    try:
        property = Property(
            title=data.get("title"),
            description=data.get("description"),
            price=float(data.get("price")),
            location=data.get("location"),
            transaction_type=data.get("transaction_type"),
            property_type=data.get("property_type"),
            status="pending",
            is_active=False
        )

        db.session.add(property)
        db.session.commit()

        # Generate listing ID
        property.listing_id = generate_listing_id(property.id)
        db.session.commit()

        # Save contact
        contact = Contact(
            property_id=property.id,
            name=data.get("name"),
            email=data.get("email"),
            mobile=data.get("mobile")
        )
        db.session.add(contact)

        # Ensure upload folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Save images
        files = request.files.getlist("images")
        for file in files:
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                unique_name = f"{int(datetime.utcnow().timestamp())}_{filename}"
                path = os.path.join(UPLOAD_FOLDER, unique_name)

                file.save(path)

                image = PropertyImage(
                    property_id=property.id,
                    image_url=f"uploads/{unique_name}"
                )
                db.session.add(image)

        db.session.commit()

        return jsonify({
            "message": "Property submitted for review",
            "listing_id": property.listing_id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# 🔍 GET PROPERTIES (WITH FILTERS + FEATURED)
# =========================
@public_bp.route("/properties", methods=["GET"])
def get_properties():
    query = Property.query.filter_by(
        status="approved",
        is_active=True,
        is_closed=False
    )

    # Filters
    location = request.args.get("location")
    transaction_type = request.args.get("type")
    property_type = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    featured = request.args.get("featured")

    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))

    if transaction_type:
        query = query.filter_by(transaction_type=transaction_type)

    if property_type:
        query = query.filter_by(property_type=property_type)

    if min_price:
        query = query.filter(Property.price >= float(min_price))

    if max_price:
        query = query.filter(Property.price <= float(max_price))

    if featured == "true":
        query = query.filter_by(is_featured=True)

    properties = query.order_by(Property.created_at.desc()).all()

    result = []
    for p in properties:
        # ✅ Get images for each property
        images = PropertyImage.query.filter_by(property_id=p.id).all()

        result.append({
            "id": p.id,
            "listing_id": p.listing_id,
            "title": p.title,
            "price": p.price,
            "location": p.location,
            "is_featured": p.is_featured,
            "is_verified": p.is_verified,
            "images": [img.image_url for img in images]  # ✅ FIXED
        })

    return jsonify(result)

# =========================
# 📄 GET PROPERTY DETAIL
# =========================
@public_bp.route("/property/<int:id>", methods=["GET"])
def get_property_detail(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({"error": "Property not found"}), 404

    images = PropertyImage.query.filter_by(property_id=id).all()

    # ✅ FIXED RELATION
    # contact = property.contact
    contact = Contact.query.filter_by(property_id=id).first()
    
    return jsonify({
        "id": property.id,
        "listing_id": property.listing_id,
        "title": property.title,
        "description": property.description,
        "price": property.price,
        "location": property.location,
        "images": [img.image_url for img in images],
        "is_featured": property.is_featured,
        "is_verified": property.is_verified,

        "contact": {
            "name": contact.name if contact else None,
            "mobile": contact.mobile if contact else None,
            "email": contact.email if contact else None
         }
    })


# =========================
# 📩 ENQUIRY (LEAD CAPTURE)
# =========================
@public_bp.route("/enquiry", methods=["POST"])
def create_enquiry():
    data = request.json

    if not data or not data.get("property_id") or not data.get("mobile"):
        return jsonify({"error": "property_id and mobile are required"}), 400

    try:
        enquiry = Enquiry(
            property_id=data.get("property_id"),
            name=data.get("name"),
            email=data.get("email"),
            mobile=data.get("mobile"),
            message=data.get("message")
        )

        db.session.add(enquiry)
        db.session.commit()

        return jsonify({"message": "Enquiry submitted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500