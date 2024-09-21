from datetime import datetime
from src.core.database import db

class Encuestre(db.Model):
    __tablename__ = "encuestres"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime)
    sexo = db.Column(db.String(10))
    raza = db.Column(db.String(80), nullable=False)
    pelaje = db.Column(db.String(80), nullable=False)
    compra_donacion = db.Column(db.String(80), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now())
    #sede_asignada = db.relationship("Sede", back_populates="encuestre")
    #tipo_ja_asignado = db.relationship("JA", back_populates="encuestre")
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Encuestre #{self.id}">'