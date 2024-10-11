from flask import Blueprint, render_template, jsonify, request, abort, flash, url_for, redirect, current_app
from sqlalchemy import asc, desc
from src.core.database import db 
from datetime import datetime

from src.core import encuestre
from src.core.encuestre import documento_encuestre
from src.core.equipo import Empleado

from src.web.handlers.auth import check

from src.web.helpers import generar_url_firmada



# from ulid import ULID

import os

from src.web import storage

encuestre_bp = Blueprint('encuestre', __name__, url_prefix='/encuestre')

@encuestre_bp.get("/")
@check("encuestre_index")
def index():
    print("Ruta /encuestre/ accedida")

    registros_por_pagina = 1

    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')  # Por defecto 'nombre'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'nombre')
    pagina = request.args.get('pagina', 1, type=int)
    
    # Construir la query base
    query = encuestre.Encuestre.query
    
    # Filtrar según el campo seleccionado (filter_by)
    if search:
        if filter_by == 'nombre':
            query = query.filter(encuestre.Encuestre.nombre.ilike(f'%{search}%'))
        elif filter_by == 'tipo_ja_asignado':
            query = query.filter(encuestre.Encuestre.tipo_ja_asignado.ilike(f'%{search}%'))
    
    # Ordenar los resultados por el campo seleccionado y en el orden indicado
    #if order == 'asc':
    #    query = query.order_by(asc(getattr(encuestre.Encuestre, filter_by)))
    #else:
    #    query = query.order_by(desc(getattr(encuestre.Encuestre, filter_by)))
    
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(encuestre.Encuestre, order_prop)))
        else:
            query = query.order_by(desc(getattr(encuestre.Encuestre, order_prop)))

    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
    if order_prop == 'nombre':
        query = query.order_by(asc(encuestre.Encuestre.nombre)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.nombre))
    elif order_prop == 'fecha_nacimiento':
        query = query.order_by(asc(encuestre.Encuestre.fecha_nacimiento)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.fecha_nacimiento))
    elif order_prop == 'fecha_ingreso':
        query = query.order_by(asc(encuestre.Encuestre.inserted_at)) if order == 'asc' else query.order_by(desc(encuestre.Encuestre.inserted_at))
    

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    
    encuestres = pagination.items

    total_paginas = pagination.pages


    # Renderizar la plantilla y pasar los empleados y los parámetros
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


@encuestre_bp.route('/detalle/<int:id>', methods=['GET'])
@check("encuestre_show")
def detalle_encuestre(id):

    encuestre_aux = encuestre.Encuestre.obtener_encuestre_por_id(id)
    if encuestre_aux is None:
        abort(404)  

    query = documento_encuestre.DocumentoEncuestre.query.filter_by(encuestre_id=id)

    registros_por_pagina = 2

    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    tipo = request.args.get('tipo', '')  # Filtro por tipo de documento
    filter_by = request.args.get('filter_by', 'titulo')  # Por defecto 'nombre'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
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

    # Si se quiere ordenar por nombre, apellido o fecha de creación adicionalmente
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
    # Buscar el encuestre por ID
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
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form.get('nombre')
        fecha_nacimiento_str = request.form.get('fecha_nacimiento')
        sexo = request.form.get('sexo')
        raza = request.form.get('raza')
        pelaje = request.form.get('pelaje')
        compra_donacion = request.form.get('tipo_ingreso')  # Compra o Donación
        fecha_ingreso_str = request.form.get('fecha_ingreso')
        sede_asignada = request.form.get('sede_asignada')
        tipo_ja_asignado = request.form.get('tipo_ja_asignado')
        entrenadores_conductores_ids = request.form.getlist('entrenadores_conductores')

        

        if not (nombre and sexo and raza and pelaje and compra_donacion and sede_asignada and entrenadores_conductores_ids and tipo_ja_asignado):
            flash(' Faltan completar campos', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))
        
        if not fecha_nacimiento_str:
            flash('La fecha de nacimiento es obligatoria', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
            if fecha_nacimiento > datetime.today():
                flash('La fecha de nacimiento no puede ser futura', 'danger')
                return redirect(url_for('encuestre.registrar_encuestre'))
        except ValueError or UnboundLocalError:
            flash('Formato de fecha de nacimiento inválido', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))

        # Validar y convertir la fecha de ingreso
        if not fecha_ingreso_str:
            flash('La fecha de ingreso es obligatoria', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))

        try:
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d')
            if fecha_ingreso > datetime.today():
                flash('La fecha de ingreso no puede ser futura', 'danger')
                return redirect(url_for('encuestre.registrar_encuestre'))
        except ValueError or UnboundLocalError:
            flash('Formato de fecha de ingreso inválido', 'danger')
            return redirect(url_for('encuestre.registrar_encuestre'))

        
        # Aquí irían las demás validaciones para los campos si es necesario

        # Si todo está bien, continuar con el registro
        # Por ejemplo, crear el objeto Encustre y guardarlo en la base de datos

        # Crear el objeto encuestre
        nuevo_encuestre = encuestre.Encuestre(
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            raza=raza,
            pelaje=pelaje,
            compra_donacion=compra_donacion,
            fecha_ingreso=fecha_ingreso,
            sede_asignada=sede_asignada,
            tipo_ja_asignado=tipo_ja_asignado
        )

        empleados_seleccionados = Empleado.query.filter(Empleado.id.in_(entrenadores_conductores_ids)).all()
        nuevo_encuestre.entrenadores_conductores = empleados_seleccionados
        
        try:
            # Subir a la base de datos
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
    
    encuestre_aux = encuestre.Encuestre.obtener_encuestre_por_id(id)
    if encuestre_aux is None:
        abort(404) 
    
    if request.method == 'POST':
        # Obtener datos del formulario
        encuestre_aux.nombre = request.form['nombre']    
        encuestre_aux.sexo = request.form['sexo']
        encuestre_aux.raza = request.form['raza']
        encuestre_aux.pelaje = request.form['pelaje']
        encuestre_aux.compra_donacion = request.form['tipo_ingreso']
        encuestre_aux.sede_asignada = request.form['sede_asignada']
        
        # Procesar entrenadores y conductores seleccionados
        entrenadores_conductores_ids = request.form.getlist('entrenadores_conductores')

        empleados_seleccionados = Empleado.query.filter(Empleado.id.in_(entrenadores_conductores_ids)).all()
        encuestre_aux.entrenadores_conductores = empleados_seleccionados
        

        # Guardar cambios en la base de datos
        db.session.commit()
        flash('Los cambios se han guardado exitosamente.', 'success')
        return redirect(url_for('encuestre.detalle_encuestre', id=encuestre_aux.id))
    
    # Obtener empleados para la lista de selección
    
    empleados = Empleado.query.filter(Empleado.puesto_laboral.in_(['Entrenador de caballos', 'Conductor'])).all()

    entrenadores_ids = [entrenador.id for entrenador in encuestre_aux.entrenadores_conductores]

    return render_template(
    'encuestre/editar_encuestre.html', 
    encuestre=encuestre_aux, 
    empleados=empleados, 
    entrenadores_ids=entrenadores_ids,  # Pasar solo los IDs
    fecha_hoy=datetime.today().date()
)

