# src/core/equipo/__init__.py
from flask import Blueprint
from .empleado import Empleado
from src.core.database import db


def create_empleado(**kwargs):
    empleado = Empleado(**kwargs)
    db.session.add(empleado)
    db.session.commit()

    return empleado

def list_empleados():
    empleados = Empleado.query.all()

    return empleados
