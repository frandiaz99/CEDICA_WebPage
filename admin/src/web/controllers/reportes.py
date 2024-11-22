from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.handlers.auth import check
from src.core.jinetes_amazonas import JineteAmazona
from src.core.equipo import Empleado
from src.core.cobros import Cobro
from src.core.registro_pagos import Pago
from src.core.database import db
from sqlalchemy import func, desc, extract
from datetime import datetime
import calendar

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")

def obtener_ranking_propuestas(page=1, per_page=10):
    """
    Obtiene el ranking de propuestas de trabajo para los Jinetes y Amazonas, 
    basado en la cantidad de veces que cada propuesta se ha asociado.
    
    Args:
        page (int): Número de página de la paginación.
        per_page (int): Número de elementos por página.

    Returns:
        Pagination: Objeto de paginación con los resultados de las propuestas y sus conteos.
    """
    ranking = (
        db.session.query(JineteAmazona.propuesta_trabajo, func.count(JineteAmazona.id).label("count"))
        .group_by(JineteAmazona.propuesta_trabajo)
        .order_by(desc("count"))
        .paginate(page=page, per_page=per_page)
    )
    return ranking

def obtener_personas_adeudan(page=1, per_page=10):
    """
    Obtiene una lista de Jinetes y Amazonas que tienen deudas pendientes, 
    junto con el monto total adeudado por cada persona.

    Returns:
        list: Una lista de tuplas con el Jinete o Amazona y su monto total de deuda.
    """
    personas_adeudan = (
        db.session.query(JineteAmazona, func.sum(Cobro.monto).label('total_deuda'))
        .join(Cobro)  
        .filter(Cobro.en_deuda == True)  
        .group_by(JineteAmazona.id)  
        .order_by(desc("total_deuda"))
        .paginate(page=page, per_page=per_page)
    )
    return personas_adeudan

def obtener_historico_cobros(empleado_id=None, fecha_inicio=None, fecha_fin=None, page=1, per_page=10):
    """
    Obtiene el historial de cobros con opción de filtro por beneficiario y rango de fechas, 
    y con paginación.

    Args:
        empleado_id (int, optional): ID del Empleado (beneficiario) para filtrar los cobros.
        fecha_inicio (date, optional): Fecha de inicio para el filtro de cobros.
        fecha_fin (date, optional): Fecha de fin para el filtro de cobros.
        page (int, optional): Número de página para la paginación. Default es 1.
        per_page (int, optional): Cantidad de registros por página. Default es 10.

    Returns:
        Pagination: Objeto de paginación con los cobros que cumplen con los filtros especificados.
    """

    query = db.session.query(Cobro)

    if empleado_id:
        query = query.filter(Cobro.beneficiario_id == empleado_id)
    if fecha_inicio:
        query = query.filter(Cobro.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Cobro.fecha_pago <= fecha_fin)

    return query.paginate(page=page, per_page=per_page)

def obtener_becados():
    """
    Obtiene la cantidad de Jinetes y Amazonas que están becados y no becados.

    Returns:
        dict: Un diccionario con el conteo de becados y no becados.
    """
    becados_count = db.session.query(
        func.count(JineteAmazona.id).label("count")
    ).filter(JineteAmazona.becado == True).scalar()
    
    total_count = db.session.query(func.count(JineteAmazona.id)).scalar()
    no_becados_count = total_count - becados_count
    
    return {
        "becados": becados_count,
        "no_becados": no_becados_count
    }

