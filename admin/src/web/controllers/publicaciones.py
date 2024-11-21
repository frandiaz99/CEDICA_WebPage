from flask import Blueprint, render_template, request, abort, flash, url_for, redirect
from src.core.database import db
from sqlalchemy import asc, desc
from datetime import datetime
from src.core.publicacion import Publicacion
from src.core.auth import User
from src.web.validadores.validador import validar_fecha_publicacion, validar_contenido, validar_titulo, validar_copete   
from src.web.handlers.auth import check

publicaciones_bp = Blueprint('publicaciones', __name__, url_prefix='/publicaciones')

@publicaciones_bp.get("/")
@check("administracion_index")
def index():
    """
    Muestra una lista de publicaciones con paginación y filtros de búsqueda por estado y orden por fecha de creación.

    :return: Renderiza la plantilla 'publicaciones/publicaciones.html' con las publicaciones.
    """
    registros_por_pagina = 5
    estado = request.args.get('estado', '')
    order = request.args.get('order', 'asc')
    pagina = int(request.args.get('pagina', 1))

    query = Publicacion.query

    if estado:
        query = query.filter(Publicacion.estado == estado)

    if order == 'asc':
        query = query.order_by(asc(Publicacion.inserted_at))
    else:
        query = query.order_by(desc(Publicacion.inserted_at))

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    publicaciones = pagination.items
    total_paginas = pagination.pages
    autores = User.query.all()

    return render_template(
        "publicaciones/publicaciones.html",
        publicaciones=publicaciones,
        estado=estado,
        order=order,
        pagina=pagina,
        total_paginas=total_paginas,
        autores = autores
    )

@publicaciones_bp.route('/registrar', methods=['GET', 'POST'])
@check("administracion_new")
def crear_publicacion():
    """
    Permite registrar una nueva publicación. Valida los datos ingresados antes de guardarlos en la base de datos.
    """
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        alias_autor = request.form['autor']
        estado = request.form.get('estado')
        copete = request.form.get('copete')
        contenido = request.form.get('contenido')

        fecha_publicacion = None
        if estado == "publicado":
            fecha_publicacion = datetime.today().date().strftime('%Y-%m-%d')
            validadores = [
                (validar_fecha_publicacion, [fecha_publicacion]),
                (validar_titulo, [titulo]),
                (validar_copete, [copete]),
                (validar_contenido, [contenido])
            ]
            mensajes_error = []
            for validar_funcion, args in validadores:
                es_valido, mensaje_error = validar_funcion(*args)
                if not es_valido:
                    # Agregar mensaje de error a la lista
                    mensajes_error.append(mensaje_error)
            if mensajes_error:
                for mensaje in mensajes_error:
                    flash(mensaje, 'danger')
                return redirect(url_for('publicaciones.crear_publicacion'))

        # Crear y guardar
        nueva_publicacion = Publicacion(
            titulo=titulo,
            autor=alias_autor,
            estado=estado,
            fecha_publicacion=fecha_publicacion,
            copete=copete,
            contenido=contenido
        )

        try:
            db.session.add(nueva_publicacion)
            db.session.commit()
            flash('Publicación registrada correctamente.', 'success')
            return redirect(url_for('publicaciones.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la publicación: {str(e)}', 'danger')
            return redirect(url_for('publicaciones.crear_publicacion'))

    autores = User.query.all()
    return render_template('publicaciones/crear_publicacion.html', autores=autores, fecha_hoy=datetime.today().date())

@publicaciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("administracion_update")
def editar_publicacion(id):
    """
    Permite editar una publicación.
    
    Args:
        id (int): El ID de la publicacion a editar.
    """
    publicacion_aux = Publicacion.query.get(id)
    if not publicacion_aux:
        abort(404)

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        estado = request.form.get('estado')
        fecha_publicacion = request.form['fecha_publicacion']
        copete = request.form.get('copete')
        contenido = request.form.get('contenido')

        if fecha_publicacion == "":
            fecha_publicacion = None

        if estado == "publicado":
            validadores = [
                (validar_fecha_publicacion, [fecha_publicacion]),
                (validar_titulo, [titulo]),
                (validar_copete, [copete]),
                (validar_contenido, [contenido])
            ]
            mensajes_error = []
            for validar_funcion, args in validadores:
                es_valido, mensaje_error = validar_funcion(*args)
                if not es_valido:
                    # Agregar mensaje de error a la lista
                    mensajes_error.append(mensaje_error)
            if mensajes_error:
                for mensaje in mensajes_error:
                    flash(mensaje, 'danger')
                return redirect(url_for('publicaciones.crear_publicacion'))

        publicacion_aux.titulo = titulo
        publicacion_aux.estado = estado
        publicacion_aux.fecha_publicacion = fecha_publicacion
        publicacion_aux.updated_at = datetime.today().date()
        publicacion_aux.copete = copete
        publicacion_aux.contenido = contenido

        try:
            db.session.commit()
            flash('La publicación ha sido actualizada.', 'success')
            return redirect(url_for('publicaciones.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la publicacion: {str(e)}', 'danger')
            return redirect(url_for('publicaciones.editar_publicacion', id=id))
        
    autores = User.query.all()

    return render_template(
        'publicaciones/editar_publicacion.html', 
        publicacion=publicacion_aux,
        autores=autores,
        fecha_hoy=datetime.today().date(),
        fecha_min=publicacion_aux.inserted_at.strftime('%Y-%m-%d')
    )

@publicaciones_bp.route('/detalle/<int:id>', methods=['GET'])
@check("administracion_show")
def detalle_publicacion(id):
    """
    Muestra la info adicional de una publicación.
    
    Args:
        id (int): El ID de la publicacion a mostrar.
    """
    publicacion = Publicacion.query.get(id)
    if not publicacion:
        abort(404)

    return render_template('publicaciones/detalle_publicacion.html', publicacion=publicacion)

@publicaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("administracion_destroy")
def eliminar_publicacion(id):
    """
    Elimina una publicacion de la base de datos.

    :param id: ID de la publicacion a eliminar.
    :return: Redirige a la página de índice de la publicacion.
    """
    publicacion_aux = Publicacion.query.get_or_404(id)

    try:
        db.session.delete(publicacion_aux)
        db.session.commit()
        flash('Publicación eliminada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la publicación: {str(e)}', 'danger')

    return redirect(url_for('publicaciones.index'))