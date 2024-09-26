
from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc
from src.core import equipo

equipo_bp = Blueprint('equipo', __name__, url_prefix='/equipo')

@equipo_bp.get("/")
def index():
    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')  # Por defecto 'nombre'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'nombre')
    
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
    
    # Ordenar los resultados por el campo seleccionado y en el orden indicado --Esto hacia que se ordene por el campo de filtro pero no el de ordenar
    #if order == 'asc':
    #    query = query.order_by(asc(getattr(equipo.Empleado, filter_by)))
    #else:
    #    query = query.order_by(desc(getattr(equipo.Empleado, filter_by)))
    
    # Adicionalmente, ordenar por order_prop si es distinto de filter_by
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(equipo.Empleado, order_prop)))
        else:
            query = query.order_by(desc(getattr(equipo.Empleado, order_prop)))


    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
    if order_prop == 'nombre':
        query = query.order_by(asc(equipo.Empleado.nombre)) if order == 'asc' else query.order_by(desc(equipo.Empleado.nombre))
    elif order_prop == 'apellido':
        query = query.order_by(asc(equipo.Empleado.apellido)) if order == 'asc' else query.order_by(desc(equipo.Empleado.apellido))
    elif order_prop == 'inserted_at':
        query = query.order_by(asc(equipo.Empleado.inserted_at)) if order == 'asc' else query.order_by(desc(equipo.Empleado.inserted_at))
    
    # Obtener los empleados filtrados y ordenados
    empleados = query.all()
    
    # Renderizar la plantilla y pasar los empleados y los parámetros
    return render_template(
        "equipo.html", 
        empleados=empleados, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop
    )
