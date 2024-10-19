import re
from datetime import datetime
from src.core.equipo import Empleado

def validar_string(string):
    """
    Verifica si el string contiene solo letras (incluyendo acentos) y espacios.

    Args:
        string (str): El string a validar.

    Returns:
        bool: True si el string es válido, False en caso contrario.
    """
    return bool(re.match(r'^[A-Za-zÀ-ÿ\s]+$', string))


def validar_vacio(string):
    """
    Verifica si el string está vacío o contiene solo espacios en blanco.

    Args:
        string (str): El string a validar.

    Returns:
        bool: True si el string no está vacío, False en caso contrario.
    """
    return bool(string and len(string.strip()) > 0)


def validar_nombre(nombre):
    """
    Valida si el nombre es válido.

    Args:
        nombre (str): El nombre a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not nombre:
        return False, "El nombre es requerido."
    if not validar_string(nombre):
        return False, "El nombre solo debe contener letras y espacios."
    return True, ""


def validar_apellido(apellido):
    """
    Valida si el apellido es válido.

    Args:
        apellido (str): El apellido a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not apellido:
        return False, "El apellido es requerido."
    if not validar_string(apellido):
        return False, "El apellido solo debe contener letras y espacios."
    return True, ""


def validar_dni(dni):
    """
    Valida si el DNI es válido (debe contener exactamente 8 dígitos).

    Args:
        dni (str): El DNI a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not dni:
        return False, "El DNI es requerido."
    if not re.match(r'^\d{8}$', dni):
        return False, "El DNI debe tener exactamente 8 dígitos."
    return True, ""


def validar_domicilio(domicilio):
    """
    Verifica si el domicilio no está vacío.

    Args:
        domicilio (str): El domicilio a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not validar_vacio(domicilio):
        return False, "El domicilio es requerido."
    return True, ""


def validar_email(email):
    """
    Valida el formato de un correo electrónico.

    Args:
        email (str): El correo a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not email:
        return False, "El correo electrónico es requerido."
    if not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email):
        return False, "El correo electrónico no es válido."
    return True, ""


def validar_localidad(localidad):
    """
    Verifica si la localidad no está vacía.

    Args:
        localidad (str): La localidad a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    if not validar_vacio(localidad):
        return False, "La localidad es requerida."
    return True, ""


def validar_telefono(telefono):
    """
    Valida si el teléfono tiene entre 7 y 15 dígitos.

    Args:
        telefono (str): El teléfono a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not telefono:
        return False, "El teléfono es requerido."
    if not re.match(r'^\d{7,15}$', telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos."
    return True, ""


def validar_profesion(profesion):
    """
    Verifica si la profesión es una opción válida.

    Args:
        profesion (str): La profesión a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    opciones_validas = [
        'Psicólogo/a', 'Psicomotricista', 'Médico/a', 'Kinesiólogo/a', 
        'Terapista Ocupacional', 'Psicopedagogo/a', 'Docente', 
        'Profesor', 'Fonoaudiólogo/a', 'Veterinario/a', 'Otro'
    ]
    if profesion not in opciones_validas:
        return False, f"La profesión debe ser una de las siguientes: {', '.join(opciones_validas)}."
    return True, ""


def validar_puesto_laboral(puesto_laboral):
    """
    Verifica si el puesto laboral es una opción válida.

    Args:
        puesto_laboral (str): El puesto laboral a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    opciones_validas = [
        'Administrativo/a', 'Terapeuta', 'Conductor', 'Auxiliar de pista', 
        'Herrero', 'Veterinario', 'Entrenador de Caballos', 'Domador', 
        'Profesor de Equitación', 'Docente de Capacitación', 'Auxiliar de mantenimiento', 'Otro'
    ]
    if puesto_laboral not in opciones_validas:
        return False, f"El puesto laboral debe ser uno de los siguientes: {', '.join(opciones_validas)}."
    return True, ""


def validar_fecha_inicio(fecha_inicio):
    """
    Valida si la fecha de inicio es válida y está en el formato correcto.

    Args:
        fecha_inicio (str): La fecha de inicio a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    if not fecha_inicio:
        return False, "La fecha de inicio es requerida."
    try:
        datetime.strptime(fecha_inicio, '%Y-%m-%d')
    except ValueError:
        return False, "La fecha de inicio no es válida. Formato esperado: AAAA-MM-DD."
    return True, ""


