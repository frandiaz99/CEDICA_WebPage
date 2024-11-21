import secrets
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash
from flask import url_for
from src.core import auth
from authlib.integrations.flask_client import OAuth
from flask import current_app as app
from src.core.config import config
from src.core.oauth import google
import random
import string

login_bp= Blueprint("auth",__name__, url_prefix="/auth")

@login_bp.get("/google-login")
def google_login():
    """
    Inicia el proceso de autenticación con Google.

    Este endpoint genera un `nonce` único, lo almacena en la sesión y redirige al usuario
    al flujo de autorización de Google para completar el inicio de sesión.

    Returns:
        Response: Redirección al flujo de autorización de Google.
    """
    # Genera un nonce único
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce

    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)


@login_bp.get("/google-callback")
def google_callback():
    """
    Procesa la respuesta de Google después de la autenticación.

    Verifica el token de acceso, valida el nonce, obtiene la información del usuario
    y realiza las siguientes acciones:
    - Crea un nuevo usuario si no existe.
    - Verifica si el registro ha sido aceptado y si el usuario está activo.
    - Inicia sesión si todas las verificaciones son exitosas.

    Returns:
        Response: Redirección a la página principal o a la pantalla de login con mensajes
        de error o éxito.
    """
    token = google.authorize_access_token()

    # Recuperar el nonce de la sesión
    expected_nonce = session.pop('nonce', None)
    if not expected_nonce:
        flash("Error de autenticación: Falta el nonce.", "error")
        return redirect(url_for("auth.login"))

    # Pasar el nonce al parse_id_token
    user_info = google.parse_id_token(token, nonce=expected_nonce)

    if not user_info:
        flash("Error al iniciar sesión con Google.", "error")
        return redirect(url_for("auth.login"))

    email = user_info['email']
    alias = user_info.get('name', email.split('@')[0])

    # Buscar usuario por correo
    user = auth.find_user_by_email(email)

    if not user:
        # Crear un nuevo usuario con una contraseña aleatoria
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        user = auth.create_user(alias=alias, email=email, password=random_password, aceptado_google=False)
    
    if not user.aceptado_google:
        flash("Esperando a que acepten tu registro por Google", "success")
        return redirect(url_for("auth.login"))
    
    if not user.activo:
        flash("Tu usuario ha sido bloqueado.", "error")
        return redirect(url_for("auth.login"))
    
    # Configurar la sesión del usuario
    session["user"] = user.email
    session["user_alias"] = user.alias
    flash("Inicio de sesión exitoso con Google", "success")
    return redirect(url_for("home"))


@login_bp.get("/")
def login():
    """
    Renderiza la página de inicio de sesión.
    
    Returns:
        Página HTML de inicio de sesión.
    """
    return render_template("auth/login.html")


@login_bp.post("/authenticate")
def authenticate():
    """
    Autentica al usuario mediante las credenciales proporcionadas.

    Obtiene los datos del formulario enviados en la solicitud (email y contraseña),
    verifica si el usuario existe y si las credenciales son correctas. Si son válidas,
    inicia una sesión para el usuario, de lo contrario, muestra mensajes de error.

    Returns:
        Redirección a la página de inicio de sesión o a la página principal del sistema.
    """
    params = request.form
    user = auth.check_user(params.get("email"), params.get("password"))

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))
    
    if not (user.activo):
        flash("Tu usuario ha sido bloqueado.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.email
    session["user_alias"] = user.alias 
    flash("¡La sesión se inició correctamente!", "success")
    return redirect(url_for("home"))


@login_bp.get("/logout")
def logout():
    """
    Cierra la sesión del usuario.

    Si hay una sesión activa, la elimina y borra los datos de sesión.
    Muestra un mensaje indicando que la sesión se ha cerrado correctamente.
    Si no hay una sesión activa, muestra un mensaje de error.

    Returns:
         Redirección a la página de inicio de sesión.
    """
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("¡La sesión se cerró correctamente!", "info")
    else:
        flash("No hay una sesión activa", "error")
    return redirect(url_for("auth.login"))
