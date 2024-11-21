from datetime import datetime
from src.core.database import db



class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=True)
    autor = db.Column(db.String(40), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=True)
    copete = db.Column(db.String(100), nullable=True)
    contenido = db.Column(db.String(3000), nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(15), nullable=False)