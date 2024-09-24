from .encuestre import Encuestre
from src.core.database import db
from flask import Blueprint

def create_encuestre(**kwargs):
    encuestre = Encuestre(**kwargs)
    db.session.add(encuestre)
    db.session.commit()

    return encuestre

def list_encustres():
    encustres = Encuestre.query.all()

    return encustres

def assign_empleado(empleado, encuestre):
    empleado.encuestr = encuestre
    db.session.add(encuestre)
    db.session.commit()

    return encuestre