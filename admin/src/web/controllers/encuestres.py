import os
from flask import Blueprint, render_template, jsonify, request, abort, flash, url_for, redirect, current_app, send_file
from sqlalchemy import asc, desc
from src.core.database import db 
from datetime import datetime
from src.core import encuestre
from src.core.encuestre import documento_encuestre
from src.core.equipo import Empleado
from src.web.handlers.auth import check
from src.web.controllers.documentos import generar_nombre 
from src.web.validadores.validador import (
    validar_nombre, validar_fecha_ingreso,
    validar_fecha_nacimiento, validar_sexo,
    validar_raza, validar_pelaje, validar_compra_donacion, 
    validar_tipo_ja_asignado, validar_entrenadores_conductores, validar_sede_asignada

)
from src.web import storage
import io

encuestre_bp = Blueprint('encuestre', __name__, url_prefix='/encuestre')

@encuestre_bp.get("/")
@check("encuestre_index")
def index():
    """
    Controlador para la página de inicio del Ecuestre. Muestra una lista de caballos con
    paginación y filtros de búsqueda.

    :return: Renderiza la plantilla 'encuestre/encuestre.html' con los caballos y parámetros de búsqueda.
    """
    registros_por_pagina = 10
    
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')  
    order = request.args.get('order', 'asc')  
    order_prop = request.args.get('order_prop', 'nombre')
    pagina = request.args.get('pagina', 1, type=int)
    
    query = encuestre.Encuestre.query
    
    if search:
        if filter_by == 'nombre':
            query = query.filter(encuestre.Encuestre.nombre.ilike(f'%{search}%'))
        elif filter_by == 'tipo_ja_asignado':
            query = query.filter(encuestre.Encuestre.tipo_ja_asignado.ilike(f'%{search}%'))
    
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(encuestre.Encuestre, order_prop)))
        else:
            query = query.order_by(desc(getattr(encuestre.Encuestre, order_prop)))


    if order_prop == 'nombre':
        query = query.order_by(asc(encuestre.Encuestre.nombre)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.nombre))
    elif order_prop == 'fecha_nacimiento':
        query = query.order_by(asc(encuestre.Encuestre.fecha_nacimiento)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.fecha_nacimiento))
    elif order_prop == 'fecha_ingreso':
        query = query.order_by(asc(encuestre.Encuestre.inserted_at)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.inserted_at))
    

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    
    encuestres = pagination.items

    total_paginas = pagination.pages

    return render_template(
        "encuestre/encuestre.html", 
        encuestres=encuestres, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas
    )


@encuestre_bp.route('/detalle/<int:id>', methods=['GET','POST'])
@check("encuestre_show")
def detalle_encuestre(id):
    """
    Muestra el detalle de un ecuestre y su documentación asociada.

    :param id: ID del ecuestre.
    :return: Renderiza la plantilla 'encuestre/detalle_encuestre.html' con los detalles del caballo y documentos.
    """

    encuestre_aux = encuestre.Encuestre.obtener_encuestre_por_id(id)
    if encuestre_aux is None:
        abort(404)  

    query = documento_encuestre.DocumentoEncuestre.query.filter_by(encuestre_id=id)

    registros_por_pagina = 2

    search = request.args.get('search', '')
    tipo = request.args.get('tipo', '')  
    filter_by = request.args.get('filter_by', 'titulo') 
    order = request.args.get('order', 'asc')  
    order_prop = request.args.get('order_prop', 'titulo')
    pagina = request.args.get('pagina', 1, type=int)
    
    if search:
        if filter_by == 'titulo':
            query = query.filter(documento_encuestre.DocumentoEncuestre.titulo.ilike(f'%{search}%'))
    
    if tipo:
        query = query.filter(documento_encuestre.DocumentoEncuestre.tipo == tipo)
    
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(documento_encuestre.DocumentoEncuestre, order_prop)))
        else:
            query = query.order_by(desc(getattr(documento_encuestre.DocumentoEncuestre, order_prop)))

    if order_prop == 'titulo':
        query = query.order_by(asc(documento_encuestre.DocumentoEncuestre.titulo)) if order == 'asc' else query.order_by(desc(documento_encuestre.DocumentoEncuestre.titulo))
    elif order_prop == 'fecha_subida':
        query = query.order_by(asc(documento_encuestre.DocumentoEncuestre.inserted_at)) if order == 'asc' else query.order_by(desc(documento_encuestre.DocumentoEncuestre.inserted_at))

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    
    documentos_filtrados = pagination.items
    total_paginas = pagination.pages
    
    return render_template(
        'encuestre/detalle_encuestre.html', 
        encuestre=encuestre_aux, 
        documentos=documentos_filtrados,
        search=search, 
        tipo=tipo,
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas

    )



