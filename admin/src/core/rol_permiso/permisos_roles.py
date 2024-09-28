from datetime import datetime
from src.core.database import db

# Tabla intermedia para la relación muchos a muchos
permisos_roles = db.Table('permisos_roles',
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'), primary_key=True),
    db.Column('inserted_at', db.DateTime, default=datetime.now),
    db.Column('updated_at', db.DateTime, default=datetime.now, onupdate=datetime.now)
)