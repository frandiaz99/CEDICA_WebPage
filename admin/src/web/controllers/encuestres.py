from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import asc, desc

from src.core import encuestre


encuestre_bp = Blueprint('encuestre', __name__, url_prefix='/encuestre')

@encuestre_bp.get("/")
def index():
    print("Ruta /encuestre/ accedida")
    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')  # Por defecto 'nombre'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'nombre')
    
    # Construir la query base
    query = encuestre.Encuestre.query
    
    # Filtrar según el campo seleccionado (filter_by)
    if search:
        if filter_by == 'nombre':
            query = query.filter(encuestre.Encuestre.nombre.ilike(f'%{search}%'))
        elif filter_by == 'tipo_ja_asignado':
            query = query.filter(encuestre.Encuestre.tipo_ja_asignado.ilike(f'%{search}%'))
    
    # Ordenar los resultados por el campo seleccionado y en el orden indicado
    if order == 'asc':
        query = query.order_by(asc(getattr(encuestre.Encuestre, filter_by)))
    else:
        query = query.order_by(desc(getattr(encuestre.Encuestre, filter_by)))
    
    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
    if order_prop == 'nombre':
        query = query.order_by(asc(encuestre.Encuestre.nombre)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.nombre))
    elif order_prop == 'fecha_nacimineto':
        query = query.order_by(asc(encuestre.Encuestre.fecha_nacimiento)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.fecha_nacimiento))
    elif order_prop == 'fecha_ingreso':
        query = query.order_by(asc(encuestre.Encuestre.inserted_at)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.inserted_at))
    
    # Obtener los empleados filtrados y ordenados
    encuestres = query.all()
    
    # Renderizar la plantilla y pasar los empleados y los parámetros
    return render_template(
        "encuestre.html", 
        encuestres=encuestres, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop
    )
