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
    user = auth.find_user_by_email_and_password(params["email"], params["password"])
    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))
    
    session["user"] = user.email
    flash("¡La sesión se inició correctamente")
    return redirect(url_for("issue.index"))

@login_bp.get("/logout")
def logout():
    pass