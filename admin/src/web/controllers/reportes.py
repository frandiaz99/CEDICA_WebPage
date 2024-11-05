from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.handlers.auth import check
from src.core.jinetes_amazonas import JineteAmazona
from src.core.cobros import Cobro
from src.core.registro_pagos import Pago
from src.core.database import db
from sqlalchemy import func, desc, extract
from datetime import datetime
import calendar

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

def obtener_becados():
    # Query to get the count of scholarship recipients
    becados_count = db.session.query(
        func.count(JineteAmazona.id).label("count")
    ).filter(JineteAmazona.becado == True).scalar()
    
    # Total count of all Jinetes y Amazonas
    total_count = db.session.query(func.count(JineteAmazona.id)).scalar()
    no_becados_count = total_count - becados_count
    
    return {
        "becados": becados_count,
        "no_becados": no_becados_count
    }

# Función para obtener los ingresos
def obtener_ingresos(criterio="anual", anio=None):
    if criterio == "mensual" and anio:
        pagos = Pago.query.filter(extract('year', Pago.fecha_pago) == anio).all()
        ingresos_mensuales = {}
        for pago in pagos:
            mes = pago.fecha_pago.month
            nombre_mes = calendar.month_name[mes]
            ingresos_mensuales[nombre_mes] = ingresos_mensuales.get(nombre_mes, 0) + pago.monto
        return ingresos_mensuales
    elif criterio == "anual":
        pagos = Pago.query.all()
        ingresos_anuales = {}
        for pago in pagos:
            anio_pago = pago.fecha_pago.year
            ingresos_anuales[anio_pago] = ingresos_anuales.get(anio_pago, 0) + pago.monto
        return ingresos_anuales
    else:
        raise ValueError("El criterio debe ser 'anual' o 'mensual'.")

def obtener_distribucion_discapacidad():
    # Contar la cantidad de cada tipo de discapacidad
    discapacidades = db.session.query(JineteAmazona.tipo_discapacidad, db.func.count()).group_by(JineteAmazona.tipo_discapacidad).all()
    
    # Inicializamos un diccionario para almacenar los resultados
    discapacidad_data = {'Mental': 0, 'Motora': 0, 'Sensorial': 0, 'Visceral': 0}
    
    # Llenamos el diccionario con los datos de la consulta
    for discapacidad, count in discapacidades:
        if discapacidad in discapacidad_data:
            discapacidad_data[discapacidad] = count

    return discapacidad_data

@reportes_bp.get("/")
@check("reportes_index")
def index():
    ranking_propuestas = obtener_ranking_propuestas()
    personas_adeudan = obtener_personas_adeudan()
    jinetes = db.session.query(JineteAmazona).all()
    becados_data = obtener_becados()
    discapacidad_data = obtener_distribucion_discapacidad()

    # Obtener el criterio (por defecto es anual)
    criterio = request.args.get('criterio', 'anual')
    anio = request.args.get('anio', type=int) if criterio == "mensual" else None

    # Si se envió el formulario, actualizamos el criterio y el año
    if request.method == 'POST':
        criterio = request.form.get('criterio')
        if criterio == 'mensual':
            anio = request.form.get('anio', type=int)

    # Obtener los ingresos según el criterio
    ingresos = obtener_ingresos(criterio, anio)
    

 
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
                        becados_data=becados_data,
                        ingresos_data = ingresos,
                        discapacidad_data=discapacidad_data,
                        anio=anio,
                        criterio = criterio,
                        historico=historico) 

