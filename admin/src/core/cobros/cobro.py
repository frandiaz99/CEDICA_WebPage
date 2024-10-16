from datetime import datetime
from src.core.database import db



class Cobro(db.Model):
    __tablename__ = 'cobros'

    id = db.Column(db.Integer, primary_key=True)
    id_ja = db.Column(db.Integer, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime.now)
    tipo_pago = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    beneficiario = db.Column(db.String(100), nullable=True)   
    en_deuda = db.Column(db.Boolean, nullable=False, default=False) 
    observaciones = db.Column(db.String(255), nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)