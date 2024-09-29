from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    code: int
    message: str
    description: str

def not_found_error(e):
    error= Error(404,"Not Found", "The requested URL was not found on the server")
    return render_template("error.html", error=error), 404

def forbidden(e): 
    error = Error(403, "Forbidden" , "Usted no esta autorizado a acceder a esta pagina")

    return render_template("error.html", error=error), 403

