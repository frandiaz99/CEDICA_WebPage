import requests
from flask import Blueprint, request, jsonify
from src.web.schemas.publicacion import create_publicacion_schema, publicaciones_schema
from src.core import publicacion
publicaciones_api_bp = Blueprint("publicaciones_api", __name__, url_prefix="/api/publicaciones")

@publicaciones_api_bp.get("/")
def index():
    publicaciones = publicacion.list_publicaciones()
    
    data = publicaciones_schema.dumps(publicaciones)
    return data, 200

@publicaciones_api_bp.post("/")
def create():
    data = request.get_json()

    publicacion_data = create_publicacion_schema.load(data)
    publicacion.create_publicacion(**publicacion_data)

    return jsonify({'success': True})
