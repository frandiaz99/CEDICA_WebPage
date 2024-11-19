from datetime import datetime
from src.core.database import db



class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(40), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.String(255), nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    estado = db.Column(db.String(15), nullable=False)