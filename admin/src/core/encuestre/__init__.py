from src.core.encuestre.encuestre import Encuestre
from src.core.database import db

def list_users():
    users = Encuestre.query.all()

    return users

def create_encuestre(**kwargs):
    encuestre = Encuestre(**kwargs)
    db.session.add(encuestre)
    db.session.commit()

    return encuestre