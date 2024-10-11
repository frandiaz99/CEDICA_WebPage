from flask import current_app 
from datetime import timedelta

def documento_url(documento):
    client = current_app.storage.client

    if documento is None:
        return ""
    

    return client.presing_get_object("grupo49", documento)


def generar_url_firmada(bucket_name, file_name):

    client = current_app.storage.client

    # Cambiar la política de acceso a 'public-read' para el archivo
    url = client.presigned_get_object(bucket_name, file_name, expires=timedelta(hours=1))
    return url
