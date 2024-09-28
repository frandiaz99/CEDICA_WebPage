from datetime import datetime
from src.core.database import db

class Permiso(db.Model):
    __tablename__ = "permisos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    roles = db.relationship('Rol', secondary='permisos_roles', back_populates='permisos')

    def __repr__(self):
        return f'<Permiso #{self.id} nombre="{self.nombre}">'