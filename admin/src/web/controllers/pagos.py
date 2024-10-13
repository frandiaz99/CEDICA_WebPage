from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.core.registro_pagos import Pago
from src.core.database import db
from src.web.handlers.auth import check
from src.core.equipo import Empleado
from datetime import datetime
from src.web.controllers.validador import (
    validar_tipo_pago, validar_monto, validar_fecha_pago, validar_descripcion, validar_beneficiario
)

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')


@pagos_bp.get('/')
@check("registro_pagos_index")
def index():
    """
    Muestra la lista de pagos con posibilidad de filtrado por tipo de pago, 
    fecha de inicio, fecha de fin, y permite ordenar los resultados por fecha.
    """
    tipo_pago = request.args.get('tipo_pago')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    orden = request.args.get('orden', 'asc')  # Ordenar por defecto en ascendente

    query = Pago.query

    # Filtrar por fechas y tipo de pago
    if fecha_inicio:
        query = query.filter(Pago.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Pago.fecha_pago <= fecha_fin)
    if tipo_pago:
        query = query.filter(Pago.tipo_pago == tipo_pago)

    # Ordenar resultados
    if orden == 'desc':
        query = query.order_by(Pago.fecha_pago.desc())
    else:
        query = query.order_by(Pago.fecha_pago.asc())

    pagos = query.all()

    # Agregar el nombre completo del beneficiario a cada pago
    for pago in pagos:
        beneficiario = Empleado.query.filter_by(id=pago.beneficiario).first()
        if beneficiario:
            pago.beneficiario = beneficiario.nombre + " " + beneficiario.apellido

    return render_template('pagos/pagos.html', pagos=pagos)


@pagos_bp.route('/registrar', methods=['GET', 'POST'])
@check("registro_pagos_new")
def registrar_pago():
    """
    Permite registrar un nuevo pago. Valida los datos ingresados antes de guardarlos en la base de datos.
    """
    if request.method == 'POST':
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        descripcion = request.form['descripcion']
        beneficiario = request.form['beneficiario']

        # Validar los campos del formulario
        validadores = [
            (validar_tipo_pago, [tipo_pago]),
            (validar_monto, [monto]),
            (validar_fecha_pago, [fecha_pago_str]),
            (validar_descripcion, [descripcion]),
            (validar_beneficiario, [beneficiario])
        ]

        # Validar cada campo
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('pagos.registrar_pago'))

        # Crear y guardar el nuevo pago
        nuevo_pago = Pago(
            tipo_pago=tipo_pago,
            monto=float(monto),
            fecha_pago=datetime.strptime(fecha_pago_str, '%Y-%m-%d'),
            descripcion=descripcion,
            beneficiario=beneficiario
        )

        try:
            db.session.add(nuevo_pago)
            db.session.commit()
            flash('Pago registrado exitosamente.', 'success')
            return redirect(url_for('pagos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el pago: {str(e)}', 'danger')
            return redirect(url_for('pagos.registrar_pago'))

    empleados = Empleado.query.all()
    return render_template('pagos/registrar_pago.html', empleados=empleados, fecha_hoy=datetime.today().date())


@pagos_bp.route('/detalle/<int:id>', methods=['GET'])
@check("registro_pagos_show")
def detalle_pago(id):
    """
    Muestra los detalles de un pago específico.
    
    Args:
        id (int): El ID del pago a mostrar.
    """
    pago = Pago.query.get(id)
    if not pago:
        abort(404)

    beneficiario = Empleado.query.filter_by(id=pago.beneficiario).first()
    if beneficiario:
        pago.beneficiario = beneficiario.nombre + " " + beneficiario.apellido

    return render_template('pagos/detalle_pago.html', pago=pago)


@pagos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("registro_pagos_update")
def editar_pago(id):
    """
    Permite editar un pago existente. Valida los datos antes de guardar los cambios en la base de datos.
    
    Args:
        id (int): El ID del pago a editar.
    """
    pago_aux = Pago.query.get(id)
    if not pago_aux:
        abort(404)

    if request.method == 'POST':
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        descripcion = request.form['descripcion']
        beneficiario = request.form['beneficiario']

        # Validar los campos del formulario
        validadores = [
            (validar_tipo_pago, [tipo_pago]),
            (validar_monto, [monto]),
            (validar_fecha_pago, [fecha_pago_str]),
            (validar_descripcion, [descripcion]),
            (validar_beneficiario, [beneficiario])
        ]

        # Validar cada campo
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('pagos.editar_pago', id=id))

        # Actualizar los campos del pago
        pago_aux.tipo_pago = tipo_pago
        pago_aux.monto = float(monto)
        pago_aux.fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d')
        pago_aux.descripcion = descripcion
        pago_aux.beneficiario = beneficiario

        # Guardar los cambios en la base de datos
        try:
            db.session.commit()
            flash('El pago se ha actualizado exitosamente.', 'success')
            return redirect(url_for('pagos.detalle_pago', id=pago_aux.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el pago: {str(e)}', 'danger')
            return redirect(url_for('pagos.editar_pago', id=id))

    empleados = Empleado.query.all()
    return render_template(
        'pagos/editar_pago.html', 
        pago=pago_aux, 
        empleados=empleados,
        fecha_hoy=datetime.today().date()
    )


@pagos_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("registro_pagos_destroy")
def eliminar_pago(id):
    """
    Elimina un pago de la base de datos.
    
    Args:
        id (int): El ID del pago a eliminar.
    """
    pago_aux = Pago.query.get_or_404(id)

    try:
        db.session.delete(pago_aux)
        db.session.commit()
        flash('Pago eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el pago: {str(e)}', 'danger')

    return redirect(url_for('pagos.index'))
