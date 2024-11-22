from src.core import auth
from src.core.auth import User
from src.web.handlers.auth import check
from flask import render_template, Blueprint, abort, request, flash, redirect, url_for, jsonify
from sqlalchemy import asc, desc
from src.web.handlers.auth import login_required
from math import ceil
from src.core.database import db
from datetime import datetime
from src.web.validadores.validador import (
    validar_email, chequear_email_repetido, validar_cont_coinciden,
    validar_string_numeros_o_vacio, validar_rol

)
from src.web.handlers import error 

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.get("/")
@login_required
@check("user_index")
def index():
    """
    Muestra la lista de usuarios que hay en el sistema, permitiendo filtrar por las diferentes opciones disponibles.
    """
    roles = auth.list_roles()
    roles_dict = {role.id: role for role in roles}

    registros_por_pagina = 10

    search = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'email')
    actividad = request.args.get('actividad', 'todos')
    order = request.args.get('order', 'asc')
    order_prop = request.args.get('order_prop', 'email')
    pagina = request.args.get('pagina', 1, type=int)

    query = User.query.filter(User.aceptado_google== True)

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
    
    if order_prop != filter_by:
        if order == 'asc':
            query = query.order_by(asc(getattr(User, order_prop)))
        else:
            query = query.order_by(desc(getattr(User, order_prop)))

    if order_prop == 'email':
        query = query.order_by(asc(User.email)) if order == 'asc' else query.order_by(desc(User.email))
    elif order_prop == 'inserted_at':
        query = query.order_by(asc(User.inserted_at)) if order == 'asc' else query.order_by(desc(User.inserted_at))

    total_registros = query.count()

    offset = (pagina - 1) * registros_por_pagina

    users = query.offset(offset).limit(registros_por_pagina).all()

    total_paginas = ceil(total_registros / registros_por_pagina)

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


@users_bp.get("/usuarios_google")
@login_required
@check("user_accept")
def index_google():
    """
    Muestra la lista de usuarios pendientes de aceptación por Google.

    Este endpoint obtiene a los usuarios que no han sido aceptados vía Google,
    paginando los resultados para una visualización más cómoda. Además, se incluyen
    los roles disponibles para su uso en la vista.

    Returns:
        Response: Renderiza la plantilla `users/listar_usuarios_google.html` con los datos
        de los usuarios, roles, página actual y total de páginas.
    """
    # Obtener los roles del sistema y construir un diccionario para un acceso más rápido
    roles = auth.list_roles()
    roles_dict = {role.id: role for role in roles}

    registros_por_pagina = 10  # Número de registros mostrados por página
    pagina = request.args.get('pagina', 1, type=int)  # Página actual, por defecto la primera

    # Filtrar usuarios que no han sido aceptados vía Google
    users = User.query.filter(User.aceptado_google == False)
    total_registros = users.count()  # Total de registros encontrados

    # Calcular el desplazamiento para la paginación
    offset = (pagina - 1) * registros_por_pagina
    users = users.offset(offset).limit(registros_por_pagina).all()  # Obtener registros de la página actual

    # Calcular el número total de páginas
    total_paginas = ceil(total_registros / registros_por_pagina)

    # Renderizar la plantilla con los datos necesarios
    return render_template(
        "users/listar_usuarios_google.html", 
        users=users, 
        roles=roles_dict,
        pagina=pagina,
        total_paginas=total_paginas
    )




