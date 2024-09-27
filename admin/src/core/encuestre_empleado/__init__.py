from src.core.database import db

def assign_empleado_to_encuestre(empleado_id, encuestre_id):
    from src.core.encuestre import Encuestre #importacion diferida, previene la importacion circular 
    from src.core.equipo import Empleado

    empleado = Empleado.query.get(empleado_id)
    encuestre = Encuestre.query.get(encuestre_id)

    if empleado and encuestre:
        encuestre.entrenadores_conductores.append(empleado)
        db.session.commit()
        return encuestre
    return None