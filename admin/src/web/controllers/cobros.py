from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.core.registro_pagos import Pago
from src.core.database import db
from src.web.handlers.auth import check
from src.core.equipo import Empleado
from datetime import datetime
from src.web.controllers.validador import (validar_tipo_pago, validar_monto, validar_fecha_pago, validar_descripcion, validar_beneficiario)
cobros_bp = Blueprint('cobros', __name__, url_prefix='/cobros')

@cobros_bp.get('/')
@check("registro_cobros_index")
def index():
    tipo_pago = request.args.get('tipo_pago')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    orden = request.args.get('orden', 'asc')  # Obtener el parámetro de orden, por defecto es 'asc'

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

    if tipo_pago:
        query = query.filter_by(tipo_pago=tipo_pago)

    if fecha_inicio and fecha_fin:
        query = query.filter(Pago.fecha_pago.between(fecha_inicio, fecha_fin))

    # Obtener la lista de pagos
    pagos = query.order_by(Pago.fecha_pago.desc()).all()

    # Agregar el email del beneficiario a cada pago
    for pago in pagos:
        beneficiario = Empleado.query.filter_by(id=pago.beneficiario).first()
        if beneficiario:
            pago.beneficiario = beneficiario.nombre +" "+ beneficiario.apellido  # Asignar el correo al objeto pago

    return render_template('cobros/cobros.html', pagos=pagos)

@cobros_bp.route('/registrar', methods=['GET', 'POST'])
@check("registro_cobros_new")
def registrar_cobro():
    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        descripcion = request.form['descripcion']
        beneficiario = request.form['beneficiario']

        # Validadores de los campos
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
                return redirect(url_for('pagos.registrar_pago'))  # Redirige si hay error

        # Crear el nuevo pago
        nuevo_pago = Pago(
            tipo_pago=tipo_pago,
            monto=float(monto),
            fecha_pago=datetime.strptime(fecha_pago_str, '%Y-%m-%d'),
            descripcion=descripcion,
            beneficiario=beneficiario
        )

        # Guardar en la base de datos
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
    return render_template('pagos/registrar_pago.html', empleados=empleados,fecha_hoy=datetime.today().date())

@cobros_bp.route('/detalle/<int:id>', methods=['GET'])
@check("registro_cobro_show")
def detalle_cobro(id):
    pago = Pago.query.get(id)
    if pago is None:
        abort(404) 
    beneficiario = Empleado.query.filter_by(id=pago.beneficiario).first()
    if beneficiario:
        pago.beneficiario = beneficiario.nombre +" "+ beneficiario.apellido  
    return render_template('pagos/detalle_pago.html', pago=pago)

@cobros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("registro_cobros_update")
def editar_cobro(id):
    pago_aux = Pago.query.get(id)
    if pago_aux is None:
        abort(404) 

    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        descripcion = request.form['descripcion']
        beneficiario = request.form['beneficiario']

        # Validadores de los campos
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
                return redirect(url_for('pagos.editar_pago', id=id))  # Redirige si hay error

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

@cobros_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("registro_cobros_destroy")
def eliminar_cobro(id):
    # Buscar el pago por ID
    pago_aux = Pago.query.get_or_404(id)
    
    try:
        db.session.delete(pago_aux)
        db.session.commit()

        flash('Pago eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el pago: {str(e)}', 'danger')
    return redirect(url_for('pagos.index'))
