from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import asc, desc
from src.core import equipo


equipo_bp = Blueprint('equipo', __name__, url_prefix='/equipo')

from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc
from src.core.equipo import Empleado


equipo_bp = Blueprint('equipo', __name__, url_prefix='/equipo')

@equipo_bp.get("/")
def index():
    registros_por_pagina = 5
    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')  # Por defecto 'nombre'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'nombre')
    pagina = int(request.args.get('pagina', 1, type=int))
    # Construir la query base
    query = equipo.Empleado.query
    
    # Filtrar según el campo seleccionado (filter_by)
    if search:
        if filter_by == 'nombre':
            query = query.filter(equipo.Empleado.nombre.ilike(f'%{search}%'))
        elif filter_by == 'apellido':
            query = query.filter(equipo.Empleado.apellido.ilike(f'%{search}%'))
        elif filter_by == 'dni':
            query = query.filter(equipo.Empleado.dni.ilike(f'%{search}%'))
        elif filter_by == 'email':
            query = query.filter(equipo.Empleado.email.ilike(f'%{search}%'))
        elif filter_by == 'profesion':
            query = query.filter(equipo.Empleado.profesion.ilike(f'%{search}%'))
    
    # Ordenar los resultados por el campo seleccionado y en el orden indicado
    if order == 'asc':
        query = query.order_by(asc(getattr(equipo.Empleado, filter_by)))
    else:
        query = query.order_by(desc(getattr(equipo.Empleado, filter_by)))
    
    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
    if order_prop == 'nombre':
        query = query.order_by(asc(equipo.Empleado.nombre)) if order == 'asc' else query.order_by(desc(equipo.Empleado.nombre))
    elif order_prop == 'apellido':
        query = query.order_by(asc(Empleado.apellido)) if order == 'asc' else query.order_by(desc(Empleado.apellido))
    elif order_prop == 'inserted_at':
        query = query.order_by(asc(Empleado.inserted_at)) if order == 'asc' else query.order_by(desc(Empleado.inserted_at))

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    
    empleados = pagination.items

    total_paginas = pagination.pages

    # Renderizar la plantilla y pasar los empleados y los parámetros
    return render_template(
        "equipo.html", 
        empleados=empleados, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop
    )
