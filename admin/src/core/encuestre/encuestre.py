from datetime import datetime
from src.core.database import db
from src.core.encuestre_empleado import encuestres_empleados

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
    sede_asignada = db.Column(db.String(100), nullable=True)
    tipo_ja_asignado = db.Column(db.String(80), nullable = False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    entrenadores_conductores = db.relationship('Empleado', secondary='encuestre_empleado',cascade="all, delete", back_populates='encuestres')

    def __repr__(self):
        return f'<Encuestre #{self.id}">'
    
    # Función para obtener el encuestre por ID
    @staticmethod
    def obtener_encuestre_por_id(encuestre_id):
        return db.session.query(Encuestre).filter(Encuestre.id == encuestre_id).first()