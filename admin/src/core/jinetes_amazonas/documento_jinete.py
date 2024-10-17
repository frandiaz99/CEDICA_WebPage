# src/core/documento/models.py
from datetime import datetime
from src.core.database import db

class DocumentoJinete(db.Model):
    __tablename__ = 'documentos_jinetes'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Entrevista, Evaluación, Planificaciones, etc.
    is_document = db.Column(db.Boolean, nullable=False, default=True)
    
    # Archivo físico o enlace externo
    url = db.Column(db.String(500), nullable=True)  # URL del archivo (en caso de ser un enlace externo)
    #archivo_nombre = db.Column(db.String(255), nullable=True)  # Nombre del archivo físico
    #archivo_tipo = db.Column(db.String(50), nullable=True)  #Tipo de archivo (PDF, DOC, XLS, JPEG)
    
    # Asociado a un jinete o amazona
    jinete_amazonas_id = db.Column(db.Integer, db.ForeignKey('jinetes_amazonas.id'), nullable=False)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    @staticmethod
    def get_jinete_by_document_id(document_id):
    # Busca el documento por ID
        documento = db.session.query(DocumentoJinete).get(document_id)
        if documento:
        # Si el documento existe, devuelve el jinete/amazona relacionado
            return documento.jinete_amazona
        return None  # Si no se encuentra, devuelve None
