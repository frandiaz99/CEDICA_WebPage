from src.core.permiso import Permiso
from src.core.database import db

def create_permiso(**kwargs):
    permiso = Permiso(**kwargs)
    db.session.add(permiso)
    db.session.commit()

    return permiso