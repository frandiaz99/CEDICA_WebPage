from datetime import datetime
from src.core.database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activo =  db.Column(db.Boolean, nullable=False, default=True)
    aceptado_google= db.Column(db.Boolean, nullable=False, default=True)
    issues = db.relationship("Issue", back_populates="user")
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 
    rol = db.relationship("Rol", back_populates="users") 

    def __repr__(self):
        return f'<User #{self.id} email="{self.email}">'
      