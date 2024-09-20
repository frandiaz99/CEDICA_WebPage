from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

def init_app(app):
    
    """
    INicializa la base de datos con la aplicacion Flask
    """
    
    db.init_app(app)
    with app.app_context(): 
        db.create_all()

    config(app)

    

    return app

def config(app):
    """
    Configuracion de hooks para la base de datos.
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

def reset():
    """
    resetea la base de datos
    """
    print("Eliminado base de datos..")
    db.drop_all()
    print("Creando base nuevamente..")
    #db.create_all()
    print("Listorti")