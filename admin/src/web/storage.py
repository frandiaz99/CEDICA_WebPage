from minio import Minio

class Storage:
    """
    Clase para gestionar la interacción con el cliente de MinIO.
    """

    def __init__(self, app=None):
        """
        Inicializa una instancia de la clase Storage. Si se pasa una aplicación Flask, 
        se inicializa el cliente MinIO inmediatamente.

        :param app: (opcional) Aplicación Flask con configuración para MinIO.
        """
        self._client = None
        if app is not None: 
            self.init_app(app)

    def init_app(self, app):
        """
        Inicializa el cliente de MinIO utilizando los parámetros de configuración
        de la aplicación Flask.

        :param app: Aplicación Flask con las configuraciones necesarias para MinIO.
        :return: La aplicación Flask modificada con el atributo `storage`.
        """
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE")

        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        app.storage = self

        return app
    
    @property
        
    def client(self):
        """
        Devuelve el cliente de MinIO que ha sido inicializado.

        :return: Instancia de MinIO.
        """
        return self._client
    
    @client.setter
    def client(self, value):
        """
        Asigna un nuevo valor al cliente de MinIO, permitiendo cambiarlo si es necesario.

        :param value: Nueva instancia de MinIO.
        """
        self._client = value


    
storage = Storage()




