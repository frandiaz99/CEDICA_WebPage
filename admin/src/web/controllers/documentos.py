import os 

def checkDoc(titulo):
    
    ruta_descargas = "src/downloads"
    

    contador = 0
    for archivo in os.listdir(ruta_descargas):
        if titulo in archivo:
            contador += 1
    
    return contador

def generar_nombre(titulo_completo):
    
    base_nombre, extension = os.path.splitext(titulo_completo)
   
    cantidad = checkDoc(base_nombre)
    
    if cantidad == 0:
        return titulo_completo
    
   
    return f"{base_nombre}({cantidad}).{extension.lstrip('.')}"