from io import BytesIO
import io
from flask import Blueprint, render_template, jsonify, request, abort, flash, send_file, url_for, redirect, current_app
from src.core.database import db
from datetime import datetime
from sqlalchemy import asc, desc
from src.core import jinetes_amazonas
from src.core.equipo import Empleado
from src.core.encuestre import Encuestre
from src.core.jinetes_amazonas import documento_jinete
from src.web.validadores.validador import (
    validar_campo_texto, validar_campo_booleano,
    validar_fecha_nacimiento, validar_sede_asignada,
    validar_dni, validar_campo_texto_numeros, 
    validar_telefono, validar_email_o_vacio, validar_campo_numeros,
    validar_diagnostico_discapacidad, validar_tipo_discapacidad,
    validar_escolaridad_familiar, validar_propuesta_trabajo, validar_condicion_jinete,
    validar_dia, validar_profesor_terapeuta, validar_conductor, validar_auxiliar, validar_caballo

)

from src.web.handlers.auth import check
import os

jinete_amazonas_bp = Blueprint('jinetes_amazonas', __name__, url_prefix='/jinetes-amazonas')

# Listar todos los Jinetes y Amazonas
@jinete_amazonas_bp.get("/")
@check("ja_index")
def index():
    """
    Muestra una lista paginada de todos los Jinetes y Amazonas con capacidades de búsqueda y orden.

    Esta función obtiene parámetros de búsqueda, filtro y orden desde la URL, construye una consulta dinámica
    y muestra los resultados paginados.

    Parámetros obtenidos de la URL:
        - search (str): Cadena de texto para buscar por nombre, apellido, dni o profesionales que los atienden.
        - filter_by (str): Filtro por el cual buscar (nombre, apellido, dni, profesionales_atienden).
        - order (str): Orden de los resultados (asc o desc).
        - order_prop (str): Propiedad por la cual ordenar (nombre, apellido, etc.).
        - pagina (int): Número de página para la paginación.

    Returns:
        Renderiza el template "jinetes_amazonas/jinetes_amazonas.html" con los resultados filtrados y paginados.
    """
    registros_por_pagina = 5

    # Parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'nombre')
    order = request.args.get('order', 'asc')
    order_prop = request.args.get('order_prop', 'nombre')
    pagina = request.args.get('pagina', 1, type=int)
    
    # Construcción de la query
    query = jinetes_amazonas.JineteAmazona.query

    # Filtros de búsqueda
    if search:
        if filter_by == 'nombre':
            query = query.filter(jinetes_amazonas.JineteAmazona.nombre.ilike(f'%{search}%'))
        elif filter_by == 'apellido':
            query = query.filter(jinetes_amazonas.JineteAmazona.apellido.ilike(f'%{search}%'))
        elif filter_by == 'dni':
            query = query.filter(jinetes_amazonas.JineteAmazona.dni.ilike(f'%{search}%'))
        elif filter_by == 'profesionales_atienden':
            query = query.filter(jinetes_amazonas.JineteAmazona.profesionales_atienden.ilike(f'%{search}%'))
    
    # Orden de resultados
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(jinetes_amazonas.JineteAmazona, order_prop)))
        else:
            query = query.order_by(desc(getattr(jinetes_amazonas.JineteAmazona, order_prop)))

    # Orden adicional por nombre o apellido
    if order_prop == 'nombre':
        query = query.order_by(asc(jinetes_amazonas.JineteAmazona.nombre)) if order == 'asc' else query.order_by(desc(jinetes_amazonas.JineteAmazona.nombre))
    elif order_prop == 'apellido':
        query = query.order_by(asc(jinetes_amazonas.JineteAmazona.apellido)) if order == 'asc' else query.order_by(desc(jinetes_amazonas.JineteAmazona.apellido))

    # Paginación
    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    jinetes = pagination.items
    total_paginas = pagination.pages

    return render_template(
        "jinetes_amazonas/jinetes_amazonas.html", 
        jinetes=jinetes, 
        search=search, 
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas
    )


