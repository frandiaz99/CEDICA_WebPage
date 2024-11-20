from flask import Blueprint, render_template, request, abort, flash, url_for, redirect, current_app, send_file
from src.core.database import db
from sqlalchemy import asc, desc
from src.core.contacto import Contacto
from src.web.validadores.validador import ( validar_estado, validar_comentario )    
from src.web.handlers.auth import check

contacto_bp = Blueprint('contacto', __name__, url_prefix='/contacto')

@contacto_bp.get("/")
@check("contacto_index")
def index():
    """
    Controlador para la página de inicio de contacto. Muestra una lista de contactos con
    paginación y filtros de búsqueda por estado y orden por fecha de creación.

    :return: Renderiza la plantilla 'contacto/contacto.html' con los contactos y parámetros de búsqueda.
    """
    registros_por_pagina = 5
    estado = request.args.get('estado', '')
    order = request.args.get('order', 'asc')
    pagina = int(request.args.get('pagina', 1))

    query = Contacto.query

    if estado:
        query = query.filter(Contacto.estado == estado)

    if order == 'asc':
        query = query.order_by(asc(Contacto.inserted_at))
    else:
        query = query.order_by(desc(Contacto.inserted_at))

    pagination = query.paginate(page=pagina, per_page=registros_por_pagina)
    contactos = pagination.items
    total_paginas = pagination.pages

    return render_template(
        "contacto/contacto.html",
        contactos=contactos,
        estado=estado,
        order=order,
        pagina=pagina,
        total_paginas=total_paginas
    )


@contacto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("contacto_update")
def editar_contacto(id):
    """
    Permite editar un contacto existente. Solo permite modificar el comentario y el estado.
    
    Args:
        id (int): El ID del contacto a editar.
    """
    contacto_aux = Contacto.query.get(id)
    if not contacto_aux:
        abort(404)

    if request.method == 'POST':
        estado = request.form['estado']
        comentario = request.form['comentario']

        validadores = [
            (validar_estado, [estado]),
            (validar_comentario, [comentario])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('contacto.editar_contacto', id=id))

        contacto_aux.estado = estado
        contacto_aux.comentario = comentario

        try:
            db.session.commit()
            flash('El contacto se ha actualizado exitosamente.', 'success')
            return redirect(url_for('contacto.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el contacto: {str(e)}', 'danger')
            return redirect(url_for('contacto.editar_contacto', id=id))

    return render_template(
        'contacto/editar_contacto.html', 
        contacto=contacto_aux,
    )

@contacto_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("contacto_destroy")
def eliminar_contacto(id):
    """
    Elimina un contacto de la base de datos.

    :param id: ID del contacto a eliminar.
    :return: Redirige a la página de índice del contacto.
    """
    contacto_aux = Contacto.query.get_or_404(id)

    try:
        db.session.delete(contacto_aux)
        db.session.commit()
        flash('Contacto eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el contacto: {str(e)}', 'danger')

    return redirect(url_for('contacto.index'))