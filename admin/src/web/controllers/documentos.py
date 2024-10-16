import os 

def checkDoc(titulo):
    
    """
    Verifica cuántos archivos en el directorio de descargas contienen el título especificado.

    :param titulo: El nombre o parte del nombre del archivo a buscar.
    :return: El número de archivos en el directorio de descargas que contienen el título.
    """

    ruta_descargas = "src/downloads"
    contador = 0
    for archivo in os.listdir(ruta_descargas):
        if titulo in archivo:
            contador += 1
    
    return contador

def generar_nombre(titulo_completo):
    
    """
    Genera un nombre único para un archivo si ya existen archivos con el mismo nombre en el directorio de descargas.
    Si ya existe un archivo con el nombre especificado, agrega un numero al nombre.

    :param titulo_completo: El nombre completo del archivo (incluyendo la extensión).
    :return: El nombre modificado del archivo si hay duplicados, o el nombre original si no hay conflictos.
    """

    base_nombre, extension = os.path.splitext(titulo_completo)
    cantidad = checkDoc(base_nombre)
    
    if cantidad == 0:
        return titulo_completo
    
   
    return f"{base_nombre}({cantidad}).{extension.lstrip('.')}"