# Ver detalles de un Jinete o Amazona
@jinete_amazonas_bp.get("/detalle/<int:id>")
@check("ja_show")
def detalle(id):
    """
    Muestra los detalles de un Jinete o Amazona, incluyendo los documentos asociados.

    Busca el Jinete o Amazona por su ID, así como los documentos asociados, y permite filtrar
    y ordenar estos documentos. También obtiene los datos relacionados de otras entidades, como el
    caballo, auxiliar de pista, profesor terapeuta y conductor.

    Args:
        id (int): ID del Jinete o Amazona.

    Parámetros obtenidos de la URL:
        - search (str): Cadena de texto para buscar documentos por título.
        - tipo (str): Filtro por tipo de documento.
        - filter_by (str): Filtro por el cual buscar los documentos (por defecto es título).
        - order (str): Orden de los documentos (asc o desc).
        - order_prop (str): Propiedad por la cual ordenar los documentos (por defecto es título).
        - pagina (int): Número de página para la paginación de los documentos.

    Returns:
        Renderiza el template "jinetes_amazonas/detalle.html" con los detalles del Jinete o Amazona y los documentos filtrados.
    """
    jinete_amazonas_aux = jinetes_amazonas.JineteAmazona.query.get(id)
    if not jinete_amazonas_aux:
        abort(404)

    # Query para documentos asociados
    query = documento_jinete.DocumentoJinete.query.filter_by(jinete_amazonas_id=id)

    registros_por_pagina = 2

    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    tipo = request.args.get('tipo', '')  # Filtro por tipo de documento
    filter_by = request.args.get('filter_by', 'titulo')  # Por defecto 'titulo'
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'titulo')
    pagina = request.args.get('pagina', 1, type=int)
    
    # Filtro de búsqueda en los documentos
    if search:
        if filter_by == 'titulo':
            query = query.filter(documento_jinete.DocumentoJinete.titulo.ilike(f'%{search}%'))
    
    # Filtro por tipo de documento
    if tipo:
        query = query.filter(documento_jinete.DocumentoJinete.tipo == tipo)
    
    # Orden de los documentos
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(documento_jinete.DocumentoJinete, order_prop)))
        else:
            query = query.order_by(desc(getattr(documento_jinete.DocumentoJinete, order_prop)))

    # Orden adicional por título o fecha de subida
    if order_prop == 'titulo':
        query = query.order_by(asc(documento_jinete.DocumentoJinete.titulo)) if order == 'asc' else query.order_by(desc(documento_jinete.DocumentoJinete.titulo))
    elif order_prop == 'fecha_subida':
        query = query.order_by(asc(documento_jinete.DocumentoJinete.inserted_at)) if order == 'asc' else query.order_by(desc(documento_jinete.DocumentoJinete.inserted_at))

    # Paginación de los documentos
    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    documentos_filtrados = pagination.items
    total_paginas = pagination.pages

    # Obtener datos relacionados
    caballo = Encuestre.query.get(jinete_amazonas_aux.caballo)
    auxiliar_pista = Empleado.query.get(jinete_amazonas_aux.auxiliar_pista)
    profesor_terapeuta = Empleado.query.get(jinete_amazonas_aux.profesor_terapeuta)
    conductor = Empleado.query.get(jinete_amazonas_aux.conductor)
    
    return render_template(
        'jinetes_amazonas/detalle.html', 
        jinete=jinete_amazonas_aux,
        caballo=caballo,
        auxiliar_pista=auxiliar_pista,
        profesor_terapeuta=profesor_terapeuta,
        conductor=conductor,
        documentos=documentos_filtrados,
        search=search, 
        tipo=tipo,
        filter_by=filter_by, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas
    )


