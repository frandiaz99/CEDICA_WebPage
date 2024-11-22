import requests
from flask import Blueprint, request, jsonify, current_app
from src.web.schemas.contacto import create_contacto_schema, contactos_schema
from src.core.contacto import create_contacto, contacto
from src.web.handlers.auth import check
from os import environ

contacto_api_bp = Blueprint("contacto_api", __name__, url_prefix="/api/contacto")

@contacto_api_bp.get("/")
@check("contacto_index")
def index():
    """
    Endpoint para obtener la lista de contactos.

    Returns:
        Tuple: JSON con la lista de contactos y código de estado HTTP 200.
    """
    contactos = contacto.list_contactos()
    data = contactos_schema.dumps(contactos)
    return data, 200

@contacto_api_bp.post("/")
def create():
    """
    Endpoint para crear un nuevo contacto.

    Este endpoint valida el CAPTCHA usando reCAPTCHA, procesa los datos
    recibidos en el request y crea un contacto en la base de datos.

    Returns:
        Response: JSON indicando éxito o errores de validación.
    """
    data = request.get_json()

    recaptcha_response = data.get('recaptchaResponse')
    RECAPTCHA_SECRET_KEY = current_app.config.get("RECAPTCHA_SECRET_KEY")
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
