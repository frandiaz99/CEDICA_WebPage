import requests
from flask import Blueprint, request, jsonify, current_app
from src.web.schemas.contacto import create_contacto_schema, contacto_schema, contactos_schema
from src.core.contacto import create_contacto 
from src.web.handlers.auth import check
from src.core.contacto import contacto
from os import environ
contacto_api_bp = Blueprint("contacto_api", __name__, url_prefix="/api/contacto")


@contacto_api_bp.get("/")
@check("contacto_index")
def index():
    contactos = contacto.list_contactos()
    data = contactos_schema.dumps(contactos)

    return data,200

@contacto_api_bp.post("/")
def create():
    data = request.get_json()
    recaptcha_response = data.get('recaptchaResponse')
    RECAPTCHA_SECRET_KEY = "6LfWlX8qAAAAAKtyOVroeG5-cxu15F8WUkVOY5Ss"
    secret_key = str(RECAPTCHA_SECRET_KEY)

    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    verify_data = {
        'secret': secret_key,
        'response': recaptcha_response
    }

    verify_response = requests.post(verify_url, data=verify_data)
    verify_result = verify_response.json()

    if not verify_result.get('success'):
        return jsonify({'error': 'reCAPTCHA validation failed'}), 400

    data.pop('recaptchaResponse')
    contacto_data = create_contacto_schema.load(data)
    create_contacto(**contacto_data)

    return jsonify({'success': True})
