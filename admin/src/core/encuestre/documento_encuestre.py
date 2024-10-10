# src/core/equipo/models.py
from datetime import datetime
from src.core.database import db
from src.core.encuestre import Encuestre


class DocumentoEncuestre(db.Model):
    __tablename__ = 'documentos_encuestre'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    operacion = db.Column(db.String(200), nullable=True)

    encuestre_id = db.Column(db.Integer, db.ForeignKey('encuestres.id'), nullable=False)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    encuestre = db.relationship('Encuestre', back_populates='documentos')