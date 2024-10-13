# src/core/equipo/models.py
from datetime import datetime
from src.core.database import db
from src.core.auth.user import User  # Importa el modelo User
from src.core.equipo.documento import Documento  # Importa el modelo Documento
from src.core.encuestre_empleado import encuestres_empleados

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    domicilio = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    profesion = db.Column(db.String(100), nullable=False)
    puesto_laboral = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    contacto_emergencia = db.Column(db.String(200), nullable=False)
    obra_social = db.Column(db.String(100), nullable=False)
    numero_afiliado = db.Column(db.String(50), nullable=False)
    condicion = db.Column(db.String(20), nullable=False)  # Voluntario o Personal Rentado
    activo = db.Column(db.Boolean, default=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relación con Encuestre
    encuestres = db.relationship('Encuestre', secondary='encuestre_empleado', back_populates='entrenadores_conductores')
    documentos = db.relationship('Documento', backref='empleado', lazy=True)

