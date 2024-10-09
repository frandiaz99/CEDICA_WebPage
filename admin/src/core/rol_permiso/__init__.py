from src.core.database import db

def assign_permisos_to_rol(rol, lista_permisos):

    for permiso in lista_permisos: 
        rol.permisos.append(permiso)

    db.session.add(rol)
    db.session.commit()

    return rol 