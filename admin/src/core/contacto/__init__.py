# src/core/equipo/__init__.py
from flask import Blueprint
from .contacto import Contacto
from src.core.database import db


def create_contacto(**kwargs):
    contacto = Contacto(**kwargs)
    db.session.add(contacto)
    db.session.commit()

    return contacto

def list_contactos():
    contactos = Contacto.query.all()

    return contactos
