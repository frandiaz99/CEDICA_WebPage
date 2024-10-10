from flask import Blueprint, render_template, request, abort, flash, url_for, redirect
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
    query = Empleado.query

    # Filtrar según el campo seleccionado (filter_by)
    if search:
        if filter_by == 'nombre':
            query = query.filter(Empleado.nombre.ilike(f'%{search}%'))
        elif filter_by == 'apellido':
            query = query.filter(Empleado.apellido.ilike(f'%{search}%'))
        elif filter_by == 'dni':
            query = query.filter(Empleado.dni.ilike(f'%{search}%'))
        elif filter_by == 'email':
            query = query.filter(Empleado.email.ilike(f'%{search}%'))
        elif filter_by == 'profesion':
            query = query.filter(Empleado.profesion.ilike(f'%{search}%'))

    # Adicionalmente, ordenar por order_prop si es distinto de filter_by
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(Empleado, order_prop)))
        else:
            query = query.order_by(desc(getattr(Empleado, order_prop)))

    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
    if order_prop == 'nombre':
        query = query.order_by(asc(Empleado.nombre)) if order == 'asc' else query.order_by(desc(Empleado.nombre))
    elif order_prop == 'apellido':
        query = query.order_by(asc(Empleado.apellido)) if order == 'asc' else query.order_by(desc(Empleado.apellido))
    elif order_prop == 'inserted_at':
        query = query.order_by(asc(Empleado.inserted_at)) if order == 'asc' else query.order_by(desc(Empleado.inserted_at))

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    
    empleados = pagination.items

    total_paginas = pagination.pages

    # Renderizar la plantilla y pasar los empleados y los parámetros
    return render_template(
        "equipo/equipo.html", 
        empleados=empleados, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas
    )


@equipo_bp.route('/detalle/<int:id>', methods=['GET'])
def detalle_empleado(id):
    empleado = Empleado.query.get(id)
    if empleado is None:
        abort(404)  # error 404 si no se encuentra el empleado
    return render_template('equipo/detalle_empleado.html', empleado=empleado)


@equipo_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_empleado():
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        email = request.form.get('email')
        profesion = request.form.get('profesion')
        puesto_laboral = request.form.get('puesto_laboral')

        if not (nombre and apellido and dni and email and profesion and puesto_laboral):
            flash('Faltan completar campos', 'danger')
            return redirect(url_for('equipo.registrar_empleado'))

        # Crear el objeto Empleado
        nuevo_empleado = Empleado(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            profesion=profesion,
            puesto_laboral=puesto_laboral
        )

        try:
            # Subir a la base de datos
            db.session.add(nuevo_empleado)
            db.session.commit()
            flash('Empleado registrado exitosamente', 'success')
            return redirect(url_for('equipo.detalle_empleado', id=nuevo_empleado.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el empleado: {str(e)}', 'danger')
            return redirect(url_for('equipo.registrar_empleado'))

    return render_template('equipo/registrar_empleado.html')