@users_bp.route("/registrar_usuario", methods=['GET', 'POST'])
@login_required
@check("user_new")
def crear_usuario():
    """
    Si el método es get, carga el template crear_usuario.html, es decir, la página de carga de cobros.
    Si el método es post, crea un nuevo usuario con los datos obtenidos del formulario.
    """
    if request.method == 'POST':

        roles = auth.list_roles()

        alias = request.form.get('alias')
        email = request.form.get('email')
        activo = request.form.get('activo')
        cont1 = request.form.get('contraseña1')
        cont2 = request.form.get('contraseña2')
        
        if not (alias and email and activo and cont1 and cont2):
            flash('Faltan completar campos.', 'danger')
            return redirect(url_for('users.crear_usuario'))

        validadores = [
            (validar_email, [email]),
            (chequear_email_repetido, [email]),
            (validar_cont_coinciden, [cont1,cont2])
        ]

        for validar_funcion, args in validadores:
            es_valido, mensaje_error = validar_funcion(*args)
            if not es_valido:
                flash(mensaje_error, 'danger')
                return redirect(url_for('users.crear_usuario')) 
        
        if(not validar_string_numeros_o_vacio):
            flash("Ingresar un Alias valido")

        if (activo == 'Sí'):
            activo = True
        else:
            activo = False

        try:
        
            nuevo_usuario = auth.create_user(
                alias=alias,
                email=email,
                activo=activo,
                password=cont1,
            )

            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('users.crear_usuario', id=nuevo_usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
            return redirect(url_for('users.crear_usuario'))

    return render_template('users/crear_usuario.html')



@users_bp.route('/detalle/<int:id>', methods=['GET'])
@login_required
@check("user_show")
def detalle_usuario(id):
    """
    Muestra más información sobre un usuario en concreto, si es que el id del mismo existe.

    - param id: el id del usuario.

    - return: carga la plantilla detalle_usuario.html con el usuario a mostrar.
    """
    user = auth.User.query.get(id)
    if user is None:
        abort(404)
    return render_template("users/detalle_usuario.html", user=user)



@users_bp.route('/bloquear_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
@check("user_update")
def bloquear_usuario(id):
    """
    Bloquea un usuario, si es que el id del mismo existe, y lo informa mediante un mensaje de éxito.

    - param id: id del usuario a bloquear.

    - return: recarga la plantilla de usuarios con el estado de bloqueo del usuario actualizado.
    """
    user = auth.User.query.get(id)
    if user is None:
        abort(404)
    if user.rol == 1:
        error.forbidden
    else:
        user.activo = False
    db.session.commit()
    flash('Usuario bloqueado.', 'success')
    return redirect(url_for('users.index'))



@users_bp.route('/desbloquear_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
@check("user_update")
def desbloquear_usuario(id):
    """
    Desloquea un usuario, si es que el id del mismo existe, y lo informa mediante un mensaje de éxito.

    - param id: id del usuario a bloquear.

    - return: recarga la plantilla de usuarios con el estado de bloqueo del usuario actualizado.
    """
    user = auth.User.query.get(id)
    if user is None:
        abort(404)
    user.activo = True
    db.session.commit()
    flash('Usuario desbloqueado.', 'success')
    return redirect(url_for('users.index'))



@users_bp.route('/actualizar_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
@check("user_update")
def actualizar_usuario(id):
    """
    Si el metodo es get, carga la plantilla actualizar_usuario.html, es decir, la página para actualizar la info del usuario, si es que el mismo existe.
    Si el método es post, carga la plantilla actualizar_usuario.html con los datos actualizados.

    - param id: id del usuario a actualizar.
    """
    user = auth.User.query.get(id)
    roles = auth.list_roles()
    roles_dict = {role.id: role for role in roles}
    if user is None:
        abort(404)

    if request.method == 'POST':
        alias = request.form.get('alias')
        email = request.form.get('email')
        activo = request.form.get('activo')
        rol = request.form.get('rol')
        rol = int(rol)

        rol_encontrado = next((r for r in roles if r.id == rol), None)

        if not (alias or email or activo):
            flash('Faltan campos por completar.', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))
        
        query = User.query  
        existing_user = User.query.filter(User.email == email, User.id != id).first()
        if (existing_user):
            flash('El email ingresado ya tiene una cuenta asociada.', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))
        
        if (activo == 'si'):
            activo = True
        else:
            activo = False

        aceptado_google = user.aceptado_google
        user.alias = alias
        user.email = email
        user.activo = activo
        user.rol = rol_encontrado
        user.updated_at = datetime.now()
        user.aceptado_google = True

        try:
            db.session.commit()
            flash('El usuario ha sido actualizado.', 'success')
            if aceptado_google:
                return redirect(url_for('users.index'))
            return redirect(url_for('users.index_google'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
            return redirect(url_for('users.actualizar_usuario', id=id))

    return render_template("users/actualizar_usuario.html", user=user, roles=roles_dict)



@users_bp.route('/eliminar_usuario#<int:id>', methods=['GET', 'POST'])
@login_required
@check("user_destroy")
def eliminar_usuario(id):
    """
    Elimina al usuario pasado por parámetro, si es que existe.

    - param id: id del usuario a eliminar.
    """
    user = auth.User.query.get(id)
    if user is None:
        abort(404)
    aceptado_google= user.aceptado_google
    try:
        db.session.delete(user)
        db.session.commit()
        flash('El usuario ha sido eliminado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {str(e)}', 'danger')
    if aceptado_google:
        return redirect(url_for('users.index'))
    return redirect(url_for('users.index_google'))