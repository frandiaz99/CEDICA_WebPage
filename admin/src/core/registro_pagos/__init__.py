# src/core/equipo/__init__.py
from flask import Blueprint
from .pago import Pago
from src.core.database import db


def create_pago(**kwargs):
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()

    return pago

def list_pagos():
    pagos = Pago.query.all()

    return pagos
