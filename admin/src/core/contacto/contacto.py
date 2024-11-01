# src/core/contacto/models.py
from datetime import datetime
from src.core.database import db

class Contacto(db.Model):
    __tablename__ = 'contactos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default="pendiente")  
    comentario = db.Column(db.String(255), nullable=True)  
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
