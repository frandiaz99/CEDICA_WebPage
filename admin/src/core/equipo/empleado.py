# src/core/equipo/models.py
from datetime import datetime
from src.core.database import db
from src.core.auth.user import User  # Importa el modelo User
from src.core.equipo.documento import Documento  # Importa el modelo Documento
class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    domicilio = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    localidad = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    profesion = db.Column(db.String(100), nullable=False)
    puesto_laboral = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    contacto_emergencia = db.Column(db.String(200), nullable=True)
    obra_social = db.Column(db.String(100), nullable=True)
    numero_afiliado = db.Column(db.String(50), nullable=True)
    condicion = db.Column(db.String(20), nullable=False)  # Voluntario o Personal Rentado
    activo = db.Column(db.Boolean, default=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relación con User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Asociación opcional
    user = db.relationship('User', backref='empleado', lazy=True)

    # Relación con Encuestre
    encuestres = db.relationship("Encuestre", back_populates="entrenadores_conductores", lazy=True)

    documentos = db.relationship('Documento', backref='empleado', lazy=True)

