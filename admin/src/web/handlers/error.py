from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    """
    Clase para estructurar la información de errores.
    
    Atributos:
        code (int): Código HTTP del error.
        message (str): Breve mensaje que describe el error.
        description (str): Detalle más amplio sobre el error.
    """
    code: int
    message: str
    description: str

def not_found_error(e):
    """
    Controlador para manejar errores 404 (Recurso no encontrado).
    
    Args:
        e (Exception): Excepción capturada.
    
    Returns:
        Tuple[str, int]: Renderiza una plantilla HTML con información del error 
        y el código de estado HTTP 404.
    """
    error = Error(404, "Not Found", "La URL solicitada no fue encontrada en el servidor")
    return render_template("error.html", error=error), 404

def unauthorized(e):
    """
    Controlador para manejar errores 401 (No autorizado).
    
    Args:
        e (Exception): Excepción capturada.
    
    Returns:
        Tuple[str, int]: Renderiza una plantilla HTML con información del error 
        y el código de estado HTTP 401.
    """
    error = Error(401, "Unauthorized", "Requiere iniciar sesión para acceder a esta página")
    return render_template("error.html", error=error), 401

def forbidden(e):
    """
    Controlador para manejar errores 403 (Prohibido).
    
    Args:
        e (Exception): Excepción capturada.
    
    Returns:
        Tuple[str, int]: Renderiza una plantilla HTML con información del error 
        y el código de estado HTTP 403.
    """
    error = Error(403, "Forbidden", "El servidor deniega el acceso solicitado")
    return render_template("error.html", error=error), 403
