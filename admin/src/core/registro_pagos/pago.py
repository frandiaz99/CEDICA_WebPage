from datetime import datetime
from src.core.database import db



class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    beneficiario = db.Column(db.String(100), nullable=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tipo_pago = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)