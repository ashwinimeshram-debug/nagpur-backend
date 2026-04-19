from flask import Blueprint, request, jsonify
from extensions import db
from models.contactus import Contactus

contact_bp = Blueprint("contact_bp", __name__)

@contact_bp.route("/api/contact", methods=["POST"])
def create_contact():
    data = request.get_json()

    if not all([data.get("name"), data.get("email"), data.get("phone"), data.get("message")]):
        return jsonify({"error": "All fields required"}), 400

    new_contact = Contactus(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        message=data["message"]
    )

    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Submitted successfully"}), 201