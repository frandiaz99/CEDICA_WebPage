from src.core import auth
from src.core.auth import User
from flask import render_template, Blueprint, abort, request, flash, redirect, url_for, jsonify
from sqlalchemy import asc, desc
from src.web.handlers.auth import login_required
from math import ceil
from src.core.database import db
from datetime import datetime


users_bp = Blueprint("users", __name__, url_prefix="/users")

def chequearMailRepetido (email):
    query = User.query  
    if (query.filter(User.email == email).all()):
        flash('El mail ingresado ya tiene una cuenta asociada.', 'danger')
        return False
    return True

@users_bp.get("/")
@login_required
def index():

    roles = auth.list_roles()
    roles_dict = {role.id: role for role in roles}

    registros_por_pagina = 10  # Puedes ajustar la cantidad de empleados por página

    # Obtener parámetros de búsqueda y orden desde la URL
    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'email')  # Por defecto 'email'
    actividad = request.args.get('actividad', 'todos')
    order = request.args.get('order', 'asc')  # Por defecto ascendente
    order_prop = request.args.get('order_prop', 'email')
    pagina = request.args.get('pagina', 1, type=int)

    # Construir la query base
    query = User.query

    # Filtrar según el campo seleccionado (filter_by y actividad)
    if search:
        if filter_by == 'email':
            query = query.filter(User.email.ilike(f'%{search}%'))
        elif filter_by == 'alias':
            query = query.filter(User.alias.ilike(f'%{search}%'))
        elif filter_by == 'rol':
            role_ids = list(roles_dict.keys())
            query = query.filter(User.rol_id.in_(role_ids))
        if actividad == 'si':
            query = query.filter(User.activo == True)
        elif actividad == 'no':
            query = query.filter(User.activo == False)
    
    # Adicionalmente, ordenar por order_prop si es distinto de filter_by
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(User, order_prop)))
        else:
            query = query.order_by(desc(getattr(User, order_prop)))

    # Si se quiere ordenar por mail o fecha de creación adicionalmente
    if order_prop == 'email':
        query = query.order_by(asc(User.email)) if order == 'asc' else query.order_by(desc(User.email))
    elif order_prop == 'inserted_at':
        query = query.order_by(asc(User.inserted_at)) if order == 'asc' else query.order_by(desc(User.inserted_at))

    # Contar el total de registros que cumplen con los criterios de búsqueda
    total_registros = query.count()

    # Calcular cuántos registros hay que omitir dependiendo de la página
    offset = (pagina - 1) * registros_por_pagina

    # Aplicar límite y offset para la paginación
    users = query.offset(offset).limit(registros_por_pagina).all()

    # Calcular el total de páginas
    total_paginas = ceil(total_registros / registros_por_pagina)

    # Renderizar la plantilla y pasar parámetros
    return render_template(
        "users/listar_usuarios.html", 
        users=users, 
        roles=roles_dict,
        search=search, 
        filter_by=filter_by,
        actividad=actividad, 
        order=order,
        order_prop=order_prop,
        pagina=pagina,
        total_paginas=total_paginas
    )

@users_bp.route("/registrar_usuario", methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if request.method == 'POST':

        # Obtengo data
        alias = request.form.get('alias')
        email = request.form.get('email')
        activo = request.form.get('activo')
        contraseña1 = request.form.get('contraseña1')
        contraseña2 = request.form.get('contraseña2')

        if not (alias and email and activo and contraseña1 and contraseña2):
            flash('Faltan completar campos.', 'danger')
            return redirect(url_for('users.crear_usuario'))
        
        query = User.query  
        
        if (chequearMailRepetido):
            return redirect(url_for('users.crear_usuario'))
        
        if not (contraseña1 == contraseña2):
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('users.crear_usuario'))

        if (activo == 'Sí'):
            activo = True
        else:
            activo = False

        # Crear el nuevo Usuario
        nuevo_usuario = User(
            alias=alias,
            email=email,
            activo=activo,
            password=contraseña1
        )

        try:
            # Subir a la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('users.crear_usuario', id=nuevo_usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
            return redirect(url_for('users.crear_usuario'))

    return render_template('users/crear_usuario.html')

@users_bp.route('/detalle/<int:id>', methods=['GET'])
@login_required
def detalle_usuario(id):
    user = auth.User.query.get(id)
    if user is None:
        abort(404)  # error 404 si no se encuentra el usuario
    return render_template("users/detalle_usuario.html", user=user)

@users_bp.route('/bloquear_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
def bloquear_usuario(id):
    user = auth.User.query.get(id)
    if user is None:
        abort(404)  # error 404 si no se encuentra el usuario
    user.activo = False
    db.session.commit()
    flash('Usuario bloqueado.', 'success')
    return redirect(url_for('users.index'))

@users_bp.route('/desbloquear_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
def desbloquear_usuario(id):
    user = auth.User.query.get(id)
    if user is None:
        abort(404)  # error 404 si no se encuentra el usuario
    user.activo = True
    db.session.commit()
    flash('Usuario desbloqueado.', 'success')
    return redirect(url_for('users.index'))

@users_bp.route('/actualizar_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
def actualizar_usuario(id):
    user = auth.User.query.get(id)
    roles = auth.list_roles()
    roles_dict = {role.id: role for role in roles}
    if user is None:
        abort(404)  # error 404 si no se encuentra el usuario

    #Prevenis que no se ejecute al apretar el boton editar
    if request.method == 'POST':
        alias = request.form.get('alias')
        email = request.form.get('email')
        activo = request.form.get('activo')
        rol = request.form.get('rol')
        rol = int(rol)
        #Buscar en la lista de roles aquel rol que coincida el id con "rol"
        rol_encontrado = next((r for r in roles if r.id == rol), None)

        if not (alias or email or activo):
            flash('Faltan campos por completar.', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))
        
        query = User.query  
        existing_user = User.query.filter(User.email == email, User.id != id).first()
        if (existing_user):
            flash('El email ingresado ya tiene una cuenta asociada.', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))
        
        if (activo == 'Sí'):
            activo = True
        else:
            activo = False

        user.alias = alias
        user.email = email
        user.activo = activo
        user.rol = rol_encontrado
        user.updated_at = datetime.now()

        try:
            db.session.commit()
            flash('El usuario ha sido actualizado.', 'success')
            return redirect(url_for('users.actualizar_usuario', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))

    return render_template("users/actualizar_usuario.html", user=user, roles=roles_dict)

@users_bp.route('/eliminar_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
def eliminar_usuario(id):
    user = auth.User.query.get(id)
    if user is None:
        abort(404)  # error 404 si no se encuentra el usuario
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('El usuario ha sido eliminado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {str(e)}', 'danger')

    return redirect(url_for('users.index'))