@encuestre_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("encuestre_destroy")
def eliminar_encuestre(id):
    """
    Elimina un ecuestre de la base de datos.

    :param id: ID del ecuestre a eliminar.
    :return: Redirige a la página de índice del ecuestre.
    """
    encuestre_aux = encuestre.Encuestre.query.get_or_404(id)
    
    try:
        db.session.delete(encuestre_aux)
        db.session.commit()

        flash('Encuestre eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el encuestre: {str(e)}', 'danger')
    return redirect(url_for('encuestre.index')) 

@encuestre_bp.route('/registrar', methods=['GET', 'POST'])
@check("encuestre_new")
def registrar_encuestre():
    """
    Registra un nuevo ecuestre. Realiza validaciones sobre los campos del formulario
    y guarda el nuevo cuestre en la base de datos.

    :return: Redirige a la página de detalles del ecuestre registrado o muestra mensajes de error.
    """
    if request.method == 'POST':
        
        nombre = request.form.get('nombre')
        fecha_nacimiento_str = request.form.get('fecha_nacimiento')
        sexo = request.form.get('sexo')
        raza = request.form.get('raza')
        pelaje = request.form.get('pelaje')
        compra_donacion = request.form.get('tipo_ingreso')
        fecha_ingreso_str = request.form.get('fecha_ingreso')
        sede_asignada = request.form.get('sede_asignada')
        tipo_ja_asignado = request.form.get('tipo_ja_asignado')
        entrenadores_conductores_ids = request.form.getlist('entrenadores_conductores')

        if not (nombre and sexo and raza and pelaje and compra_donacion and sede_asignada and entrenadores_conductores_ids and tipo_ja_asignado):
            
            flash(' Faltan completar campos', 'danger')
            
            return render_template('encuestre/registrar_encuestre.html',
                nombre=nombre,
                sexo=sexo,
                raza=raza,
                pelaje=pelaje,
                compra_donacion=compra_donacion,
                sede_asignada=sede_asignada,
                tipo_ja_asignado=tipo_ja_asignado
            )
            #return redirect(url_for('encuestre.registrar_encuestre'))

        validadores = [
            (validar_nombre, [nombre]),
            (validar_fecha_ingreso, [fecha_ingreso_str]),
            (validar_fecha_nacimiento, [fecha_nacimiento_str]),
            (validar_sexo, [sexo]),
            (validar_raza, [raza]),
            (validar_pelaje, [pelaje]),
            (validar_compra_donacion, [compra_donacion]),
            (validar_tipo_ja_asignado, [tipo_ja_asignado]),
            (validar_entrenadores_conductores, [entrenadores_conductores_ids]),
            (validar_sede_asignada, [sede_asignada])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('encuestre.registrar_encuestre'))

        nuevo_encuestre = encuestre.Encuestre(
            nombre=nombre,
            fecha_nacimiento=datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d'),
            sexo=sexo,
            raza=raza,
            pelaje=pelaje,
            compra_donacion=compra_donacion,
            fecha_ingreso=datetime.strptime(fecha_ingreso_str, '%Y-%m-%d'),
            sede_asignada=sede_asignada,
            tipo_ja_asignado=tipo_ja_asignado
        )

        empleados_seleccionados = Empleado.query.filter(Empleado.id.in_(entrenadores_conductores_ids)).all()
        nuevo_encuestre.entrenadores_conductores = empleados_seleccionados
        
        try:
            
            db.session.add(nuevo_encuestre)
            db.session.commit()
            flash('Caballo registrado exitosamente', 'success')
            return redirect(url_for('encuestre.detalle_encuestre', id=nuevo_encuestre.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el caballo: {str(e)}', 'danger')
            print(f'Error {str(e)}')
            return redirect(url_for('encuestre.registrar_encuestre'))
    
    empleados = Empleado.query.filter(Empleado.puesto_laboral.in_(['Entrenador de caballos', 'Conductor'])).all()
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    return render_template('encuestre/registrar_encuestre.html', empleados=empleados, fecha_hoy=fecha_hoy)

@encuestre_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("encuestre_update")
def editar_encuestre(id):
    """
    Edita los datos de un ecuestre existente.

    :param id: ID del ecuestre a editar.
    :return: Redirige a la página de detalles del ecuestre editado o muestra mensajes de error.
    """

    encuestre_aux = encuestre.Encuestre.obtener_encuestre_por_id(id)
    if encuestre_aux is None:
        abort(404) 
    
    if request.method == 'POST':
        encuestre_aux.nombre = request.form['nombre']    
        encuestre_aux.sexo = request.form['sexo']
        encuestre_aux.raza = request.form['raza']
        encuestre_aux.pelaje = request.form['pelaje']
        encuestre_aux.compra_donacion = request.form['tipo_ingreso']
        encuestre_aux.sede_asignada = request.form['sede_asignada']
        entrenadores_conductores_ids = request.form.getlist('entrenadores_conductores')

        if not (encuestre_aux.nombre and encuestre_aux.sexo and encuestre_aux.raza and encuestre_aux.pelaje and encuestre_aux.compra_donacion and encuestre_aux.sede_asignada and entrenadores_conductores_ids):
            flash(' Faltan completar campos', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))

        validadores = [
            (validar_nombre, [encuestre_aux.nombre]),
            (validar_sexo, [encuestre_aux.sexo]),
            (validar_raza, [encuestre_aux.raza]),
            (validar_pelaje, [encuestre_aux.pelaje]),
            (validar_compra_donacion, [encuestre_aux.compra_donacion]),
            (validar_entrenadores_conductores, [entrenadores_conductores_ids]),
            (validar_sede_asignada, [encuestre_aux.ede_asignada])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('encuestre.registrar_encuestre'))

        empleados_seleccionados = Empleado.query.filter(Empleado.id.in_(entrenadores_conductores_ids)).all()
        encuestre_aux.entrenadores_conductores = empleados_seleccionados
        
        db.session.commit()
        flash('Los cambios se han guardado exitosamente.', 'success')
        return redirect(url_for('encuestre.detalle_encuestre', id=encuestre_aux.id))
    
    empleados = Empleado.query.filter(Empleado.puesto_laboral.in_(['Entrenador de caballos', 'Conductor'])).all()

    entrenadores_ids = [entrenador.id for entrenador in encuestre_aux.entrenadores_conductores]

    return render_template(
    'encuestre/editar_encuestre.html', 
    encuestre=encuestre_aux, 
    empleados=empleados, 
    entrenadores_ids=entrenadores_ids,  
    fecha_hoy=datetime.today().date()
)

@encuestre_bp.route('/subir_documento', methods=['POST'])
def subir_documento():
    """
    Permite seleccionar un documento. Valida los campos del documento, nombre, tamaño y extension. Y lo
    asocia al ecuestre accedido

    :return: Redirige a la página de detalles del ecuestre o muestra mensajes de error.
    """
    MAX_FILE_SIZE = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    file = request.files['file']
    tipo_documento = request.form.get('tipo_documento')

    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    if not allowed_file(file.filename):
        flash('El archivo no tiene una extensión permitida', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))

    client = current_app.storage.client 

    file_size = os.fstat(file.fileno()).st_size
    if file_size > MAX_FILE_SIZE:
        flash('El archivo excede el tamaño máximo permitido (16MB)', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    try:
        client.put_object(
            'grupo49',
            f'documentos_encuestres/{file.filename}',
            file,
            file_size, 
            content_type=file.content_type
        )

        encuestre_id = request.form.get('encuestre_id')
        encuestre_aux = encuestre.Encuestre.query.get(encuestre_id)
        
        nuevo_documento = documento_encuestre.DocumentoEncuestre(
            titulo=file.filename,
            tipo=tipo_documento,
            url=f"{current_app.config['MINIO_SERVER']}/grupo49/documento_encuestre/{file.filename}",
            encuestre=encuestre_aux
        )
        
        db.session.add(nuevo_documento)
        db.session.commit()
        
        flash('Documento subido exitosamente', 'success')
    except Exception as e:
        flash(f'Error al subir el documento: {str(e)}', 'error')
    
    return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))


