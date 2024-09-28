from datetime import datetime
from src.core.database import db

class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    users = db.relationship("User", back_populates="rol") 

    permisos = db.relationship('Permiso', secondary='permisos_roles', back_populates='roles')

    def __repr__(self):
        return f'<Rol #{self.id} nombre="{self.nombre}">'