def validar_fecha_cese(fecha_cese, fecha_inicio):
    """
    Valida si la fecha de cese es válida y no es anterior a la fecha de inicio.

    Args:
        fecha_cese (str): La fecha de cese a validar.
        fecha_inicio (str): La fecha de inicio a comparar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
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
    """
    Verifica si el contacto de emergencia no está vacío.

    Args:
        contacto_emergencia (str): El contacto de emergencia a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not validar_vacio(contacto_emergencia):
        return False, "El contacto de emergencia es requerido."
    return True, ""


def validar_obra_social(obra_social):
    """
    Verifica si la obra social no está vacía.

    Args:
        obra_social (str): La obra social a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    if not validar_vacio(obra_social):
        return False, "La obra social es requerida."
    return True, ""


def validar_numero_afiliado(numero_afiliado):
    """
    Verifica si el número de afiliado contiene solo dígitos.

    Args:
        numero_afiliado (str): El número de afiliado a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not numero_afiliado:
        return False, "El número de afiliado es requerido."
    if not re.match(r'^\d+$', numero_afiliado):
        return False, "El número de afiliado debe contener solo dígitos."
    return True, ""


def validar_condicion(condicion):
    """
    Verifica si la condición es 'Voluntario' o 'Personal Rentado'.

    Args:
        condicion (str): La condición a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    if condicion not in ['Voluntario', 'Personal Rentado']:
        return False, "La condición debe ser 'Voluntario' o 'Personal Rentado'."
    return True, ""


def validar_activo(activo):
    """
    Verifica si el estado activo es 'Sí' o 'No'.

    Args:
        activo (str): El estado activo a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if activo not in ['Sí', 'No']:
        return False, "El estado activo debe ser 'Sí' o 'No'."
    return True, ""


def validar_tipo_pago(tipo_pago):
    """
    Verifica si el tipo de pago es uno de los válidos.

    Args:
        tipo_pago (str): El tipo de pago a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    tipos_validos = ['honorarios', 'proveedor', 'gastos varios', 'efectivo', 'debito', 'credito']
    if tipo_pago in tipos_validos:
        return True, ""
    return False, "Tipo de pago no es válido."


def validar_monto(monto):
    """
    Verifica si el monto es un número positivo.

    Args:
        monto (str): El monto a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    try:
        monto_float = float(monto)
        if monto_float > 0:
            return True, ""
        return False, "El monto debe ser un número positivo."
    except ValueError:
        return False, "El monto ingresado no es un número válido."


def validar_fecha_pago(fecha_pago_str):
    """
    Valida si la fecha de pago es válida y no es futura.

    Args:
        fecha_pago_str (str): La fecha de pago a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    try:
        fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d')
        if fecha_pago <= datetime.today():
            return True, ""
        return False, "La fecha de pago no puede ser futura."
    except ValueError:
        return False, "La fecha de pago no tiene un formato válido. Debe ser YYYY-MM-DD."


def validar_descripcion(descripcion):
    """
    Verifica si la descripción no está vacía.

    Args:
        descripcion (str): La descripción a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    if validar_vacio(descripcion):
        return True, ""
    return False, "La descripción no puede estar vacía."


def validar_beneficiario(beneficiario):
    """
    Valida si el ID del beneficiario es un número.

    Args:
        beneficiario (str): El ID del beneficiario a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if beneficiario and beneficiario.isdigit():
        return True, ""
    return False, "El ID del beneficiario no es válido."


def validar_fecha_ingreso(fecha_ingreso_str):
    """
    Valida si la fecha de ingreso es válida y no es futura.

    Args:
        fecha_ingreso_str (str): La fecha de ingreso a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    try:
        fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d')
        if fecha_ingreso <= datetime.today():
            return True, ""
        return False, "La fecha de ingreso no puede ser futura."
    except ValueError:
        return False, "La fecha de ingreso no tiene un formato válido. Debe ser YYYY-MM-DD."
    
