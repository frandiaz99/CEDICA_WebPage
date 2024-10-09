from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.equipo import equipo_bp
from src.web.controllers.auth import login_bp
from src.web.controllers.encuestres import encuestre_bp
from src.web.controllers.users import users_bp
from src.web.handlers.auth import is_authenticated
from src.web.handlers.auth import check_permission
from src.core import database
from src.core.config import config
from src.core import seeds
from src.core.bcrypt import bcrypt
from flask_session import Session
from src.web.storage import storage
from src.web import helpers

session = Session()

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config['SECRET_KEY'] = '1234'

    app.config.from_object(config[env])
    database.init_app(app)

    session.init_app(app)
    bcrypt.init_app(app)

    storage.init_app(app)

    @app.route("/")
    def login():
        return render_template("auth/login.html")
        
    
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    @app.route("/home")
    def home():
        return render_template("home.html")
    
    @app.route("/jinetes_amazonas")
    def jinetes_amazonas():
        return render_template("jinetes_amazonas.html")
    
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(401, error.unauthorized)
    
    app.register_blueprint(issues_bp)

    app.register_blueprint(equipo_bp)

    app.register_blueprint(encuestre_bp)

    app.register_blueprint(login_bp)

    app.register_blueprint(users_bp)

    app.jinja_env.globals.update(is_authenticated=is_authenticated)

    app.jinja_env.globals.update(check_permission=check_permission)

    app.jinja_env.globals.update(documento_url=helpers.documento_url)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seed-db")
    def seed_db():
        seeds.run()

    return app 

