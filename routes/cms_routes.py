from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.cms_models import HeroSlide, Service, Advantage
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import time
import os



# ✅ Create Blueprint
cms_bp = Blueprint("cms", __name__)

# =========================
# 🔥 HERO SECTION
# =========================

# Public
@cms_bp.route("/hero", methods=["GET"])
def get_hero():
    slides = HeroSlide.query.order_by(HeroSlide.order).all()

    return jsonify([{
        "id": s.id,
        "image": s.image,
        "title": s.title,
        "subtitle": s.subtitle,
        "button_text": s.button_text,
        "button_link": s.button_link,
        "is_active": s.is_active
    } for s in slides])

@cms_bp.route("/hero/<int:id>", methods=["PUT"])
@jwt_required()
def update_hero(id):
    data = request.json
    slide = HeroSlide.query.get_or_404(id)

    slide.title = data.get("title")
    slide.subtitle = data.get("subtitle")
    slide.image = data.get("image")
    slide.button_text = data.get("button_text")
    slide.button_link = data.get("button_link")

    db.session.commit()
    return {"message": "Updated"}

@cms_bp.route("/hero/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_hero(id):
    slide = HeroSlide.query.get_or_404(id)
    db.session.delete(slide)
    db.session.commit()
    return {"message": "Deleted"}

@cms_bp.route("/hero/toggle/<int:id>", methods=["PATCH"])
@jwt_required()
def toggle_hero(id):
    slide = HeroSlide.query.get_or_404(id)
    slide.is_active = not slide.is_active
    db.session.commit()

    return {"message": "Updated"}

@cms_bp.route("/hero/reorder", methods=["POST"])
@jwt_required()
def reorder_hero():
    data = request.json  # [{id, order}]

    for item in data:
        slide = HeroSlide.query.get(item["id"])
        slide.order = item["order"]

    db.session.commit()
    return {"message": "Reordered"}


# Admin (protected)
@cms_bp.route("/admin/hero", methods=["POST"])
@jwt_required()
def add_hero():
    data = request.json

    slide = HeroSlide(
        image=data.get("image"),
        title=data.get("title"),
        subtitle=data.get("subtitle"),
        button_text=data.get("button_text"),
        button_link=data.get("button_link"),
        is_active=True
    )

    db.session.add(slide)
    db.session.commit()

    return jsonify({"message": "Hero added successfully"}), 201


# =========================
# 🔥 SERVICES SECTION
# =========================

# @cms_bp.route("/services", methods=["GET"])
# def get_services():
#     services = Service.query.filter_by(is_active=True).all()

#     return jsonify([
#         {
#             "id": s.id,
#             "title": s.title,
#             "description": s.description,
#             "image": s.image
#         }
#         for s in services
#     ])


# @cms_bp.route("/admin/services", methods=["POST"])
# @jwt_required()
# def add_service():
#     data = request.json

#     service = Service(
#         title=data.get("title"),
#         description=data.get("description"),
#         image=data.get("image"),
#         is_active=True
#     )

#     db.session.add(service)
#     db.session.commit()

#     return jsonify({"message": "Service added"}), 201


# =========================
# 🔥 ADVANTAGES SECTION
# =========================

@cms_bp.route("/advantages", methods=["GET"])
def get_advantages():
    advantages = Advantage.query.filter_by(is_active=True).all()

    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "icon": a.icon
        }
        for a in advantages
    ])


@cms_bp.route("/admin/advantages", methods=["POST"])
@jwt_required()
def add_advantage():
    data = request.json

    advantage = Advantage(
        title=data.get("title"),
        description=data.get("description"),
        icon=data.get("icon"),
        is_active=True
    )

    db.session.add(advantage)
    db.session.commit()

    return jsonify({"message": "Advantage added"}), 201

@cms_bp.route("/admin/advantages/<int:id>", methods=["PUT"])
@jwt_required()
def update_advantage(id):
    data = request.json

    advantage = Advantage.query.get_or_404(id)

    advantage.title = data.get("title")
    advantage.description = data.get("description")

    db.session.commit()

    return jsonify({"message": "Advantage updated"})

@cms_bp.route("/admin/advantages/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_advantage(id):
    advantage = Advantage.query.get_or_404(id)

    db.session.delete(advantage)
    db.session.commit()

    return jsonify({"message": "Advantage deleted"})



@cms_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # create unique filename
    filename = str(int(time.time())) + "_" + secure_filename(file.filename)

    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return jsonify({
        "url": f"https://nagpur-backend.onrender.com/uploads/{filename}"
    })

    
# =========================
# ✅ GET ALL SERVICES
# =========================
@cms_bp.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()

    return jsonify([{
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "image": s.image
    } for s in services])


# =========================
# ✅ ADD SERVICE
# =========================
@cms_bp.route("/admin/services", methods=["POST"])
@jwt_required()
def add_service():
    data = request.json

    service = Service(
        title=data.get("title"),
        description=data.get("description"),
        image=data.get("image")
    )

    db.session.add(service)
    db.session.commit()

    return {"message": "Service added"}


# =========================
# ✅ UPDATE SERVICE
# =========================
@cms_bp.route("/admin/services/<int:id>", methods=["PUT"])
# @jwt_required()
def update_service(id):
    data = request.json

    service = Service.query.get_or_404(id)

    service.title = data.get("title")
    service.description = data.get("description")
    service.image = data.get("image")

    db.session.commit()

    return {"message": "Service updated"}


# =========================
# ✅ DELETE SERVICE
# =========================
@cms_bp.route("/admin/services/<int:id>", methods=["DELETE"])
# @jwt_required()
def delete_service(id):
    service = Service.query.get_or_404(id)

    db.session.delete(service)
    db.session.commit()

    return {"message": "Service deleted"}