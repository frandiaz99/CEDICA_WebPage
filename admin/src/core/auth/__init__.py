from src.core.auth.user import User
from src.core.auth.rol import Rol
from src.core.database import db

def list_users():
    users = User.query.all()
    return users

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def create_rol(**kwargs):
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()

    return rol

def assign_rol(user, rol):
    user.rol = rol
    db.session.add(user)
    db.session.commit()

    return user