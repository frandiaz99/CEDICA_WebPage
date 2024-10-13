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
from src.web.controllers.validador import (
    validar_nombre, validar_apellido, validar_dni, validar_domicilio, 
    validar_email, validar_localidad, validar_telefono, validar_profesion, 
    validar_puesto_laboral, validar_fecha_inicio, validar_fecha_cese, 
    validar_contacto_emergencia, validar_obra_social, validar_numero_afiliado, 
    validar_condicion, validar_activo
)
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
        elif filter_by == 'puesto':
            query = query.filter(Empleado.puesto_laboral.ilike(f'%{search}%'))

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
@check("equipo_show")
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
    empleado_aux = Empleado.query.get_or_404(id)
    
    try:
        db.session.delete(empleado_aux)
        db.session.commit()

        flash('Empleado eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el empleado: {str(e)}', 'danger')
    return redirect(url_for('equipo.index')) 


@equipo_bp.route('/registrar', methods=['GET', 'POST'])
@check("equipo_new")
def registrar_empleado():
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        domicilio = request.form.get('domicilio')
        email = request.form.get('email')
        localidad = request.form.get('localidad')
        telefono = request.form.get('telefono')
        profesion = request.form.get('profesion')
        puesto_laboral = request.form.get('puesto_laboral')
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_cese_str = request.form.get('fecha_cese')
        contacto_emergencia = request.form.get('contacto_emergencia')
        obra_social = request.form.get('obra_social')
        numero_afiliado = request.form.get('numero_afiliado')
        condicion = request.form.get('condicion')
        activo = request.form.get('activo')

        # Validar que los campos requeridos no estén vacíos
        if not (nombre and apellido and dni and domicilio and email and localidad and telefono and profesion and puesto_laboral and fecha_inicio_str and fecha_cese_str and contacto_emergencia and condicion and activo):
            flash('Faltan completar campos obligatorios', 'danger')
            return redirect(url_for('equipo.registrar_empleado'))

        dni_aux = Empleado.query.filter_by(dni=dni).first()
        if dni_aux:
            flash('El DNI ingresado ya se encuentra registrado.', 'danger')
            return redirect(url_for('equipo.registrar_empleado'))
        # Validadores
        validadores = [
            (validar_nombre, [nombre]),
            (validar_apellido, [apellido]),
            (validar_dni, [dni]),
            (validar_domicilio, [domicilio]),
            (validar_email, [email]),
            (validar_localidad, [localidad]),
            (validar_telefono, [telefono]),
            (validar_profesion, [profesion]),
            (validar_puesto_laboral, [puesto_laboral]),
            (validar_fecha_inicio, [fecha_inicio_str]),
            (validar_fecha_cese, [fecha_cese_str, fecha_inicio_str]),  # Aquí también se pasa la fecha de inicio
            (validar_contacto_emergencia, [contacto_emergencia]),
            (validar_obra_social, [obra_social]),
            (validar_numero_afiliado, [numero_afiliado]),
            (validar_condicion, [condicion]),
            (validar_activo, [activo])
        ]

        # Ejecutar validaciones
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)  # Desempaquetamos los argumentos
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('equipo.registrar_empleado'))  # Redirige si hay error

        # Crear el objeto Empleado
        nuevo_empleado = Empleado(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            domicilio=domicilio,
            email=email,
            localidad=localidad,
            telefono=telefono,
            profesion=profesion,
            puesto_laboral=puesto_laboral,
            fecha_inicio=datetime.strptime(fecha_inicio_str, '%Y-%m-%d'),
            fecha_cese=datetime.strptime(fecha_cese_str, '%Y-%m-%d'),
            contacto_emergencia=contacto_emergencia,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            condicion=condicion,
            activo=(activo == 'Sí')
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
@check("equipo_update")
def editar_empleado(id):
    empleado_aux = Empleado.query.get(id)
    if empleado_aux is None:
        abort(404) 

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        domicilio = request.form['domicilio']
        email = request.form['email']
        localidad = request.form['localidad']
        telefono = request.form['telefono']
        profesion = request.form['profesion']
        puesto_laboral = request.form['puesto_laboral']
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_cese_str = request.form.get('fecha_cese')
        contacto_emergencia = request.form['contacto_emergencia']
        obra_social = request.form['obra_social']
        numero_afiliado = request.form['n_afiliado']
        condicion = request.form['condicion']
        activo = request.form['activo']

        validadores = [
            (validar_nombre, [nombre]),
            (validar_apellido, [apellido]),
            (validar_dni, [dni]),
            (validar_domicilio, [domicilio]),
            (validar_email, [email]),
            (validar_localidad, [localidad]),
            (validar_telefono, [telefono]),
            (validar_profesion, [profesion]),
            (validar_puesto_laboral, [puesto_laboral]),
            (validar_fecha_inicio, [fecha_inicio_str]),
            (validar_fecha_cese, [fecha_cese_str, fecha_inicio_str]),  # Aquí sí hay dos argumentos
            (validar_contacto_emergencia, [contacto_emergencia]),
            (validar_obra_social, [obra_social]),
            (validar_numero_afiliado, [numero_afiliado]),
            (validar_condicion, [condicion]),
            (validar_activo, [activo])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)  # Desempaquetamos los argumentos
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('equipo.editar_empleado', id=id))  # Redirige si hay error

        empleado_aux.nombre = nombre
        empleado_aux.apellido = apellido
        empleado_aux.dni = dni
        empleado_aux.domicilio = domicilio
        empleado_aux.email = email
        empleado_aux.localidad = localidad
        empleado_aux.telefono = telefono
        empleado_aux.profesion = profesion
        empleado_aux.puesto_laboral = puesto_laboral
        empleado_aux.fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        empleado_aux.fecha_cese = datetime.strptime(fecha_cese_str, '%Y-%m-%d')
        empleado_aux.contacto_emergencia = contacto_emergencia
        empleado_aux.obra_social = obra_social
        empleado_aux.numero_afiliado = numero_afiliado
        empleado_aux.condicion = condicion
        empleado_aux.activo = activo == 'Sí' 

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
@check("equipo_update")
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

@equipo_bp.route('/descargar_documento/<int:document_id>')
@check("equipo_show")
def descargar_documento(document_id):
    documento = documento.Documento.query.get_or_404(document_id)  
    url_descarga = f"https://{documento.url}"  
    return redirect(url_descarga)


@equipo_bp.route('/eliminar_documento/<int:document_id>', methods=['POST'])
@check("equipo_destroy")
def eliminar_documento(document_id):
    print("Eliminando documento...")
    documento = documento.Documento.query.get_or_404(document_id)  
    eliminar_de_minio(documento.titulo)  
    try:
        db.session.delete(documento)
        db.session.commit()

        flash('Documento eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el documento: {str(e)}', 'danger')

    return redirect(url_for('equipo.detalle_empleado', id=documento.empleado_id))  

def eliminar_de_minio(file):
    client = current_app.storage.client
    object_name = f'documentos_empleados/{file}' 
    client.remove_object('grupo49', object_name)
