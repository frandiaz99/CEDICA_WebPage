from functools import wraps
from flask import session 
from flask import abort 
from src.core import auth 

def is_authenticated(session):
    """
    Verifica si el usuario está autenticado.

    Args:
        session (dict): Diccionario que contiene los datos de la sesión actual.

    Returns:
        bool: True si el usuario está autenticado, False de lo contrario.
    """
    return session.get("user") is not None


def check_permission(session, permission):
    """
    Verifica si el usuario tiene un permiso específico.

    Args:
        session (dict): Diccionario que contiene los datos de la sesión actual.
        permission (str): El permiso requerido a verificar.

    Returns:
        bool: True si el usuario existe y tiene el permiso, False de lo contrario.
    """
    user_email = session.get("user")
    user = auth.find_user_by_email(user_email)
    permissions = auth.get_permissions(user)

    print("User:", user_email)
    print("Requested Permission:", permission)

    return user is not None and permission in permissions


def login_required(func):
    """
    Decorador que requiere que el usuario esté autenticado para acceder a una vista.

    Si el usuario no está autenticado, retorna un error 401 (no autorizado).

    Args:
        func (function): La función a la que se aplicará el decorador.

    Returns:
        function: La función decorada que incluye la verificación de autenticación.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)

        return func(*args, **kwargs)

    return wrapper


def check(permission):
    """
    Decorador que verifica si el usuario tiene un permiso específico para acceder a una vista.

    Si el usuario no tiene el permiso requerido, retorna un error 403 (prohibido).

    Args:
        permission (str): El permiso que se requiere para acceder a la función decorada.

    Returns:
        function: La función decorada que incluye la verificación de permisos.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not check_permission(session, permission):
                return abort(403)

            return f(*args, **kwargs)

        return wrapper
    
    return decorator
