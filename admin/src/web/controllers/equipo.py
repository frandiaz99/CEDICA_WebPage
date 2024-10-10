from flask import Blueprint, render_template, request, abort, flash, url_for, redirect, current_app
from sqlalchemy import asc, desc
from src.core.database import db
from datetime import datetime
equipo_bp = Blueprint('equipo', __name__, url_prefix='/equipo')

from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc
from src.core.equipo import Empleado, documento
from src.web.handlers.auth import check
import os 
equipo_bp = Blueprint('equipo', __name__, url_prefix='/equipo')

@equipo_bp.get("/")
@check('equipo_index')
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
    
    registros_por_pagina = 5
    query = documento.Documento.query
    pagina = request.args.get('pagina', 1, type=int)
    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    documentos = pagination.items
    total_paginas = pagination.pages
    
    return render_template('equipo/detalle_empleado.html', empleado=empleado, documentos=documentos, pagina=pagina, total_paginas=total_paginas)

@equipo_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("equipo_destroy")
def eliminar_empleado(id):
    # Buscar el encuestre por ID
    equipo_aux = Empleado.query.get_or_404(id)
    
    try:
        db.session.delete(equipo_aux)
        db.session.commit()

        flash('Equipo eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el equipo: {str(e)}', 'danger')
    return redirect(url_for('equipo.index')) 


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

@equipo_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
# @check("empleado_update")
def editar_empleado(id):
    empleado_aux = Empleado.query.get(id)
    if empleado_aux is None:
        abort(404) 

    if request.method == 'POST':
        # Obtener datos del formulario
        empleado_aux.nombre = request.form['nombre']
        empleado_aux.apellido = request.form['apellido']
        empleado_aux.dni = request.form['dni']
        empleado_aux.domicilio = request.form['domicilio']
        empleado_aux.email = request.form['email']
        empleado_aux.localidad = request.form['localidad']
        empleado_aux.telefono = request.form['telefono']
        empleado_aux.profesion = request.form['profesion']
        empleado_aux.puesto_laboral = request.form['puesto_laboral']
        empleado_aux.fecha_inicio = request.form['fecha_inicio']
        empleado_aux.fecha_cese = request.form.get('fecha_cese')
        empleado_aux.contacto_emergencia = request.form['contacto_emergencia']
        empleado_aux.obra_social = request.form['obra_social']
        empleado_aux.numero_afiliado = request.form['numero_afiliado']
        empleado_aux.condicion = request.form['condicion']
        empleado_aux.activo = True if request.form['activo'] == 'si' else False

        # Guardar cambios en la base de datos
        try:
            db.session.commit()
            flash('Los cambios se han guardado exitosamente.', 'success')
            return redirect(url_for('equipo.detalle_empleado', id=empleado_aux.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el empleado: {str(e)}', 'danger')
            return redirect(url_for('equipo.editar_empleado', id=id))
    
    return render_template(
        'equipo/editar_empleado.html', 
        empleado=empleado_aux, 
        fecha_hoy=datetime.today().date()
    )

@equipo_bp.route('/subir_documento', methods=['POST'])
def subir_documento():
    MAX_FILE_SIZE = 16 * 1024 * 1024

    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('equipo.detalle_empleado', id=request.form.get('empleado_id')))
    
    file = request.files['file']

    client = current_app.storage.client 

    file_size = os.fstat(file.fileno()).st_size
    
    if file_size > MAX_FILE_SIZE:
        flash('El archivo excede el tamaño máximo permitido (16MB)', 'error')
        return redirect(url_for('equipo.detalle_empleado', id=request.form.get('empleado_id')))
    
    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('equipo.detalle_empleado', id=request.form.get('empleado_id')))
    
    try:
        client.put_object(
            'grupo49',
            file.filename,
            file,
            file_size, 
            content_type=file.content_type
        )
        
        # Obtener el empleado asociado
        empleado_id = request.form.get('empleado_id')
        empleado_aux = Empleado.query.get(empleado_id)
        
        # Crear el documento y asociarlo al empleado
        nuevo_documento = documento.Documento(
            titulo=file.filename,
            url=f"{current_app.config['MINIO_SERVER']}/grupo49/{file.name}",
            empleado=empleado_aux
        )
        
        db.session.add(nuevo_documento)
        db.session.commit()
        
        flash('Documento subido exitosamente', 'success')
    except Exception as e:
        flash(f'Error al subir el documento: {str(e)}', 'error')
    
    return redirect(url_for('equipo.detalle_empleado', id=request.form.get('empleado_id')))
