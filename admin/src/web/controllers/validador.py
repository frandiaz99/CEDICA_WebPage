import re
from datetime import datetime

def validar_nombre(nombre):
    if not nombre:
        return False, "El nombre es requerido."
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nombre):
        return False, "El nombre solo debe contener letras y espacios."
    return True, ""

def validar_apellido(apellido):
    if not apellido:
        return False, "El apellido es requerido."
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', apellido):
        return False, "El apellido solo debe contener letras y espacios."
    return True, ""

def validar_dni(dni):
    if not dni:
        return False, "El DNI es requerido."
    if not re.match(r'^\d{8}$', dni):
        return False, "El DNI debe tener exactamente 8 dígitos."
    return True, ""

def validar_domicilio(domicilio):
    if not domicilio or len(domicilio.strip()) == 0:
        return False, "El domicilio es requerido."
    return True, ""

def validar_email(email):
    if not email:
        return False, "El correo electrónico es requerido."
    if not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email):
        return False, "El correo electrónico no es válido."
    return True, ""

def validar_localidad(localidad):
    if not localidad or len(localidad.strip()) == 0:
        return False, "La localidad es requerida."
    return True, ""

def validar_telefono(telefono):
    if not telefono:
        return False, "El teléfono es requerido."
    if not re.match(r'^\d{7,15}$', telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos."
    return True, ""

def validar_profesion(profesion):
    opciones_validas = [
        'Psicólogo/a', 'Psicomotricista', 'Médico/a', 'Kinesiólogo/a', 
        'Terapista Ocupacional', 'Psicopedagogo/a', 'Docente', 
        'Profesor', 'Fonoaudiólogo/a', 'Veterinario/a', 'Otro'
    ]
    if profesion not in opciones_validas:
        return False, f"La profesión debe ser una de las siguientes: {', '.join(opciones_validas)}."
    return True, ""

def validar_puesto_laboral(puesto_laboral):
    opciones_validas = [
        'Administrativo/a', 'Terapeuta', 'Conductor', 'Auxiliar de pista', 
        'Herrero', 'Veterinario', 'Entrenador de Caballos', 'Domador', 
        'Profesor de Equitación', 'Docente de Capacitación', 'Auxiliar de mantenimiento', 'Otro'
    ]
    if puesto_laboral not in opciones_validas:
        return False, f"El puesto laboral debe ser uno de los siguientes: {', '.join(opciones_validas)}."
    return True, ""


def validar_fecha_inicio(fecha_inicio):
    if not fecha_inicio:
        return False, "La fecha de inicio es requerida."
    try:
        fecha = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    except ValueError:
        return False, "La fecha de inicio no es válida. Formato esperado: AAAA-MM-DD."
    return True, ""

def validar_fecha_cese(fecha_cese, fecha_inicio):
    if not fecha_cese:
        return False, "La fecha de cese es requerida."
    try:
        fecha_cese_dt = datetime.strptime(fecha_cese, '%Y-%m-%d')
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        if fecha_inicio_dt > fecha_cese_dt:
            return False, "La fecha de inicio no puede ser mayor a la fecha de cese."
    except ValueError:
        return False, "La fecha de cese no es válida. Formato esperado: AAAA-MM-DD."
    return True, ""

def validar_contacto_emergencia(contacto_emergencia):
    if not contacto_emergencia or len(contacto_emergencia.strip()) == 0:
        return False, "El contacto de emergencia es requerido."
    return True, ""

def validar_obra_social(obra_social):
    if not obra_social or len(obra_social.strip()) == 0:
        return False, "La obra social es requerida."
    return True, ""

def validar_numero_afiliado(numero_afiliado):
    if not numero_afiliado:
        return False, "El número de afiliado es requerido."
    if not re.match(r'^\d+$', numero_afiliado):
        return False, "El número de afiliado debe contener solo dígitos."
    return True, ""

def validar_condicion(condicion):
    if condicion not in ['Voluntario', 'Personal Rentado']:
        return False, "La condición debe ser 'Voluntario' o 'Personal Rentado'."
    return True, ""

def validar_activo(activo):
    if activo not in ['Sí', 'No']:
        return False, "El estado activo debe ser 'Sí' o 'No'."
    return True, ""