@encuestre_bp.route('/descargar_documento/<int:document_id>')
@check("encuestre_show")
def descargar_documento(document_id):
    """
    Descargar documento existente o redirige al enlace.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige al enlace del documento o al detalle del ecuestre, dependiendo si es un enlace o un documento o retorna error. 
    """
    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)

    if documento is None:
        flash('No se encontro el documento/enlace.', 'danger')
        return redirect(url_for('equipo.index'))
    
    encuestre = documento_encuestre.DocumentoEncuestre.get_encuestre_by_document_id(document_id)
    client = current_app.storage.client
    object_name = f'documentos_encuestres/{documento.titulo}'
    
    try: 
        if(documento.is_document):
            url_descarga = url_for('encuestre.detalle_encuestre', id=encuestre.id)
            response = client.get_object("grupo49", object_name)
            doc = io.BytesIO(response.read())
            flash('El documento se ha descargado con éxito.', 'success')
            return send_file(doc, as_attachment=True, download_name=documento.titulo)
            
        else: 
            url_descarga = documento.url
    except Exception as e: 
        flash(f'Error en la descarga: {str(e)}', 'danger')



    return redirect(url_descarga)


    

@encuestre_bp.route('/eliminar_documento/<int:document_id>', methods=['POST'])
@check("encuestre_destroy")
def eliminar_documento(document_id):
    """
    Elimina el documento o enlace existente.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige al detalle del ecuestre o retorna error.
    """
    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)

    if(documento.is_document):
        eliminar_de_minio(documento.titulo)

    try:
        db.session.delete(documento)
        db.session.commit()

        flash('Documento eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el documento: {str(e)}', 'danger')

    return redirect(url_for('encuestre.detalle_encuestre', id=documento.encuestre_id))

