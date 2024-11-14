from flask import Blueprint, request, jsonify
from src.core import auth
from src.web.handlers.auth import check
from src.core import contacto
from src.web.schemas.contacto import contactos_schema, create_contacto_schema, contacto_schema
contacto_api_bp = Blueprint("contacto_api", __name__, url_prefix="/api/contacto")

@contacto_api_bp.get("/")
def index():
    contactos = contacto.list_contactos()
    data = contactos_schema.dumps(contactos)

    return data,200

@contacto_api_bp.post("/")
def create():
    data = request.get_json()
    errors = create_contacto_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    else:
        new_contacto = create_contacto_schema.load(data)
    
    return contacto_schema.dumps(new_contacto), 201
