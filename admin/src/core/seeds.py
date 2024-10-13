from src.core import board, auth, equipo, encuestre, encuestre_empleado, permiso, rol_permiso # Importa el módulo equipo
from datetime import datetime
from itertools import chain 

def run():
    # Crear issues
    issue1 = board.create_issue(
        email="mail1@gmail.com",
        title="Mi computadora no funciona",
        description="Me compraron una nueva pc y no anda"
    )

    issue2 = board.create_issue(
        email="mail2@gmail.com",
        title="No puedo obtener mis mails",
        description="Estoy tratando de acceder a los mails",
        status="in_progress"
    )

    issue3 = board.create_issue(
        email="mail3@gmail.com",
        title="No puedo imprimir",
        description="No anda la impresora",
        status="done"
    )

    
    # Crear usuarios de prueba
    fede = auth.create_user(alias="Fede", email="fede@gmail.com", password="1234", activo=True)    
    mati = auth.create_user(alias="el mati", email="mati@gmail.com", password="1234", activo=True)    
    miguel = auth.create_user(alias="migueee", email="miguel@gmail.com", password="1234", activo=False)     
    aaaa = auth.create_user(alias="aaaa", email="aaaa@gmail.com", password="1234", activo=True)    
    bbbb = auth.create_user(alias="bbb", email="bbbb@gmail.com", password="1234", activo=False)    
    ccc = auth.create_user(alias="ccc", email="ccc@gmail.com", password="1234", activo=False)  
    ddd = auth.create_user(alias="dd", email="ddd@gmail.com", password="1234", activo=True)    
    eee = auth.create_user(alias="eee", email="eee@gmail.com", password="1234", activo=False)    
    ffff = auth.create_user(alias="fff", email="ffff@gmail.com", password="1234", activo=False)
    gg = auth.create_user(alias="ggg", email="ggg@gmail.com", password="1234", activo=True)    
    hhh = auth.create_user(alias="hhh", email="hhh@gmail.com", password="1234", activo=False)  
    iii = auth.create_user(alias="iii", email="iii@gmail.com", password="1234", activo=False)    
    jjj = auth.create_user(alias="jjjj", email="jjj@gmail.com", password="1234", activo=True)    
    kkkk = auth.create_user(alias="kkk", email="kkk@gmail.com", password="1234", activo=False)            

    # Asignar issues a usuarios
    board.assign_user(issue1, fede)
    board.assign_user(issue2, mati)
    board.assign_user(issue3, miguel)

    # Crear labels
    label1 = board.create_label(title="Urgente", description="Issues que tienen que resolverse dentro de 24hs")
    label2 = board.create_label(title="Importante", description="Issues de alta prioridad")
    label3 = board.create_label(title="Soporte", description="Issues relacionados con soporte técnico")
    label4 = board.create_label(title="Ventas", description="Issues relacionados con el área de ventas")

    # Asignar labels a issues
    board.assign_labels(issue1, [label1, label2])
    board.assign_labels(issue2, [label3, label4])
    board.assign_labels(issue3, [label1, label3])

    #Crear Roles
    tecnica_rol = auth.create_rol(nombre="tecnica")
    encuestre_rol = auth.create_rol(nombre="encuestre")
    voluntariado_rol = auth.create_rol(nombre="voluntariado")
    administracion_rol = auth.create_rol(nombre="administracion")
    system_admin = auth.create_rol(nombre="system_admin")

    #Asigna roles
    auth.assign_rol(fede, system_admin)
    auth.assign_rol(mati, encuestre_rol)
    auth.assign_rol(miguel, administracion_rol)
    auth.assign_rol(aaaa, tecnica_rol)
    auth.assign_rol(bbbb, voluntariado_rol)
    auth.assign_rol(ccc, encuestre_rol)
    auth.assign_rol(ddd, administracion_rol)
    auth.assign_rol(eee, tecnica_rol)
    auth.assign_rol(ffff, voluntariado_rol)
    auth.assign_rol(gg, encuestre_rol)
    auth.assign_rol(hhh, administracion_rol)
    auth.assign_rol(iii, tecnica_rol)
    auth.assign_rol(jjj, voluntariado_rol)

    #Creo permisos
    user_index = permiso.create_permiso(nombre="user_index")
    user_new= permiso.create_permiso(nombre="user_new")
    user_destroy = permiso.create_permiso(nombre="user_destroy")
    user_update = permiso.create_permiso(nombre="user_update")
    user_show = permiso.create_permiso(nombre="user_show")

    permisos_user = [user_index, user_new, user_destroy, user_update, user_show]

    issue_index = permiso.create_permiso(nombre="issue_index")
    issue_new= permiso.create_permiso(nombre="issue_new")
    issue_destroy = permiso.create_permiso(nombre="issue_destroy")
    issue_update = permiso.create_permiso(nombre="issue_update")
    issue_show = permiso.create_permiso(nombre="issue_show")

    permisos_issue = [issue_index, issue_new, issue_destroy, issue_update, issue_show]

    # Permisos para el módulo equipo
    equipo_index = permiso.create_permiso(nombre="equipo_index")
    equipo_new = permiso.create_permiso(nombre="equipo_new")
    equipo_destroy = permiso.create_permiso(nombre="equipo_destroy")
    equipo_update = permiso.create_permiso(nombre="equipo_update")
    equipo_show = permiso.create_permiso(nombre="equipo_show")

    permisos_equipo = [equipo_index, equipo_new, equipo_destroy, equipo_update, equipo_show]

    # Permisos para el módulo registro_pagos
    registro_pagos_index = permiso.create_permiso(nombre="registro_pagos_index")
    registro_pagos_new = permiso.create_permiso(nombre="registro_pagos_new")
    registro_pagos_destroy = permiso.create_permiso(nombre="registro_pagos_destroy")
    registro_pagos_update = permiso.create_permiso(nombre="registro_pagos_update")
    registro_pagos_show = permiso.create_permiso(nombre="registro_pagos_show")

    permisos_registro_pagos = [registro_pagos_index, registro_pagos_new, registro_pagos_destroy, registro_pagos_update, registro_pagos_show]

    # Permisos para el módulo registro_cobros
    registro_cobros_index = permiso.create_permiso(nombre="registro_cobros_index")
    registro_cobros_new = permiso.create_permiso(nombre="registro_cobros_new")
    registro_cobros_destroy = permiso.create_permiso(nombre="registro_cobros_destroy")
    registro_cobros_update = permiso.create_permiso(nombre="registro_cobros_update")
    registro_cobros_show = permiso.create_permiso(nombre="registro_cobros_show")

    permisos_registro_cobros = [registro_cobros_index, registro_cobros_new, registro_cobros_destroy, registro_cobros_update, registro_cobros_show]

    # Permisos para el módulo J&A
    ja_index = permiso.create_permiso(nombre="ja_index")
    ja_new = permiso.create_permiso(nombre="ja_new")
    ja_destroy = permiso.create_permiso(nombre="ja_destroy")
    ja_update = permiso.create_permiso(nombre="ja_update")
    ja_show = permiso.create_permiso(nombre="ja_show")

    permisos_ja = [ja_index, ja_new, ja_destroy, ja_update, ja_show]

    # Permisos para el módulo encuestre
    encuestre_index = permiso.create_permiso(nombre="encuestre_index")
    encuestre_new = permiso.create_permiso(nombre="encuestre_new")
    encuestre_destroy = permiso.create_permiso(nombre="encuestre_destroy")
    encuestre_update = permiso.create_permiso(nombre="encuestre_update")
    encuestre_show = permiso.create_permiso(nombre="encuestre_show")

    permisos_encuestre = [encuestre_index, encuestre_new, encuestre_destroy, encuestre_update, encuestre_show]

    # Asignar permisos a rol
    permisos_system_admin = list(chain(permisos_user,  permisos_issue , permisos_equipo , permisos_registro_cobros , permisos_registro_pagos , permisos_ja , permisos_encuestre))
    rol_permiso.assign_permisos_to_rol(system_admin, permisos_system_admin)
    
    permisos_administracion_rol = list(chain(permisos_equipo , permisos_ja , permisos_registro_cobros , permisos_registro_pagos , [encuestre_index] , [encuestre_show]))
    rol_permiso.assign_permisos_to_rol(administracion_rol, permisos_administracion_rol)

    permisos_tecnica_rol = list(chain(permisos_ja , [registro_cobros_index] , [registro_cobros_show] , [encuestre_index] , [encuestre_show]))
    rol_permiso.assign_permisos_to_rol(tecnica_rol, permisos_tecnica_rol)

    permisos_encuestre_rol = list(chain([ja_index] , [ja_show] , permisos_encuestre))
    rol_permiso.assign_permisos_to_rol(encuestre_rol, permisos_encuestre_rol)
    
    # Crear empleados y asociarlos con usuarios
    empleado1 = equipo.create_empleado(
        nombre="Federico", 
        apellido="García", 
        dni="12345678", 
        domicilio="Calle Falsa 123", 
        email="fede@gmail.com", 
        localidad="Buenos Aires", 
        telefono="123456789", 
        profesion="Psicólogo", 
        puesto_laboral="Terapeuta", 
        contacto_emergencia="Juan Perez 123456789", 
        obra_social="OSDE", 
        numero_afiliado="112233", 
        condicion="Personal Rentado", 
        user_id=fede.id
    )

    empleado2 = equipo.create_empleado(
        nombre="Matías", 
        apellido="Fernández", 
        dni="87654321", 
        domicilio="Av. Siempreviva 742", 
        email="mati@gmail.com", 
        localidad="Córdoba", 
        telefono="987654321", 
        profesion="Kinesiólogo", 
        puesto_laboral="Auxiliar de pista", 
        contacto_emergencia="Maria Gomez 987654321", 
        obra_social="Swiss Medical", 
        numero_afiliado="445566", 
        condicion="Voluntario", 
        user_id=mati.id
    )

    empleado3 = equipo.create_empleado(
        nombre="Miguel", 
        apellido="Sánchez", 
        dni="45678901", 
        domicilio="Av. Libertador 4000", 
        email="miguel@gmail.com", 
        localidad="Rosario", 
        telefono="567890123", 
        profesion="Veterinario", 
        puesto_laboral="Conductor", 
        contacto_emergencia="Carlos López 567890123", 
        obra_social="Galeno", 
        numero_afiliado="778899", 
        condicion="Personal Rentado", 
        user_id=miguel.id
    )

    caballo1 = encuestre.create_encuestre(
        nombre="Juancito el caballo veloz",
        fecha_nacimiento=datetime(2015, 5, 1),
        sexo="Macho",
        raza="Pura Sangre",
        pelaje="Castaño",
        compra_donacion="Compra",
        fecha_ingreso=datetime.now(),
        sede_asignada = "la plata",
        tipo_ja_asignado="Hipoterapia",
        
    )
    
    caballo2 = encuestre.create_encuestre(
        nombre="Rocinante el caballo fiel",
        fecha_nacimiento=datetime(2012, 3, 15),
        sexo="Macho",
        raza="Criollo",
        pelaje="Blanco",
        compra_donacion="Donación",
        fecha_ingreso=datetime.now(),
        sede_asignada = "la plata",
        tipo_ja_asignado="Monta Terapeutica",
        
    )

    caballo3 = encuestre.create_encuestre(
    nombre="Bucéfalo el invencible",
    fecha_nacimiento=datetime(2017, 5, 22),
    sexo="Macho",
    raza="Pura Raza Española",
    pelaje="Negro",
    compra_donacion="Compra",
    fecha_ingreso=datetime.now(),
    sede_asignada="Buenos Aires",
    tipo_ja_asignado="Equitación",
    
)
    lista_empleados1 = [empleado1, empleado2]
    lista_empleados2 = [empleado2, empleado3]
    lista_empleados3 = [empleado3]

    encuestre_empleado.assign_empleado_to_encuestre(caballo1, lista_empleados1)
    encuestre_empleado.assign_empleado_to_encuestre(caballo2, lista_empleados2)
    encuestre_empleado.assign_empleado_to_encuestre(caballo3, lista_empleados3)