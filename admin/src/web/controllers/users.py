from src.core import auth
from flask import render_template
from flask import Blueprint
from src.web.handlers.auth import login_required

users_bp = Blueprint("users", __name__, url_prefix="/usuarios")

@users_bp.get("/")
@login_required
def index():
    users = auth.list_users()
    
    return render_template("users/index.html", users=users)