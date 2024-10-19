from .jinetes_amazonas import JineteAmazona
from src.core.database import db


def create_jinete_amazona(**kwargs):
    jinete_amazona = JineteAmazona(**kwargs)
    db.session.add(jinete_amazona)
    db.session.commit()

    return jinete_amazona

def list_jinetes_amazonas():
    jinetes_amazonas = JineteAmazona.query.all()

    return jinetes_amazonas