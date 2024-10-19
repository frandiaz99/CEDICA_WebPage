from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash
from flask import url_for
from src.core import auth

login_bp= Blueprint("auth",__name__, url_prefix="/auth")

@login_bp.get("/")
def login():
    return render_template("auth/login.html")

@login_bp.post("/authenticate")
def authenticate():
    params = request.form
    user = auth.check_user(params["email"], params["password"])

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))
    
    if not (user.activo):
        flash("Tu usuario ha sido bloqueado.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.email
    session["user_alias"] = user.alias 
    flash("¡La sesión se inició correctamente","success")
    return redirect(url_for("home"))

@login_bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("¡La sesión se cerró correctamente!", "info")
    else:
        flash("No hay una sesión activa", "error")
    return redirect(url_for("auth.login"))