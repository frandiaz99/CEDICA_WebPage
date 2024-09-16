from flask import Flask
from flask import render_template
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp



def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    app.register_error_handler(404, error.not_found_error)
    
    app.register_blueprint(issues_bp)

    return app 

