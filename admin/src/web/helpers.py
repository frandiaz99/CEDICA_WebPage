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

def inject_minio_image_url(storage, image_names):
    """
    Genera URLs presignadas para múltiples imágenes almacenadas en MinIO.
    
    :param storage: Instancia de la clase Storage que contiene el cliente de MinIO.
    :param image_names: Lista de nombres de archivos o rutas relativas dentro del bucket de MinIO.
    :return: Diccionario con las URLs presignadas de las imágenes.
    """
    bucket_name = 'grupo49'
    urls = {}

    # Itera sobre cada nombre de archivo para generar la URL presignada
    for image_name in image_names:
        urls[image_name] = storage.client.presigned_get_object(bucket_name, image_name)
    
    # Retorna el diccionario con las URLs presignadas para todas las imágenes
    return dict(minio_image_urls=urls)