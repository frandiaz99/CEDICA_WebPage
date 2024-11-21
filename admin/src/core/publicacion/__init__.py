from sqlalchemy import desc
from .publicacion import Publicacion
from src.core.database import db


def create_publicacion(**kwargs):
    publicacion = Publicacion(**kwargs)
    db.session.add(publicacion)
    db.session.commit()

    return publicacion

def list_publicaciones():
    publicaciones = Publicacion.query.order_by(desc(Publicacion.fecha_publicacion)).all()

    return publicaciones