@encuestre_bp.route('/subir_documento', methods=['POST'])
def subir_documento():

    MAX_FILE_SIZE = 16 * 1024 * 1024

    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    file = request.files['file']
    tipo_documento = request.form.get('tipo_documento')

    client = current_app.storage.client 

    file_size = os.fstat(file.fileno()).st_size
    
    if file_size > MAX_FILE_SIZE:
        flash('El archivo excede el tamaño máximo permitido (16MB)', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('encuestre.detalle_encuestre', id=request.form.get('encuestre_id')))
    
    if tipo_documento not in ['entrevista', 'evaluación', 'planificaciones', 'evolución', 'crónicas', 'documental']:
        return 'Tipo de documento no válido', 400
    
    #ulid = str(ULID())
    #extension = os.path.splitext(file.filename)[1]
    #nombre_unico = f"{extension}"

    
    try:
        client.put_object(
            'grupo49',
            f'documentos_encuestres/{file.filename}',
            file,
            file_size, 
            content_type=file.content_type
        )
        
        # Obtener el encuestre asociado
        encuestre_id = request.form.get('encuestre_id')
        encuestre_aux = encuestre.Encuestre.query.get(encuestre_id)
        
        # Crear el documento y asociarlo al encuestre
        nuevo_documento = documento_encuestre.DocumentoEncuestre(
            titulo=file.filename,
            tipo=tipo_documento,
            url=f"{current_app.config['MINIO_SERVER']}/grupo49/{file.name}",
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
    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)
    
    #url_firmada = generar_url_firmada("grupo49", documento.titulo)

    url_descarga = f"https://{documento.url}"
    return redirect(url_descarga)


@encuestre_bp.route('/eliminar_documento/<int:document_id>', methods=['POST'])
@check("encuestre_destroy")
def eliminar_documento(document_id):
    print("eliminandoooooooooooooooooooooooooooooooooo")
    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)
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
    client = current_app.storage.client
    object_name = f'documentos_encuestres/{file}'
    client.remove_object('grupo49', object_name)

# Ruta para editar documento
@encuestre_bp.route('/editar_documento/<int:document_id>')
@check("encuestre_update")
def editar_documento(document_id):
    documento = documento_encuestre.DocumentoEncuestre.query.get_or_404(document_id)
    
    # Renderizar un formulario con la información del documento para editar
    return render_template('encuestre/editar_documento.html', documento=documento)