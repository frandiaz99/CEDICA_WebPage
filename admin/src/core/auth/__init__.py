from src.core.auth.user import User
from src.core.auth.rol import Rol
from src.core.database import db
from src.core.bcrypt import bcrypt

def list_users():
    users = User.query.all()
    return users

def list_roles():
    roles = Rol.query.all()
    return roles

def create_user(**kwargs):
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
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

def get_permissions(user):  
    permisos = [permiso.nombre for permiso in user.rol.permisos]

    return permisos

def find_user_by_email(email):
    user = User.query.filter_by(email=email).first()

    return user

def check_user(email, password):
    user = find_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

