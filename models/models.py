from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import db

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    listing_id = db.Column(db.String(20), unique=True)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    transaction_type = db.Column(
        db.Enum('buy', 'sell', 'rent'),
        nullable=False
    )

    property_type = db.Column(
        db.Enum('flat', 'plot', 'house', 'commercial'),
        nullable=False
    )

    price = db.Column(db.Numeric(12, 2))

    location = db.Column(db.String(255), nullable=False)

    status = db.Column(
        db.Enum('pending', 'approved', 'rejected'),
        default='pending'
    )

    is_active = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_closed = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    closed_at = db.Column(db.DateTime, nullable=True)

    # ✅ ONLY define relationship here
    contacts = db.relationship(
        "Contact",
        backref="property",   # auto creates contact.property
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Property {self.id} - {self.title}>"
    
class Contact(db.Model):
    __tablename__ = "contacts"   # ⚠️ make sure DB table name matches

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=True
    )

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    mobile = db.Column(db.String(15), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ❌ DO NOT define relationship here again

    def __repr__(self):
        return f"<Contact {self.id} - {self.name}>"

class PropertyImage(db.Model):
    __tablename__ = "property_images"
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # ✅ NEW
    name = db.Column(db.String(120), nullable=True)                 # ✅ NEW

    password = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(20), nullable=True)                 # ✅ NEW
    profile_image = db.Column(db.String(255), nullable=True)        # ✅ NEW

    is_active = db.Column(db.Boolean, default=True)                 # ✅ NEW

    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)      # ✅ NEW

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)              # ✅ NEW

class Enquiry(db.Model):
    __tablename__ = "enquiries"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer)

    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    mobile = db.Column(db.String(15))
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

