from flask import Flask, render_template
from flask_session import Session
from flask_cors import CORS
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.equipo import equipo_bp
from src.web.controllers.auth import login_bp
from src.web.controllers.encuestres import encuestre_bp
from src.web.controllers.users import users_bp
from src.web.controllers.pagos import pagos_bp
from src.web.controllers.jinetes_amazonas import jinete_amazonas_bp
from src.web.controllers.cobros import cobros_bp
from src.web.controllers.contacto import contacto_bp
from src.web.controllers.reportes import reportes_bp
from src.web.handlers.auth import is_authenticated, check_permission
from src.core import database, seeds
from src.core.config import config
from src.core.bcrypt import bcrypt
from src.web.storage import storage
from src.web import helpers
from src.web.api.contacto import contacto_api_bp

# Inicialización de sesiones
session = Session()

def create_app(env="development", static_folder="../../static"):
    """
    Crea e inicializa una instancia de Flask con configuración específica del entorno.

    Args:
        env (str): Nombre del entorno ('development', 'production', 'testing').
        static_folder (str): Ruta al directorio de archivos estáticos.

    Returns:
        Flask: La instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__, static_folder=static_folder)

    # Configuración del entorno
    app.config.from_object(config[env])

    # Inicialización de extensiones
    database.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)
    storage.init_app(app)

    # Configuración de CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    # Rutas base
    @app.route("/")
    def login():
        """Renderiza la página de inicio de sesión."""
        return render_template("auth/login.html")

    @app.route("/home")
    def home():
        """Renderiza la página de inicio o dashboard."""
        return render_template("home.html")

    @app.route("/perfil")
    def perfil():
        """Renderiza la página de perfil de usuario."""
        return render_template("auth/perfil.html")

    # Controladores de errores
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(401, error.unauthorized)

    # Registro de blueprints
    app.register_blueprint(equipo_bp)
    app.register_blueprint(encuestre_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(cobros_bp)
    app.register_blueprint(jinete_amazonas_bp)
    app.register_blueprint(contacto_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(contacto_api_bp)

    # Funciones globales para Jinja2
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(documento_url=helpers.documento_url)

    # Inyección de URLs de imágenes desde MinIO
    @app.context_processor
    def inject_minio_url():
        """
        Inyecta URLs de imágenes de MinIO para ser usadas en las plantillas.
        """
        image_names = [
            'img_layout/icono_cedica.jpg',
            'img_layout/icono_usuario.png'
        ]
        return helpers.inject_minio_image_url(storage, image_names)

    # Comandos de la línea de comandos para gestión de la base de datos
    @app.cli.command(name="reset-db")
    def reset_db():
        """
        Comando CLI para reiniciar la base de datos.
        """
        database.reset()

    @app.cli.command(name="seed-db")
    def seed_db():
        """
        Comando CLI para cargar datos iniciales en la base de datos.
        """
        seeds.run()

    return app
