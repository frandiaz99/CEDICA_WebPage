from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.handlers.auth import check
from src.core.jinetes_amazonas import JineteAmazona
from src.core.cobros import Cobro
from src.core.database import db
from sqlalchemy import func, desc
from datetime import datetime

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")

def obtener_ranking_propuestas():
    ranking = (
        db.session.query(JineteAmazona.propuesta_trabajo, func.count(JineteAmazona.id).label("count"))
        .group_by(JineteAmazona.propuesta_trabajo)
        .order_by(desc("count"))
        .all()
    )
    return {propuesta: count for propuesta, count in ranking}

def obtener_personas_adeudan():
    personas_adeudan = (
        db.session.query(JineteAmazona, func.sum(Cobro.monto).label('total_deuda'))
        .join(Cobro)  
        .filter(Cobro.en_deuda == True)  
        .group_by(JineteAmazona.id)  
        .order_by(desc("total_deuda"))
        .all()
    )
    return personas_adeudan

def obtener_historico_cobros(jinete_id=None, fecha_inicio=None, fecha_fin=None):
    query = db.session.query(Cobro)
    
    if jinete_id:
        query = query.filter(Cobro.id_ja == jinete_id)
    if fecha_inicio:
        query = query.filter(Cobro.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Cobro.fecha_pago <= fecha_fin)

    return query.all()


@reportes_bp.get("/")
@check("reportes_index")
def index():
    ranking_propuestas = obtener_ranking_propuestas()
    personas_adeudan = obtener_personas_adeudan()
    jinetes = db.session.query(JineteAmazona).all()

 
    historico = None  


    jinete_id = request.args.get("jinete_id")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    if jinete_id and fecha_inicio and fecha_fin:
      
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
       
            historico = obtener_historico_cobros(jinete_id, fecha_inicio, fecha_fin)
        except ValueError:
            flash("Por favor, ingrese fechas válidas.", "error")

    print("Ranking propuestas: ", ranking_propuestas)
    print("Personas adeudan: ", personas_adeudan)
    print("Historico: ", historico)

    return render_template("reportes/reportes.html", 
                           jinetes = jinetes, 
                           ranking_propuestas=ranking_propuestas, 
                           personas=personas_adeudan,
                           historico=historico) 

