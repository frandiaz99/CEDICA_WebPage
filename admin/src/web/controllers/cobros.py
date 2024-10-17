from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.core.cobros import Cobro
from src.core.database import db
from src.web.handlers.auth import check
from src.core.equipo import Empleado
from datetime import datetime
from src.web.validadores.validador import (validar_tipo_pago, validar_monto, validar_fecha_pago, validar_descripcion, validar_beneficiario)
cobros_bp = Blueprint('cobros', __name__, url_prefix='/cobros')

@cobros_bp.get('/')
@check("registro_cobros_index")
def index():
    tipo_pago = request.args.get('tipo_pago')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    orden = request.args.get('orden', 'asc')  # Obtener el parámetro de orden, por defecto es 'asc'

    query = Cobro.query

    if fecha_inicio and fecha_fin:
        #Chequear que la fecha de inicio no sea mayor a la final y viceversa
        if fecha_inicio > fecha_fin:
            cobros = query.all()
            flash("El rango de fechas ingresado es inválido.", 'danger')
            return render_template('cobros/cobros.html', cobros=cobros)
        # Filtrar por fechas y tipo de pago
        query = query.filter(Cobro.fecha_pago >= fecha_inicio)
        query = query.filter(Cobro.fecha_pago <= fecha_fin)
        
    if tipo_pago:
        query = query.filter(Cobro.tipo_pago == tipo_pago)

    cobros = query.all()

    for cobro in cobros:
        empleado = Empleado.query.filter_by(id=cobro.beneficiario).first()
        if empleado:
            cobro.beneficiario = empleado.nombre +" "+ empleado.apellido

    if nombre:
        cobros = [cobro for cobro in cobros if nombre.lower() in cobro.beneficiario.lower()]
    if apellido:
        cobros = [cobro for cobro in cobros if apellido.lower() in cobro.beneficiario.lower()]

    # Ordenar resultados
    if orden == 'desc':
        query = query.order_by(Cobro.fecha_pago.desc())
    else:
        query = query.order_by(Cobro.fecha_pago.asc())

    return render_template('cobros/cobros.html', cobros=cobros)

@cobros_bp.route('/registrar', methods=['GET', 'POST'])
@check("registro_cobros_new")
def registrar_cobro():
    if request.method == 'POST':
        # Obtener datos del formulario
        jinete = request.form['jinete'] #Cuando este la db J&A, cambiar en select para que no sea siempre 1.
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        deuda = request.form.get('deuda')
        observaciones = request.form['observaciones']
        beneficiario = request.form['beneficiario']

        # Validadores de los campos
        validadores = [
            (validar_tipo_pago, [tipo_pago]),
            (validar_monto, [monto]),
            (validar_fecha_pago, [fecha_pago_str]),
            (validar_descripcion, [observaciones]),
            (validar_beneficiario, [beneficiario])
        ]

        # Validar cada campo
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('cobros.registrar_cobro'))  # Redirige si hay error

        # Crear el nuevo cobro
        if deuda == 'si':
            deuda = True
        else:
            deuda = False
        nuevo_cobro = Cobro(
            id_ja = jinete,
            fecha_pago=datetime.strptime(fecha_pago_str, '%Y-%m-%d'),
            tipo_pago=tipo_pago,
            monto=float(monto),
            beneficiario=beneficiario,
            en_deuda = deuda,
            observaciones=observaciones
        )

        # Guardar en la base de datos
        try:
            db.session.add(nuevo_cobro)
            db.session.commit()
            flash('El cobro ha sido registrado.', 'success')
            return redirect(url_for('cobros.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el cobro: {str(e)}', 'danger')
            return redirect(url_for('cobros.registrar_cobro'))

    empleados = Empleado.query.all()
    return render_template('cobros/registrar_cobro.html', empleados=empleados,fecha_hoy=datetime.today().date())

@cobros_bp.route('/detalle/<int:id>', methods=['GET'])
@check("registro_cobros_show")
def detalle_cobro(id):
    cobro = Cobro.query.get(id)
    if cobro is None:
        abort(404) 
    beneficiario = Empleado.query.filter_by(id=cobro.beneficiario).first()
    if beneficiario:
        cobro.beneficiario = beneficiario.nombre +" "+ beneficiario.apellido  
    return render_template('cobros/detalle_cobro.html', cobro=cobro)

@cobros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("registro_cobros_update")
def editar_cobro(id):
    cobro = Cobro.query.get(id)
    if cobro is None:
        abort(404) 

    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        observaciones = request.form['observaciones']
        en_deuda = request.form['deuda']
        beneficiario = request.form['beneficiario']

        # Validadores de los campos
        validadores = [
            (validar_tipo_pago, [tipo_pago]),
            (validar_monto, [monto]),
            (validar_fecha_pago, [fecha_pago_str]),
            (validar_descripcion, [observaciones]),
            (validar_beneficiario, [beneficiario])
        ]

        if en_deuda == 'si':
            en_deuda = True
        else:
            en_deuda = False

        # Validar cada campo
        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('cobros.editar_cobro', id=id))  # Redirige si hay error

        # Actualizar los campos del pago
        cobro.tipo_pago = tipo_pago
        cobro.monto = float(monto)
        cobro.fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d')
        cobro.observaciones = observaciones
        cobro.en_deuda = en_deuda
        cobro.beneficiario = beneficiario

        # Guardar los cambios en la base de datos
        try:
            db.session.commit()
            flash('El cobro se ha actualizado.', 'success')
            return redirect(url_for('cobros.detalle_cobro', id=cobro.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cobro: {str(e)}', 'danger')
            return redirect(url_for('cobros.editar_cobro', id=id))
    empleados = Empleado.query.all()
    return render_template(
        'cobros/editar_cobro.html', 
        cobro=cobro, 
        empleados=empleados,
        fecha_hoy=datetime.today().date()
    )

@cobros_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("registro_cobros_destroy")
def eliminar_cobro(id):

    cobro = Cobro.query.get_or_404(id)
    
    try:
        db.session.delete(cobro)
        db.session.commit()
        flash('Cobro eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el cobro: {str(e)}', 'danger')
    return redirect(url_for('cobros.index'))
