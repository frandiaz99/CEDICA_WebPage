from minio import Minio

class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None: 
            self.init_app(app)

    def init_app(self, app):
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)

        # Inicializa cliente minio
        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        #Asjunta cliente al contexto de al App
        app.storage = self

        return app
    
    @property
        
    def client(self):
        """obtener el cliente de minio"""
        return self._client
    
    @client.setter
    def client(self, value):
        """ Propiedad setter para permitir reasignar el cliente a miniO """
        self._client = value
    
storage = Storage()




