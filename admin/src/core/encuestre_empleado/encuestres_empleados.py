from datetime import datetime
from src.core.database import db

# Tabla intermedia para la relación muchos a muchos
encuestre_empleado = db.Table('encuestre_empleado',
    db.Column('encuestre_id', db.Integer, db.ForeignKey('encuestres.id'), primary_key=True),
    db.Column('empleado_id', db.Integer, db.ForeignKey('empleados.id'), primary_key=True),
    db.Column('inserted_at', db.DateTime, default=datetime.now),
    db.Column('updated_at', db.DateTime, default=datetime.now, onupdate=datetime.now)
)
