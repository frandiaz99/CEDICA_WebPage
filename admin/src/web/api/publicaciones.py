from flask import Blueprint, request, jsonify
from src.web.schemas.publicacion import create_publicacion_schema, publicaciones_schema
from src.core import publicacion
from src.web.handlers.auth import check
publicaciones_api_bp = Blueprint("publicaciones_api", __name__, url_prefix="/api/publicaciones")

@publicaciones_api_bp.get("/")
@check("administracion_index")
def index():
    """
    Ruta para obtener todas las publicaciones.

    Esta función utiliza el método `list_publicaciones` para recuperar todas las publicaciones
    almacenadas y las serializa en formato JSON para ser retornadas como respuesta.

    Returns:
        Tuple[str, int]: Datos serializados de las publicaciones (JSON) y código de estado HTTP 200.
    """
    publicaciones = publicacion.list_publicaciones()
    
    data = publicaciones_schema.dumps(publicaciones)
    return data, 200

@publicaciones_api_bp.post("/")
@check("administracion_new")
def create():
    """
    Ruta para crear una nueva publicación.

    Esta función recibe datos en formato JSON, los valida utilizando un esquema de carga,
    y llama a `create_publicacion` para crear una nueva publicación en la base de datos.

    Returns:
        Response: Respuesta JSON indicando el éxito de la operación.
    """
    data = request.get_json()

    publicacion_data = create_publicacion_schema.load(data)
    publicacion.create_publicacion(**publicacion_data)

    return jsonify({'success': True})
