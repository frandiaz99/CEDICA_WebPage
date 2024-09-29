from src.core.database import db

def assign_empleado_to_encuestre(encuestre, lista_empleados):

    for empleado in lista_empleados: 
        encuestre.entrenadores_conductores.append(empleado)

    db.session.add(encuestre)
    db.session.commit()

    return encuestre 