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
    is_document = db.Column(db.Boolean, nullable=False, default=True)

    encuestre_id = db.Column(db.Integer, db.ForeignKey('encuestres.id'), nullable=True)
    

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    encuestre = db.relationship('Encuestre', back_populates='documentos')

    @staticmethod
    def get_encuestre_by_document_id(document_id):
        documento = db.session.query(DocumentoEncuestre).get(document_id)
        if documento:
            return documento.encuestre
        return None 