def eliminar_de_minio(file):
    """
    Elimina el documento existente de minio.
    
    :param file: titulo del documento.
    """
    client = current_app.storage.client
    object_name = f'documentos_encuestres/{file}'
    client.remove_object('grupo49', object_name)

@encuestre_bp.route('/editar_documento/<int:document_id>', methods=['POST','GET'])
@check("encuestre_update")
def editar_documento(document_id):
    """
    Edita el documento o enlace existente.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige a la plantilla encuestre/editar_documento.html o retorna error.
    """

    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)
    encuestre = documento_encuestre.DocumentoEncuestre.get_encuestre_by_document_id(document_id)
    tipo = documento.tipo
    if documento is None:
        abort(404) 
    
    if request.method == 'POST':
        documento.titulo = request.form['nombre']    
        documento.tipo = request.form['tipo_documento']
        
        db.session.commit()
        flash('Los cambios se han guardado exitosamente.', 'success')
        return redirect(url_for('encuestre.detalle_encuestre', id=encuestre.id))

    return render_template('encuestre/editar_documento.html', documento=documento, encuestre=encuestre, tipo=tipo)


@encuestre_bp.route('/subir_enlace', methods=['POST'])
def subir_enlace():
    """
    Registra un enlace en la base de datos en la tabla de documentos.

    :return: Redirige al detalle del ecuestre o retorna error.
    """

    encuestre_id = request.form.get('encuestre_id')
    encuestre_aux = encuestre.Encuestre.query.get(encuestre_id)
    tipo_enlace = request.form.get('tipo_documento')

    url_enlace = request.form.get('enlace')

    if not url_enlace:
        flash('El enlace no puede estar vacío', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=encuestre_id))

    nuevo_enlace = documento_encuestre.DocumentoEncuestre(
        titulo=url_enlace,
        tipo=tipo_enlace,
        url=url_enlace,
        encuestre=encuestre_aux,
        is_document = False
    )
    
    db.session.add(nuevo_enlace)
    db.session.commit()

    flash('Enlace subido exitosamente', 'success')
    return redirect(url_for('encuestre.detalle_encuestre', id=encuestre_id))