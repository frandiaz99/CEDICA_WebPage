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
        beneficiario = Empleado.query.filter_by(id=cobro.beneficiario).first()
        if beneficiario:
            cobro.beneficiario = beneficiario.nombre +" "+ beneficiario.apellido
        if nombre:
            query = query.filter(cobro.beneficiario.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(cobro.beneficiario.ilike(f"%{apellido}%"))

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
@check("registro_cobro_show")
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
