from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from src.core.cobros import Cobro
from src.core.database import db
from src.web.handlers.auth import check
from src.core.equipo import Empleado
from src.core.jinetes_amazonas import JineteAmazona
from datetime import datetime
from src.web.validadores.validador import (validar_tipo_pago, validar_monto, validar_fecha_pago, validar_descripcion, validar_beneficiario)

cobros_bp = Blueprint('cobros', __name__, url_prefix='/cobros')



@cobros_bp.get('/')
@check("registro_cobros_index")
def index():
    """
    Muestra la lista de cobros que hay en el sistema, permitiendo filtrar por las diferentes opciones disponibles.
    """
    tipo_pago = request.args.get('tipo_pago')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    orden = request.args.get('orden', 'asc')

    query = Cobro.query

    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            cobros = query.all()
            flash("El rango de fechas ingresado es inválido.", 'danger')
            return render_template('cobros/cobros.html', cobros=cobros)
        query = query.filter(Cobro.fecha_pago >= fecha_inicio)
        query = query.filter(Cobro.fecha_pago <= fecha_fin)
        
    if tipo_pago:
        query = query.filter(Cobro.tipo_pago == tipo_pago)

    if orden == 'desc':
        query = query.order_by(Cobro.fecha_pago.desc())
    else:
        query = query.order_by(Cobro.fecha_pago.asc())

    cobros = query.all()

    for cobro in cobros:
        empleado = Empleado.query.filter_by(id=cobro.beneficiario).first()
        if empleado:
            cobro.beneficiario = empleado.nombre +" "+ empleado.apellido

    if nombre:
        cobros = [cobro for cobro in cobros if nombre.lower() in cobro.beneficiario.lower()]
    if apellido:
        cobros = [cobro for cobro in cobros if apellido.lower() in cobro.beneficiario.lower()]

    jinetes = JineteAmazona.query.all()

    return render_template('cobros/cobros.html', cobros=cobros, jinetes=jinetes)



@cobros_bp.route('/registrar', methods=['GET', 'POST'])
@check("registro_cobros_new")
def registrar_cobro():
    """
    Si el método es get, carga el template registrar_cobro.html, es decir, la página de carga de usuarios.
    Si el método es post, crea un nuevo cobro con los datos obtenidos del formulario.
    """
    jinetes = JineteAmazona.query.all()
    print(jinetes)
    if request.method == 'POST':
        jinete_id = request.form['jinete']
        tipo_pago = request.form['tipo_pago']
        monto = request.form['monto']
        fecha_pago_str = request.form.get('fecha_pago')
        deuda = request.form.get('deuda')
        observaciones = request.form['observaciones']
        beneficiario = request.form['beneficiario']

        validadores = [
            (validar_tipo_pago, [tipo_pago]),
            (validar_monto, [monto]),
            (validar_fecha_pago, [fecha_pago_str]),
            (validar_descripcion, [observaciones]),
            (validar_beneficiario, [beneficiario])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('cobros.registrar_cobro', jinetes))

        if deuda == 'si':
            deuda = True
        else:
            deuda = False
        nuevo_cobro = Cobro(
            id_ja = jinete_id,
            fecha_pago=datetime.strptime(fecha_pago_str, '%Y-%m-%d'),
            tipo_pago=tipo_pago,
            monto=float(monto),
            beneficiario=beneficiario,
            en_deuda = deuda,
            observaciones=observaciones
        )

        try:
            db.session.add(nuevo_cobro)
            db.session.commit()
            flash('El cobro ha sido registrado.', 'success')
            return redirect(url_for('cobros.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el cobro: {str(e)}', 'danger')
            return redirect(url_for('cobros.registrar_cobro', jinetes))

    empleados = Empleado.query.all()
    return render_template('cobros/registrar_cobro.html', empleados=empleados, jinetes=jinetes, fecha_hoy=datetime.today().date())



@cobros_bp.route('/detalle/<int:id>', methods=['GET'])
@check("registro_cobros_show")
def detalle_cobro(id):
    """
    Muestra más información sobre un cobro en concreto, si es que el id del mismo existe.

    - param id: el id del cobro.

    - return: carga la plantilla detalle_cobro.html con el cobro a mostrar.
    """
    cobro = Cobro.query.get(id)
    if cobro is None:
        abort(404) 
    beneficiario = Empleado.query.filter_by(id=cobro.beneficiario).first()
    if beneficiario:
        cobro.beneficiario = beneficiario.nombre +" "+ beneficiario.apellido  
    jinetes = JineteAmazona.query.all()
    return render_template('cobros/detalle_cobro.html', cobro=cobro, jinetes=jinetes)



@cobros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@check("registro_cobros_update")
def editar_cobro(id):
    """
    Si el metodo es get, carga la plantilla editar_cobro.html, es decir, la página para actualizar la info de un cobro, si es que el mismo existe.
    Si el método es post, carga la plantilla editar_cobro.html con los datos del cobro actualizados.

    - param id: id del cobro a actualizar.
    """
    cobro = Cobro.query.get(id)
    if cobro is None:
        abort(404) 

    jinetes = JineteAmazona.query.all()

    if request.method == 'POST':
        # Obtener datos del formulario
        jinete_id = request.form['jinete']
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
        cobro.id_ja = jinete_id
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
            return redirect(url_for('cobros.detalle_cobro', id=cobro.id, jinetes=jinetes))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cobro: {str(e)}', 'danger')
            return redirect(url_for('cobros.editar_cobro', id=id))
    empleados = Empleado.query.all()
    return render_template(
        'cobros/editar_cobro.html', 
        cobro=cobro, 
        empleados=empleados,
        fecha_hoy=datetime.today().date(),
        jinetes=jinetes
    )



@cobros_bp.route('/eliminar/<int:id>', methods=['POST'])
@check("registro_cobros_destroy")
def eliminar_cobro(id):
    """
    Elimina al cobro pasado por parámetro, si es que existe.

    - param id: id del cobro a eliminar.
    """
    cobro = Cobro.query.get_or_404(id)
    
    try:
        db.session.delete(cobro)
        db.session.commit()
        flash('Cobro eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el cobro: {str(e)}', 'danger')
    return redirect(url_for('cobros.index'))
