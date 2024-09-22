# src/core/equipo/models.py
from datetime import datetime
from src.core.database import db
from src.core.auth.user import User  # Importa el modelo User


class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    archivo = db.Column(db.String(200), nullable=False)  # Ruta del archivo en el servidor o Minio
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