def validar_fecha_nacimiento(fecha_nacimiento_str):
    """
    Valida si la fecha de nacimiento es válida y no es futura.

    Args:
        fecha_nacimiento_str (str): La fecha de nacimiento a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válida y un mensaje de error.
    """
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
        if fecha_nacimiento <= datetime.today():
            return True, ""
        return False, "La fecha de nacimiento no puede ser futura."
    except ValueError:
        return False, "La fecha de nacimiento no tiene un formato válido. Debe ser YYYY-MM-DD."
    

def validar_sexo(sexo):
    """Valida que el sexo sea uno de los valores permitidos.
    
    Arrgs: 
        sexo (str): sexo a validar
    
    Returns:
        turple: (bool,str) Retorna un booleano indicando si es válida y un mensaje de error.
    
    """
    sexos_permitidos = ['masculino', 'femenino']
    if sexo not in sexos_permitidos:
        return False, f"El sexo debe ser uno de los siguientes: {', '.join(sexos_permitidos)}."
    return True, ""

def validar_raza(raza):
    """
    Valida si la raza es válido.

    Args:
        raza (str): La raza a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not raza:
        return False, "La raza del caballo es requerido."
    if not validar_string(raza):
        return False, "La raza del caballo solo debe contener letras y espacios."
    return True, ""

def validar_pelaje(pelaje):
    """
    Valida si el pelaje es válido.

    Args:
        pelaje (str): El pelaje a validar.

    Returns:
        tuple: (bool, str) Retorna un booleano indicando si es válido y un mensaje de error.
    """
    if not pelaje:
        return False, "El pelaje del caballo es requerido."
    if not validar_string(pelaje):
        return False, "El pelaje del caballo solo debe contener letras y espacios."
    return True, ""

def validar_compra_donacion(compra_donacion):
    """Valida que el tipo (compra/donacion) sea uno de los valores permitidos.
    
    Args: 
        compra_donacion(str): tipo a validar
    
    Returns:
        turple: (bool,str) Retorna un booleano indicando si es válida y un mensaje de error.
    
    """
    tipos = ['compra', 'donacion']
    if compra_donacion not in tipos:
        return False, f"El tipo debe ser uno de los siguientes: {', '.join(tipos)}."
    return True, ""

def validar_tipo_ja_asignado(tipo_ja_asignado):
    """Valida que el tipo de J&A asignado sea uno de los valores permitidos.
    
    Args: 
        tipo_ja_asignado(str): tipo a validar
    
    Returns:
        turple: (bool,str) Retorna un booleano indicando si es válida y un mensaje de error.
    
    """
    tipos_permitidos = ['Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación']
    if tipo_ja_asignado not in tipos_permitidos:
        return False, f"El tipo de J&A asignado debe ser uno de los siguientes: {', '.join(tipos_permitidos)}."
    return True, ""

def validar_entrenadores_conductores(entrenadores_conductores_ids):
    """Valida que los entrenadores/condcutores formen parte del equipo.
    
    Args: 
        entrenadores_cnductores_ids(int): tipo a validar
    
    Returns:
        turple: (bool,str) Retorna un booleano indicando si es válida y un mensaje de error.
    
    """
    entrenadores_conductores = Empleado.query.filter(Empleado.id.in_(entrenadores_conductores_ids), Empleado.puesto_laboral.in_(['Entrenador de caballos', 'Conductor'])).all()
    
    if not entrenadores_conductores:
        return False, "Debe seleccionar entrenadores o conductores válidos."
    return True, ""

# Validar sede asignada (si fuera necesario)
def validar_sede_asignada(sede_asignada):
    """Valida la sede asignada sea una de las permitidas.
    
    Args: 
        sede_asignada(str): tipo a validar
    
    Returns:
        turple: (bool) Retorna un booleano indicando si es válida y un mensaje de error.
    
    """
    sedes_permitidas = ['CASJ', 'HLP', ]
    if sede_asignada not in sedes_permitidas:
        return False, f"La sede asignada debe ser uno de los siguientes: {', '.join(sedes_permitidas)}."
    return True, ""