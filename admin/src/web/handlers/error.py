from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    code: int
    message: str
    description: str

def not_found_error(e):
    error= Error(404,"Not Found", "La URL solicitada no fue encontrada en el servidor")
    return render_template("error.html", error=error), 404

def unauthorized(e):
    error= Error(401,"Unauthorized", "Requiere iniciar sesión para acceder a esta página")
    return render_template("error.html", error=error), 401

def forbidden(e): 
    error = Error(403, "Forbidden" , "El servidor deniega el acceso solicitado")

    return render_template("error.html", error=error), 403

