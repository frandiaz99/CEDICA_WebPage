from src.core import board
from flask import render_template
from flask import Blueprint

bp = Blueprint("issue", __name__, url_prefix="/consultas")

@bp.get("/")
def index():
    issues = board.list_issues()
    
    return render_template("issues/index.html", issues=issues)

