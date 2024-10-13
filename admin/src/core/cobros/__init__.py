from .cobro import Cobro
from src.core.database import db


def create_cobro(**kwargs):
    cobro = Cobro(**kwargs)
    db.session.add(cobro)
    db.session.commit()

    return cobro

def list_cobro():
    cobros = Cobro.query.all()

    return cobros