def obtener_ingresos(criterio="anual", anio=None):
    """
    Obtiene el total de ingresos agrupados por mes o por año, según el criterio especificado.

    Args:
        criterio (str, optional): Criterio de agrupación de ingresos, puede ser 'anual' o 'mensual'. Default es 'anual'.
        anio (int, optional): Año específico para filtrar ingresos si el criterio es 'mensual'. Default es None.

    Returns:
        dict: Un diccionario con los ingresos agrupados por año o mes, según el criterio seleccionado.

    Raises:
        ValueError: Si el criterio no es 'anual' o 'mensual'.
    """
    if criterio == "mensual":
        if not anio:
            flash("Debe seleccionar un año para el criterio mensual.", "danger") 
            return redirect(url_for('users.index'))

        pagos = Pago.query.filter(extract('year', Pago.fecha_pago) == anio).all()
        ingresos_mensuales = {calendar.month_name[i]: 0 for i in range(1,13)}
        for pago in pagos:
            mes = pago.fecha_pago.month
            nombre_mes = calendar.month_name[mes]
            ingresos_mensuales[nombre_mes] += pago.monto
        return ingresos_mensuales
    
    elif criterio == "anual":
        if not anio:
            anio = datetime.now().year

        inicio_rango = anio - 5

        pagos = Pago.query.filter(extract('year', Pago.fecha_pago).between(inicio_rango, anio)).all()
        ingresos_anuales = {year: 0 for year in range(inicio_rango, anio + 1)}
        for pago in pagos:
            anio_pago = pago.fecha_pago.year
            ingresos_anuales[anio_pago] += pago.monto
        return ingresos_anuales
    else:
        raise ValueError("El criterio debe ser 'anual' o 'mensual'.")

def obtener_distribucion_discapacidad():
    """
    Obtiene la distribución de los tipos de discapacidad entre los Jinetes y Amazonas.

    Returns:
        dict: Un diccionario con los tipos de discapacidad ('Mental', 'Motora', 'Sensorial', 'Visceral') y su conteo correspondiente.
    """
    discapacidades = db.session.query(JineteAmazona.tipo_discapacidad, db.func.count()).group_by(JineteAmazona.tipo_discapacidad).all()
    
    discapacidad_data = {'Mental': 0, 'Motora': 0, 'Sensorial': 0, 'Visceral': 0}
    
    for discapacidad, count in discapacidades:
        if discapacidad in discapacidad_data:
            discapacidad_data[discapacidad] = count

    return discapacidad_data


@reportes_bp.get("/")
@check("reportes_show")
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Puedes ajustar esto según tus necesidades

    page_ranking = request.args.get('page_ranking', 1, type=int)
    ranking_propuestas = obtener_ranking_propuestas(page=page_ranking, per_page=per_page)

    page_adeuda = request.args.get('page_adeuda', 1, type=int)
    personas_adeudan = obtener_personas_adeudan(page=page_adeuda, per_page=per_page)
    empleados = db.session.query(Empleado).all()
    jinetes = db.session.query(JineteAmazona).all()
    becados_data = obtener_becados()
    discapacidad_data = obtener_distribucion_discapacidad()
    

    criterio = request.args.get('criterio', 'anual')
    anio = request.args.get('anio', type=int) if criterio == "mensual" else None

    if request.method == 'POST':
        criterio = request.form.get('criterio')
        if criterio == 'mensual':
            anio = request.form.get('anio', type=int)

    ingresos = obtener_ingresos(criterio, anio)


    empleado_id = request.args.get('empleado_id')
    jinete_id = request.args.get('jinete_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    page_historico = request.args.get('page_historico', 1, type=int)
    historico = obtener_historico_cobros(empleado_id, fecha_inicio, fecha_fin, page=page_historico, per_page=per_page)

    jinete_id = request.args.get("jinete_id")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    if jinete_id and fecha_inicio and fecha_fin:
      
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

            
        except ValueError:
            flash("Por favor, ingrese fechas válidas.", "error")

    print("Ranking propuestas: ", ranking_propuestas)
    print("Personas adeudan: ", personas_adeudan)
    print("Historico: ", historico)

    return render_template("reportes/reportes.html", 
                        empleados = empleados, 
                        jinetes = jinetes, 
                        ranking_propuestas=ranking_propuestas, 
                        personas=personas_adeudan,
                        becados_data=becados_data,
                        ingresos_data = ingresos,
                        discapacidad_data=discapacidad_data,
                        anio=anio,
                        criterio = criterio,
                        historico=historico
                        ) 