# Registrar un nuevo Jinete o Amazona
@jinete_amazonas_bp.route("/registrar", methods=['GET', 'POST'])
@check("ja_new")
def registrar():
    """
    Controlador para registrar un nuevo Jinete o Amazona.
    - Si la solicitud es GET: Muestra el formulario de registro.
    - Si la solicitud es POST: Procesa los datos del formulario y los valida antes de guardarlos en la base de datos.

    :return: Redirige a la página de detalles del jinete/amazona registrado o muestra mensajes de error
    """
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        edad = request.form.get('edad')
        fecha_nacimiento_str = request.form.get('fecha_nacimiento')
        lugar_nacimiento_localidad = request.form.get('lugar_nacimiento_localidad')
        lugar_nacimiento_provincia = request.form.get('lugar_nacimiento_provincia')
        domicilio_actual = request.form.get('domicilio_actual')
        telefono = request.form.get('telefono')
        contacto_emergencia = request.form.get('contacto_emergencia')
        telefono_emergencia = request.form.get('telefono_emergencia')
        becado = request.form.get('becado') 
        beca_observaciones = request.form.get('beca_observaciones')
        certificado_discapacidad =  request.form.get('certificado_discapacidad')
        diagnostico_discapacidad = request.form.get('diagnostico_discapacidad')
        tipo_discapacidad = request.form.get('tipo_discapacidad')
        percibe_asignacion_familiar = request.form.get('percibe_asignacion_familiar')
        asignacion_hijo = request.form.get('asignacion_hijo')
        asignacion_hijo_discapacidad = request.form.get('asignacion_hijo_discapacidad')
        asignacion_ayuda_escolar =request.form.get('asignacion_ayuda_escolar') 
        pension = request.form.get('pension')
        obra_social = request.form.get('obra_social')
        numero_afiliado = request.form.get('numero_afiliado')
        curatela =  request.form.get('curatela')
        observaciones_previsionales = request.form.get('observaciones_previsionales')
        institucion_escolar = request.form.get('institucion_escolar')
        direccion_institucion = request.form.get('direccion_institucion')
        telefono_institucion = request.form.get('telefono_institucion')
        grado_anio_actual = request.form.get('grado_anio_actual')
        observaciones_institucion = request.form.get('observaciones_institucion')
        profesionales_atienden = request.form.get('profesionales_atienden')
        parentesco_familiar_1 = request.form.get('parentesco_familiar_1')
        nombre_familiar_1 = request.form.get('nombre_familiar_1')
        apellido_familiar_1 = request.form.get('apellido_familiar_1')
        dni_familiar_1 = request.form.get('dni_familiar_1')
        domicilio_familiar_1 = request.form.get('domicilio_familiar_1')
        celular_familiar_1 = request.form.get('celular_familiar_1')
        email_familiar_1 = request.form.get('email_familiar_1')
        escolaridad_familiar_1 = request.form.get('escolaridad_familiar_1')
        ocupacion_familiar_1 = request.form.get('ocupacion_familiar_1')
        parentesco_familiar_2 = request.form.get('parentesco_familiar_2')
        nombre_familiar_2 = request.form.get('nombre_familiar_2')
        apellido_familiar_2 = request.form.get('apellido_familiar_2')
        dni_familiar_2 = request.form.get('dni_familiar_2')
        domicilio_familiar_2 = request.form.get('domicilio_familiar_2')
        celular_familiar_2 = request.form.get('celular_familiar_2')
        email_familiar_2 = request.form.get('email_familiar_2')
        escolaridad_familiar_2 = request.form.get('escolaridad_familiar_2')
        ocupacion_familiar_2 = request.form.get('ocupacion_familiar_2')
        propuesta_trabajo = request.form.get('propuesta_trabajo')
        condicion= request.form.get('condicion')
        sede= request.form.get('sede')
        dia= request.form.getlist('dia')
        profesor_terapeuta = request.form.get('profesor_terapeuta')
        conductor = request.form.get('conductor')
        auxiliar_pista = request.form.get('auxiliar_pista')
        caballo = request.form.get('caballo')
        

        # Validar que los campos requeridos no estén vacíos
        if not (nombre and apellido and dni and edad and fecha_nacimiento_str and lugar_nacimiento_localidad  and pension and lugar_nacimiento_provincia and domicilio_actual and telefono and contacto_emergencia and telefono_emergencia and becado and certificado_discapacidad and diagnostico_discapacidad  and tipo_discapacidad and percibe_asignacion_familiar and asignacion_hijo and asignacion_hijo_discapacidad and asignacion_ayuda_escolar and curatela and propuesta_trabajo and sede and dia and caballo and auxiliar_pista and profesor_terapeuta and conductor and condicion):
            flash('Faltan completar campos obligatorios', 'danger')
            return redirect(url_for('jinetes_amazonas.registrar'))
        
        
         # Verificar si ya existe un jinete/amazona con el mismo DNI
        dni_aux = jinetes_amazonas.JineteAmazona.query.filter_by(dni=dni).first()
        if dni_aux:
            flash('El DNI ingresado ya se encuentra registrado.', 'danger')
            return redirect(url_for('jinetes_amazonas.registrar'))
        
        validadores= [
            (validar_campo_texto, [nombre]),
            (validar_campo_texto, [apellido]),
            (validar_dni, [dni]),
            (validar_campo_numeros, [edad]),
            (validar_fecha_nacimiento, [fecha_nacimiento_str]),
            (validar_campo_texto_numeros, [lugar_nacimiento_localidad]),
            (validar_campo_texto, [lugar_nacimiento_provincia]),
            (validar_campo_texto_numeros, [domicilio_actual]),
            (validar_telefono, [telefono]),
            (validar_campo_texto, [contacto_emergencia]),
            (validar_telefono, [telefono_emergencia]),
            (validar_campo_booleano, [becado]),
            (validar_campo_texto, [beca_observaciones]),
            (validar_campo_booleano, [certificado_discapacidad]),
            (validar_diagnostico_discapacidad,[diagnostico_discapacidad]),
            (validar_tipo_discapacidad,[tipo_discapacidad]),
            (validar_campo_booleano, [percibe_asignacion_familiar]),
            (validar_campo_booleano, [asignacion_hijo]),
            (validar_campo_booleano, [asignacion_hijo_discapacidad]),
            (validar_campo_booleano, [asignacion_ayuda_escolar]),
            (validar_campo_texto, [pension]),
            (validar_campo_texto, [obra_social]),
            (validar_campo_numeros, [numero_afiliado]),
            (validar_campo_booleano, [curatela]),
            (validar_campo_texto, [observaciones_previsionales]),
            (validar_campo_texto, [institucion_escolar]),
            (validar_campo_texto_numeros, [direccion_institucion]),
            (validar_campo_numeros, [telefono_institucion]),
            (validar_campo_texto_numeros, [grado_anio_actual]),
            (validar_campo_texto, [observaciones_institucion]),
            (validar_campo_texto, [profesionales_atienden]),
            (validar_campo_texto, [parentesco_familiar_1]),
            (validar_campo_texto, [nombre_familiar_1]),
            (validar_campo_texto, [apellido_familiar_1]),
            (validar_campo_numeros, [dni_familiar_1]),
            (validar_campo_texto_numeros, [domicilio_familiar_1]),
            (validar_campo_numeros, [celular_familiar_1]),
            (validar_email_o_vacio, [email_familiar_1]),
            (validar_escolaridad_familiar,[escolaridad_familiar_1]),
            (validar_campo_texto, [ocupacion_familiar_1]),
            (validar_campo_texto, [parentesco_familiar_2]),
            (validar_campo_texto, [nombre_familiar_2]),
            (validar_campo_texto, [apellido_familiar_2]),
            (validar_campo_numeros, [dni_familiar_2]),
            (validar_campo_texto_numeros, [domicilio_familiar_2]),
            (validar_campo_numeros, [celular_familiar_2]),
            (validar_email_o_vacio, [email_familiar_2]),
            (validar_escolaridad_familiar,[escolaridad_familiar_2]),
            (validar_campo_texto, [ocupacion_familiar_2]),
            (validar_propuesta_trabajo,[propuesta_trabajo]),
            (validar_condicion_jinete, [condicion]),
            (validar_sede_asignada, [sede]),
            (validar_dia,[dia]),
            (validar_profesor_terapeuta, [profesor_terapeuta]),
            (validar_conductor,[conductor]),
            (validar_auxiliar,[auxiliar_pista]),
            (validar_caballo, [caballo])

        ]

        # Ejecuta todos los validadores
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('jinetes_amazonas.registrar'))
        
        # Crear el objeto JineteAmazona
        nuevo_jinete_amazona = jinetes_amazonas.JineteAmazona(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            edad=edad,
            fecha_nacimiento=datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d'),
            lugar_nacimiento_localidad=lugar_nacimiento_localidad,
            lugar_nacimiento_provincia=lugar_nacimiento_provincia,
            domicilio_actual=domicilio_actual,
            telefono=telefono,
            contacto_emergencia=contacto_emergencia,
            telefono_emergencia=telefono_emergencia,
            becado=(becado == 'True'),
            beca_observaciones=beca_observaciones,
            certificado_discapacidad=(certificado_discapacidad == 'True'),
            diagnostico_discapacidad=diagnostico_discapacidad,
            tipo_discapacidad=tipo_discapacidad,
            percibe_asignacion_familiar=(percibe_asignacion_familiar == 'True'),
            asignacion_hijo=(asignacion_hijo == 'True'),
            asignacion_hijo_discapacidad=(asignacion_hijo_discapacidad == 'True'),
            asignacion_ayuda_escolar=(asignacion_ayuda_escolar == 'True'),
            pension=pension,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            curatela=(curatela == 'True'),
            observaciones_previsionales=observaciones_previsionales,
            institucion_escolar=institucion_escolar,
            direccion_institucion=direccion_institucion,
            telefono_institucion=telefono_institucion,
            grado_anio_actual=grado_anio_actual,
            observaciones_institucion=observaciones_institucion,
            profesionales_atienden=profesionales_atienden,
            parentesco_familiar_1=parentesco_familiar_1,
            nombre_familiar_1=nombre_familiar_1,
            apellido_familiar_1=apellido_familiar_1,
            dni_familiar_1=dni_familiar_1,
            domicilio_familiar_1=domicilio_familiar_1,
            celular_familiar_1=celular_familiar_1,
            email_familiar_1=email_familiar_1,
            escolaridad_familiar_1=escolaridad_familiar_1,
            ocupacion_familiar_1=ocupacion_familiar_1,
            parentesco_familiar_2=parentesco_familiar_2,
            nombre_familiar_2=nombre_familiar_2,
            apellido_familiar_2=apellido_familiar_2,
            dni_familiar_2=dni_familiar_2,
            domicilio_familiar_2=domicilio_familiar_2,
            celular_familiar_2=celular_familiar_2,
            email_familiar_2=email_familiar_2,
            escolaridad_familiar_2=escolaridad_familiar_2,
            ocupacion_familiar_2=ocupacion_familiar_2,
            propuesta_trabajo = propuesta_trabajo,
            condicion= condicion,
            sede= sede,
            dia= dia,
            profesor_terapeuta = profesor_terapeuta,
            conductor = conductor,
            auxiliar_pista = auxiliar_pista,
            caballo = caballo
        )

        try:
            # Subir a la base de datos
            db.session.add(nuevo_jinete_amazona)
            db.session.commit()
            flash('Jinete/Amazona registrado exitosamente', 'success')
            return redirect(url_for('jinetes_amazonas.detalle', id=nuevo_jinete_amazona.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el jinete/amazona: {str(e)}', 'danger')
            return redirect(url_for('jinetes_amazonas.registrar'))
    
    terapeutas= Empleado.query.filter(Empleado.puesto_laboral.in_(['Terapeuta', 'Profesor de Equitación', 'Docente de Capacitación'])).all()
    auxiliares= Empleado.query.filter_by(puesto_laboral='Auxiliar de pista').all()
    caballos= Encuestre.query.all()
    conductores= Empleado.query.filter_by(puesto_laboral='Conductor').all()
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    return render_template('jinetes_amazonas/registrar.html', fecha_hoy=fecha_hoy, terapeutas=terapeutas, auxiliares=auxiliares, caballos=caballos, conductores=conductores)

# Editar un Jinete o Amazona existente
@jinete_amazonas_bp.route("/editar/<int:id>", methods=['GET', 'POST'])
@check("ja_update")
def editar(id):

    """
    Edita los datos de un jinete/amazona existente.

    :param id: ID del jinete/amazona a editar.
    :return: Redirige a la página de detalles del jinete/amazona editado o muestra mensajes de error.
    """
    jinete_amazonas_aux = jinetes_amazonas.JineteAmazona.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        edad = request.form.get('edad')
        fecha_nacimiento_str = request.form.get('fecha_nacimiento')
        lugar_nacimiento_localidad = request.form.get('lugar_nacimiento_localidad')
        lugar_nacimiento_provincia = request.form.get('lugar_nacimiento_provincia')
        domicilio_actual = request.form.get('domicilio_actual')
        telefono = request.form.get('telefono')
        contacto_emergencia = request.form.get('contacto_emergencia')
        telefono_emergencia = request.form.get('telefono_emergencia')
        becado = request.form.get('becado')
        beca_observaciones = request.form.get('beca_observaciones')
        certificado_discapacidad = request.form.get('certificado_discapacidad') 
        diagnostico_discapacidad = request.form.get('diagnostico_discapacidad')
        tipo_discapacidad = request.form.get('tipo_discapacidad')
        percibe_asignacion_familiar = request.form.get('percibe_asignacion_familiar')
        asignacion_hijo = request.form.get('asignacion_hijo')
        asignacion_hijo_discapacidad =  request.form.get('asignacion_hijo_discapacidad')
        asignacion_ayuda_escolar = request.form.get('asignacion_ayuda_escolar')
        pension = request.form.get('pension')
        obra_social = request.form.get('obra_social')
        numero_afiliado = request.form.get('numero_afiliado')
        curatela = request.form.get('curatela')
        observaciones_previsionales = request.form.get('observaciones_previsionales')
        institucion_escolar = request.form.get('institucion_escolar')
        direccion_institucion = request.form.get('direccion_institucion')
        telefono_institucion = request.form.get('telefono_institucion')
        grado_anio_actual = request.form.get('grado_anio_actual')
        observaciones_institucion = request.form.get('observaciones_institucion')
        profesionales_atienden = request.form.get('profesionales_atienden')
        parentesco_familiar_1 = request.form.get('parentesco_familiar_1')
        nombre_familiar_1 = request.form.get('nombre_familiar_1')
        apellido_familiar_1 = request.form.get('apellido_familiar_1')
        dni_familiar_1 = request.form.get('dni_familiar_1')
        domicilio_familiar_1 = request.form.get('domicilio_familiar_1')
        celular_familiar_1 = request.form.get('celular_familiar_1')
        email_familiar_1 = request.form.get('email_familiar_1')
        escolaridad_familiar_1 = request.form.get('escolaridad_familiar_1')
        ocupacion_familiar_1 = request.form.get('ocupacion_familiar_1')
        parentesco_familiar_2 = request.form.get('parentesco_familiar_2')
        nombre_familiar_2 = request.form.get('nombre_familiar_2')
        apellido_familiar_2 = request.form.get('apellido_familiar_2')
        dni_familiar_2 = request.form.get('dni_familiar_2')
        domicilio_familiar_2 = request.form.get('domicilio_familiar_2')
        celular_familiar_2 = request.form.get('celular_familiar_2')
        email_familiar_2 = request.form.get('email_familiar_2')
        escolaridad_familiar_2 = request.form.get('escolaridad_familiar_2')
        ocupacion_familiar_2 = request.form.get('ocupacion_familiar_2')
        propuesta_trabajo = request.form.get('propuesta_trabajo')
        condicion= request.form.get('condicion')
        sede= request.form.get('sede')
        dia= request.form.getlist('dia')
        profesor_terapeuta = request.form.get('profesor_terapeuta')
        conductor = request.form.get('conductor')
        auxiliar_pista = request.form.get('auxiliar_pista')
        caballo = request.form.get('caballo')


        # Validar que los campos requeridos no estén vacíos
        if not (nombre and apellido and dni and edad and fecha_nacimiento_str and lugar_nacimiento_localidad  and pension and lugar_nacimiento_provincia and domicilio_actual and telefono and contacto_emergencia and telefono_emergencia and becado and certificado_discapacidad and diagnostico_discapacidad  and tipo_discapacidad and percibe_asignacion_familiar and asignacion_hijo and asignacion_hijo_discapacidad and asignacion_ayuda_escolar and curatela and propuesta_trabajo and sede and dia and caballo and auxiliar_pista and profesor_terapeuta and conductor and condicion):
            flash('Faltan completar campos obligatorios', 'danger')
            return redirect(url_for('jinetes_amazonas.editar', id=id))
        

        validadores= [
            (validar_campo_texto, [nombre]),
            (validar_campo_texto, [apellido]),
            (validar_dni, [dni]),
            (validar_campo_numeros, [edad]),
            (validar_fecha_nacimiento, [fecha_nacimiento_str]),
            (validar_campo_texto_numeros, [lugar_nacimiento_localidad]),
            (validar_campo_texto, [lugar_nacimiento_provincia]),
            (validar_campo_texto_numeros, [domicilio_actual]),
            (validar_telefono, [telefono]),
            (validar_campo_texto, [contacto_emergencia]),
            (validar_telefono, [telefono_emergencia]),
            (validar_campo_booleano, [becado]),
            (validar_campo_texto, [beca_observaciones]),
            (validar_campo_booleano, [certificado_discapacidad]),
            (validar_diagnostico_discapacidad,[diagnostico_discapacidad]),
            (validar_tipo_discapacidad,[tipo_discapacidad]),
            (validar_campo_booleano, [percibe_asignacion_familiar]),
            (validar_campo_booleano, [asignacion_hijo]),
            (validar_campo_booleano, [asignacion_hijo_discapacidad]),
            (validar_campo_booleano, [asignacion_ayuda_escolar]),
            (validar_campo_texto, [pension]),
            (validar_campo_texto, [obra_social]),
            (validar_campo_numeros, [numero_afiliado]),
            (validar_campo_booleano, [curatela]),
            (validar_campo_texto, [observaciones_previsionales]),
            (validar_campo_texto, [institucion_escolar]),
            (validar_campo_texto_numeros, [direccion_institucion]),
            (validar_campo_numeros, [telefono_institucion]),
            (validar_campo_texto_numeros, [grado_anio_actual]),
            (validar_campo_texto, [observaciones_institucion]),
            (validar_campo_texto, [profesionales_atienden]),
            (validar_campo_texto, [parentesco_familiar_1]),
            (validar_campo_texto, [nombre_familiar_1]),
            (validar_campo_texto, [apellido_familiar_1]),
            (validar_campo_numeros, [dni_familiar_1]),
            (validar_campo_texto_numeros, [domicilio_familiar_1]),
            (validar_campo_numeros, [celular_familiar_1]),
            (validar_email_o_vacio, [email_familiar_1]),
            (validar_escolaridad_familiar,[escolaridad_familiar_1]),
            (validar_campo_texto, [ocupacion_familiar_1]),
            (validar_campo_texto, [parentesco_familiar_2]),
            (validar_campo_texto, [nombre_familiar_2]),
            (validar_campo_texto, [apellido_familiar_2]),
            (validar_campo_numeros, [dni_familiar_2]),
            (validar_campo_texto_numeros, [domicilio_familiar_2]),
            (validar_campo_numeros, [celular_familiar_2]),
            (validar_email_o_vacio, [email_familiar_2]),
            (validar_escolaridad_familiar,[escolaridad_familiar_2]),
            (validar_campo_texto, [ocupacion_familiar_2]),
            (validar_propuesta_trabajo,[propuesta_trabajo]),
            (validar_condicion_jinete, [condicion]),
            (validar_sede_asignada, [sede]),
            (validar_dia,[dia]),
            (validar_profesor_terapeuta, [profesor_terapeuta]),
            (validar_conductor,[conductor]),
            (validar_auxiliar,[auxiliar_pista]),
            (validar_caballo, [caballo])

        ]

        # Ejecuta todos los validadores
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('jinetes_amazonas.editar', id=id))


        jinete_amazonas_aux.nombre = nombre
        jinete_amazonas_aux.apellido = apellido
        jinete_amazonas_aux.dni = dni
        jinete_amazonas_aux.edad = edad
        jinete_amazonas_aux.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
        jinete_amazonas_aux.lugar_nacimiento_localidad = lugar_nacimiento_localidad
        jinete_amazonas_aux.lugar_nacimiento_provincia = lugar_nacimiento_provincia
        jinete_amazonas_aux.domicilio_actual = domicilio_actual
        jinete_amazonas_aux.telefono = telefono
        jinete_amazonas_aux.contacto_emergencia = contacto_emergencia
        jinete_amazonas_aux.telefono_emergencia = telefono_emergencia
        jinete_amazonas_aux.becado = (becado == 'True')
        jinete_amazonas_aux.beca_observaciones = beca_observaciones
        jinete_amazonas_aux.certificado_discapacidad = (certificado_discapacidad == 'True')
        jinete_amazonas_aux.diagnostico_discapacidad = diagnostico_discapacidad
        jinete_amazonas_aux.tipo_discapacidad = tipo_discapacidad
        jinete_amazonas_aux.percibe_asignacion_familiar = (percibe_asignacion_familiar == 'True')
        jinete_amazonas_aux.asignacion_hijo = (asignacion_hijo == 'True')
        jinete_amazonas_aux.asignacion_hijo_discapacidad = (asignacion_hijo_discapacidad == 'True')
        jinete_amazonas_aux.asignacion_ayuda_escolar = (asignacion_ayuda_escolar == 'True')
        jinete_amazonas_aux.pension = pension
        jinete_amazonas_aux.obra_social = obra_social
        jinete_amazonas_aux.numero_afiliado = numero_afiliado
        jinete_amazonas_aux.curatela = (curatela == 'True')
        jinete_amazonas_aux.observaciones_previsionales = observaciones_previsionales
        jinete_amazonas_aux.institucion_escolar = institucion_escolar
        jinete_amazonas_aux.direccion_institucion = direccion_institucion
        jinete_amazonas_aux.telefono_institucion = telefono_institucion
        jinete_amazonas_aux.grado_anio_actual = grado_anio_actual
        jinete_amazonas_aux.observaciones_institucion = observaciones_institucion
        jinete_amazonas_aux.profesionales_atienden = profesionales_atienden
        jinete_amazonas_aux.parentesco_familiar_1 = parentesco_familiar_1
        jinete_amazonas_aux.nombre_familiar_1 = nombre_familiar_1
        jinete_amazonas_aux.apellido_familiar_1 = apellido_familiar_1
        jinete_amazonas_aux.dni_familiar_1 = dni_familiar_1
        jinete_amazonas_aux.domicilio_familiar_1 = domicilio_familiar_1
        jinete_amazonas_aux.celular_familiar_1 = celular_familiar_1
        jinete_amazonas_aux.email_familiar_1 = email_familiar_1
        jinete_amazonas_aux.escolaridad_familiar_1 = escolaridad_familiar_1
        jinete_amazonas_aux.ocupacion_familiar_1 = ocupacion_familiar_1
        jinete_amazonas_aux.parentesco_familiar_2 = parentesco_familiar_2
        jinete_amazonas_aux.nombre_familiar_2 = nombre_familiar_2
        jinete_amazonas_aux.apellido_familiar_2 = apellido_familiar_2
        jinete_amazonas_aux.dni_familiar_2 = dni_familiar_2
        jinete_amazonas_aux.domicilio_familiar_2 = domicilio_familiar_2
        jinete_amazonas_aux.celular_familiar_2 = celular_familiar_2
        jinete_amazonas_aux.email_familiar_2 = email_familiar_2
        jinete_amazonas_aux.escolaridad_familiar_2 = escolaridad_familiar_2
        jinete_amazonas_aux.ocupacion_familiar_2 = ocupacion_familiar_2
        jinete_amazonas_aux.propuesta_trabajo = propuesta_trabajo
        jinete_amazonas_aux.condicion= condicion
        jinete_amazonas_aux.sede= sede
        jinete_amazonas_aux.dia= dia
        jinete_amazonas_aux.profesor_terapeuta = profesor_terapeuta
        jinete_amazonas_aux.conductor = conductor
        jinete_amazonas_aux.auxiliar_pista = auxiliar_pista
        jinete_amazonas_aux.caballo = caballo


        try:
            db.session.commit()
            flash('Cambios guardados exitosamente', 'success')
            return redirect(url_for('jinetes_amazonas.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar los cambios: {str(e)}', 'danger')
            return redirect(url_for('jinetes_amazonas.editar', id=id))
        
    terapeutas= Empleado.query.filter(Empleado.puesto_laboral.in_(['Terapeuta', 'Profesor de Equitación', 'Docente de Capacitación'])).all()
    auxiliares= Empleado.query.filter_by(puesto_laboral='Auxiliar de pista').all()
    caballos= Encuestre.query.all()
    conductores= Empleado.query.filter_by(puesto_laboral='Conductor').all()
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    return render_template("jinetes_amazonas/editar_jinete.html", jinete=jinete_amazonas_aux, fecha_hoy=fecha_hoy, terapeutas=terapeutas, auxiliares=auxiliares, caballos=caballos, conductores=conductores)

@jinete_amazonas_bp.route('/filtrar_caballos', methods=['GET'])
def filtrar_caballos():
    """
    Controlador para filtrar caballos según la propuesta de trabajo y la sede.
    
    Este endpoint permite a los usuarios filtrar los caballos disponibles en 
    la base de datos basándose en la propuesta de trabajo o en la sede asignada.
    

    Returns:
        JSON: Lista de caballos filtrados con su id y nombre.
    """
    propuesta_trabajo = request.args.get('propuesta_trabajo')
    sede = request.args.get('sede')     

    print("sedeeeeeeeeeeee--------------------------> ", sede)

    # Crear una consulta base
    query = Encuestre.query

    # Añadir filtros opcionales basados en los parámetros presentes
    if propuesta_trabajo and sede == "":
        query = query.filter(Encuestre.tipo_ja_asignado == propuesta_trabajo)
    if sede and propuesta_trabajo == "":
        query = query.filter(Encuestre.sede_asignada == sede)

    # Ejecutar la consulta
    caballos = query.all()

    # Serializar los caballos en formato JSON
    caballos_data = [{"id": caballo.id, "nombre": caballo.nombre} for caballo in caballos]

    return jsonify({"caballos": caballos_data})



# Eliminar un Jinete o Amazona
@jinete_amazonas_bp.route("/eliminar/<int:id>", methods=['POST'])
@check("ja_destroy")
def eliminar(id):
    """
    Elimina un Jinete o Amazona de la base de datos.

    :param id: ID del jinete/amazona a eliminar.
    :return: Redirige a la página de índice de jinetes y amazonas.
    """
    jinete_amazonas_aux = jinetes_amazonas.JineteAmazona.query.get_or_404(id)
    
    try:
        db.session.delete(jinete_amazonas_aux)
        db.session.commit()
        flash('Jinete o Amazona eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('jinetes_amazonas.index'))


@jinete_amazonas_bp.route('/subir_documento', methods=['POST'])
@check("ja_new")
def subir_documento():
    """
    Permite seleccionar un documento. Valida los campos del documento, nombre, tamaño y extension. Y lo
    asocia al jinete/amazona accedido

    :return: Redirige a la página de detalles del jinete/amazona o muestra mensajes de error.
    """
    MAX_FILE_SIZE = 16 * 1024 * 1024

    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('jinetes_amazonas.detalle', id=request.form.get('jinete_amazonas_id')))
    
    file = request.files['file']
    tipo_documento = request.form.get('tipo_documento')

    client = current_app.storage.client

    file_size = os.fstat(file.fileno()).st_size
    
    if file_size > MAX_FILE_SIZE:
        flash('El archivo excede el tamaño máximo permitido (16MB)', 'error')
        return redirect(url_for('jinetes_amazonas.detalle', id=request.form.get('jinete_amazonas_id')))
    
    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(url_for('jinetes_amazonas.detalle', id=request.form.get('jinete_amazonas_id')))

    try:
        client.put_object(
            'grupo49',
            f'documentos_jinetes_amazonas/{file.filename}',
            file,
            file_size,
            content_type=file.content_type
        )
        
        # Obtener el jinete o amazona asociado
        jinete_amazonas_id = request.form.get('jinete_amazonas_id')
        jinete_amazonas_aux = jinetes_amazonas.JineteAmazona.query.get(jinete_amazonas_id)
        
        # Crear el documento y asociarlo al jinete o amazona
        nuevo_documento = documento_jinete.DocumentoJinete(
            titulo=file.filename,
            tipo=tipo_documento,
            url=f"{current_app.config['MINIO_SERVER']}/grupo49/{file.filename}",
            jinete_amazona=jinete_amazonas_aux
        )
        
        db.session.add(nuevo_documento)
        db.session.commit()
        
        flash('Documento subido exitosamente', 'success')
    except Exception as e:
        flash(f'Error al subir el documento: {str(e)}', 'error')

    return redirect(url_for('jinetes_amazonas.detalle', id=jinete_amazonas_id))


@jinete_amazonas_bp.route('/descargar_documento/<int:document_id>')
@check("ja_show")
def descargar_documento(document_id):
    """
    Descargar documento existente o redirige al enlace.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige al enlace del documento o al detalle del jinete/amazona, dependiendo si es un enlace o un documento o retorna error. 
    """
    documento = documento_jinete.DocumentoJinete.query.get_or_404(document_id)

    if documento is None:
        flash('No se encontro el documento/enlace.', 'danger')
        return redirect(url_for('jinetes_amazonas.index'))
    
    jinete = documento_jinete.DocumentoJinete.get_jinete_by_document_id(document_id)
    client = current_app.storage.client
    object_name = f'documentos_jinetes_amazonas/{documento.titulo}'
    
    try: 
        if(documento.is_document):
            url_descarga = url_for('jinetes_amazonas.detalle', id=jinete.id)
            response = client.get_object("grupo49", object_name)
            doc = io.BytesIO(response.read())
            flash('El documento se ha descargado con éxito.', 'success')
            return send_file(doc, as_attachment=True, download_name=documento.titulo)
            
        else: 
            url_descarga = documento.url
    except Exception as e: 
        flash(f'Error en la descarga: {str(e)}', 'danger')



    return redirect(url_descarga)

@jinete_amazonas_bp.route('/eliminar_documento/<int:document_id>', methods=['POST'])
@check("ja_destroy")
def eliminar_documento(document_id):
    """
    Elimina el documento o enlace existente.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige al detalle del jinete/amazona o retorna error.
    """
    documento = documento_jinete.DocumentoJinete.query.get_or_404(document_id)

    if documento.is_document:
        eliminar_de_minio(documento.titulo)

    try:
        db.session.delete(documento)
        db.session.commit()

        flash('Documento eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el documento: {str(e)}', 'danger')

    return redirect(url_for('jinetes_amazonas.detalle', id=documento.jinete_amazonas_id))


def eliminar_de_minio(file):
    """
    Elimina el documento existente de minio.
    
    :param file: titulo del documento.
    """
    client = current_app.storage.client
    object_name = f'documentos_jinetes_amazonas/{file}'
    client.remove_object('grupo49', object_name)


@jinete_amazonas_bp.route('/editar_documento/<int:document_id>', methods=['POST', 'GET'])
@check("ja_update")
def editar_documento(document_id):
    """
    Edita el documento o enlace existente.
    
    :param documento_id: ID del documento/enlace a descargar.
    :return: Redirige a la plantilla encuestre/editar_documento.html  si el método es get, y si el métodoe es post al detalle del jinete/amazona o retorna error.
    """
    documento = documento_jinete.DocumentoJinete.query.get_or_404(document_id)
    jinete_amazonas = documento_jinete.DocumentoJinete.get_jinete_by_document_id(document_id)
    tipo = documento.tipo
    if documento is None:
        abort(404)

    if request.method == 'POST':
        if(documento.is_document):

            objeto_anterior =  f'documentos_jinetes_amazonas/{documento.titulo}'

            documento.titulo = request.form['nombre']    
            documento.tipo = request.form['tipo_documento']

            objeto_nuevo =  f'documentos_jinetes_amazonas/{documento.titulo}'

            try: 
                client = current_app.storage.client

                response = client.get_object('grupo49', objeto_anterior)
                file_data = response.read() 
                file_stream = BytesIO(file_data)
                
                client.put_object(
                    'grupo49', 
                    objeto_nuevo, 
                    file_stream, 
                    length=len(file_data), 
                    content_type=response.headers.get('Content-Type')
                )
                
            
                client.remove_object('grupo49', objeto_anterior)
            except Exception as e:
                flash(f'Error al renombrar el archivo en MinIO: {str(e)}', 'error')
                return redirect(url_for('jinetes_amazonas.editar_documento', document_id=document_id))
        else:  
            documento.titulo = request.form['nombre']
            documento.tipo = request.form['tipo_documento']

        # Guardar cambios en la base de datos
        db.session.commit()
        flash('Los cambios se han guardado exitosamente.', 'success')
        return redirect(url_for('jinetes_amazonas.detalle', id=jinete_amazonas.id))

    return render_template('jinetes_amazonas/editar_documento.html', documento=documento, jinete_amazonas=jinete_amazonas, tipo=tipo)


@jinete_amazonas_bp.route('/subir_enlace', methods=['POST'])
@check("ja_new")
def subir_enlace():
    """
    Registra un enlace en la base de datos en la tabla de documentos.

    :return: Redirige al detalle del jinete/amazona o retorna error.
    """
    jinete_amazonas_id = request.form.get('jinete_amazonas_id')
    jinete_amazonas_aux = jinetes_amazonas.JineteAmazona.query.get(jinete_amazonas_id)
    tipo_enlace = request.form.get('tipo_documento')

    titulo = request.form.get('titulo')
    url_enlace = request.form.get('enlace')

    # Valida que no se suban enlaces vacíos
    if not url_enlace:
        flash('El enlace no puede estar vacío', 'error')
        return redirect(url_for('jinetes_amazonas.detalle', id=jinete_amazonas_id))

    # Agregar el enlace como un objeto separado de documentos
    nuevo_enlace = documento_jinete.DocumentoJinete(
        titulo=url_enlace,
        tipo=tipo_enlace,
        url=url_enlace,
        jinete_amazona=jinete_amazonas_aux,
        is_document=False
    )
    
    db.session.add(nuevo_enlace)
    db.session.commit()

    flash('Enlace subido exitosamente', 'success')
    return redirect(url_for('jinetes_amazonas.detalle', id=jinete_amazonas_id))
