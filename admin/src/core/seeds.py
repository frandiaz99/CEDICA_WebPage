from src.core import board, auth, equipo, encuestre, encuestre_empleado, permiso, rol_permiso, contacto, jinetes_amazonas, cobros
from datetime import datetime
from itertools import chain 

def run():
    '''
    Inserta los datos de prueba en la DB
    '''
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
    kkk = auth.create_user(alias="kkk", email="kkk@gmail.com", password="1234", activo=False)            

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
    editor_rol = auth.create_rol(nombre="editor")

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
    auth.assign_rol(kkk, editor_rol)

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

    #permisos modulo reporte
    reportes_index = permiso.create_permiso(nombre="reportes_index")
    reportes_show = permiso.create_permiso(nombre="reportes_show")

    # permisos modulo administracion
    administracion_index = permiso.create_permiso(nombre="administracion_index")
    administracion_new = permiso.create_permiso(nombre="administracion_new")
    administracion_destroy = permiso.create_permiso(nombre="administracion_destroy")
    administracion_update = permiso.create_permiso(nombre="administracion_update")
    administracion_show = permiso.create_permiso(nombre="administracion_show")

    permisos_administracion = [administracion_index, administracion_new, administracion_destroy, administracion_update, administracion_show]

    #permisos modulo contacto 
    contacto_index = permiso.create_permiso(nombre="contacto_index")
    contacto_new = permiso.create_permiso(nombre="contacto_new")
    contacto_destroy = permiso.create_permiso(nombre="contacto_destroy")
    contacto_update = permiso.create_permiso(nombre="contacto_update")
    contacto_show = permiso.create_permiso(nombre="contacto_show")

    permisos_contacto = [contacto_index, contacto_new, contacto_destroy, contacto_update, contacto_show]

    permiso_accept = permiso.create_permiso(nombre="user_accept")

    # Asignar permisos a rol
    permisos_system_admin = list(chain(permisos_user,  permisos_issue , permisos_equipo , permisos_registro_cobros , permisos_registro_pagos , permisos_ja , permisos_encuestre, permisos_administracion, permisos_contacto, [reportes_show], [reportes_index], [permiso_accept]))
    rol_permiso.assign_permisos_to_rol(system_admin, permisos_system_admin)
    
    permisos_administracion_rol = list(chain(permisos_equipo , permisos_ja , permisos_registro_cobros , permisos_registro_pagos , [encuestre_index] , [encuestre_show], [reportes_show], [reportes_index], permisos_administracion, permisos_contacto, [permiso_accept], [user_update],[user_destroy]))
    rol_permiso.assign_permisos_to_rol(administracion_rol, permisos_administracion_rol)

    permisos_tecnica_rol = list(chain(permisos_ja , [registro_cobros_index] , [registro_cobros_show] , [encuestre_index] , [encuestre_show], [reportes_index], [reportes_show]))
    rol_permiso.assign_permisos_to_rol(tecnica_rol, permisos_tecnica_rol)

    permisos_encuestre_rol = list(chain([ja_index] , [ja_show] , permisos_encuestre))
    rol_permiso.assign_permisos_to_rol(encuestre_rol, permisos_encuestre_rol)

    permisos_editor_rol = list(chain([administracion_index], [administracion_show], [administracion_update], [administracion_new]))
    rol_permiso.assign_permisos_to_rol(editor_rol, permisos_editor_rol)

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
        fecha_cese=datetime(2025, 12, 11),
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
        fecha_cese=datetime(2025, 11, 15),
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
        fecha_cese=datetime(2025, 10, 1),
    )

    caballo1 = encuestre.create_encuestre(
        nombre="Juancito el caballo veloz",
        fecha_nacimiento=datetime(2015, 5, 1),
        sexo="Macho",
        raza="Pura Sangre",
        pelaje="Castaño",
        compra_donacion="Compra",
        fecha_ingreso=datetime.now(),
        sede_asignada = "CASJ",
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
        sede_asignada = "HLP",
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
    sede_asignada="AAAA",
    tipo_ja_asignado="Equitación",
    
    )
    lista_empleados1 = [empleado1, empleado2]
    lista_empleados2 = [empleado2, empleado3]
    lista_empleados3 = [empleado3]

    encuestre_empleado.assign_empleado_to_encuestre(caballo1, lista_empleados1)
    encuestre_empleado.assign_empleado_to_encuestre(caballo2, lista_empleados2)
    encuestre_empleado.assign_empleado_to_encuestre(caballo3, lista_empleados3)


    contacto1 = contacto.create_contacto(
        nombre_completo="Juan Perez",
        correo_electronico="juanp@gmail.com",
        mensaje="Holaa ajaja",
    )

#- ------------------
    jinete1 = jinetes_amazonas.create_jinete_amazona(
    nombre="Lucía",
    apellido="Gómez",
    dni="32456789",
    edad=25,
    fecha_nacimiento=datetime(1998, 4, 5),
    lugar_nacimiento_localidad="Buenos Aires",
    lugar_nacimiento_provincia="Buenos Aires",
    domicilio_actual="Pasaje Los Pinos 101",
    telefono="1122334455",
    contacto_emergencia="Juan Gómez",
    telefono_emergencia="1122334455",
    becado=True,
    beca_observaciones="Beca parcial",
    certificado_discapacidad=True,
    diagnostico_discapacidad="Trastorno de movilidad",
    tipo_discapacidad="Motora",
    percibe_asignacion_familiar=True,
    asignacion_hijo=False,
    asignacion_hijo_discapacidad=True,
    asignacion_ayuda_escolar=False,
    pension="Nacional",
    obra_social="OSDE",
    numero_afiliado="112233",
    curatela=False,
    observaciones_previsionales="Observaciones de previsión",
    institucion_escolar="Escuela Especial ABC",
    direccion_institucion="Calle Falsa 123",
    telefono_institucion="1123456789",
    grado_anio_actual="5to año",
    observaciones_institucion="Recibe apoyo en clase",
    profesionales_atienden="Kinesiólogo, Psicólogo",
    parentesco_familiar_1="Madre",
    nombre_familiar_1="Ana",
    apellido_familiar_1="Gómez",
    dni_familiar_1="12345678",
    domicilio_familiar_1="Pasaje Los Pinos 101",
    celular_familiar_1="1122334455",
    email_familiar_1="ana.gomez@gmail.com",
    escolaridad_familiar_1="Universitario",
    ocupacion_familiar_1="Médica",
    propuesta_trabajo="Hipoterapia",
    condicion="Rentado",
    sede="CASJ",
    dia="Lunes y miércoles",
    profesor_terapeuta=empleado1.id,
    conductor=empleado2.id,
    auxiliar_pista=empleado3.id,
    caballo=caballo1.id,
    )

    jinete2 = jinetes_amazonas.create_jinete_amazona(
        nombre="Martín",
        apellido="López",
        dni="33456789",
        edad=22,
        fecha_nacimiento=datetime(2001, 7, 22),
        lugar_nacimiento_localidad="Córdoba",
        lugar_nacimiento_provincia="Córdoba",
        domicilio_actual="Av. de Mayo 200",
        telefono="1234567890",
        contacto_emergencia="Carlos López",
        telefono_emergencia="1234567890",
        becado=False,
        beca_observaciones=None,
        certificado_discapacidad=False,
        diagnostico_discapacidad=None,
        tipo_discapacidad=None,
        percibe_asignacion_familiar=False,
        asignacion_hijo=False,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=False,
        pension=None,
        obra_social="Swiss Medical",
        numero_afiliado="223344",
        curatela=True,
        observaciones_previsionales="Apoyo del estado",
        institucion_escolar="Escuela Nacional Nro. 3",
        direccion_institucion="Av. Siempreviva 742",
        telefono_institucion="987654321",
        grado_anio_actual="3er año",
        observaciones_institucion="Regularidad académica",
        profesionales_atienden="Fonoaudiólogo",
        parentesco_familiar_1="Padre",
        nombre_familiar_1="Carlos",
        apellido_familiar_1="López",
        dni_familiar_1="87654321",
        domicilio_familiar_1="Av. de Mayo 200",
        celular_familiar_1="1234567890",
        email_familiar_1="carlos.lopez@gmail.com",
        escolaridad_familiar_1="Secundario",
        ocupacion_familiar_1="Electricista",
        propuesta_trabajo="Monta Terapéutica",
        condicion="Voluntario",
        sede="HLP",
        dia="Martes y jueves",
        profesor_terapeuta=empleado2.id,
        conductor=empleado3.id,
        auxiliar_pista=empleado1.id,
        caballo=caballo2.id,
    )

    jinete10 = jinetes_amazonas.create_jinete_amazona(
        nombre="Florencia",
        apellido="Navarro",
        dni="41456789",
        edad=20,
        fecha_nacimiento=datetime(2003, 12, 12),
        lugar_nacimiento_localidad="Santa Fe",
        lugar_nacimiento_provincia="Santa Fe",
        domicilio_actual="Calle Mitre 789",
        telefono="1133557799",
        contacto_emergencia="María Navarro",
        telefono_emergencia="1133557798",
        becado=True,
        beca_observaciones="Beca completa",
        certificado_discapacidad=True,
        diagnostico_discapacidad="Trastorno sensorial",
        tipo_discapacidad="Sensorial",
        percibe_asignacion_familiar=True,
        asignacion_hijo=True,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=True,
        pension="Provincial",
        obra_social="Galeno",
        numero_afiliado="556677",
        curatela=False,
        observaciones_previsionales="Pensión provincial",
        institucion_escolar="Escuela Inclusiva Nro. 5",
        direccion_institucion="Calle Principal 999",
        telefono_institucion="1122345678",
        grado_anio_actual="2do año",
        observaciones_institucion="Recibe apoyo pedagógico",
        profesionales_atienden="Psicólogo, Terapeuta ocupacional",
        parentesco_familiar_1="Hermano",
        nombre_familiar_1="Juan",
        apellido_familiar_1="Navarro",
        dni_familiar_1="45678901",
        domicilio_familiar_1="Calle Mitre 789",
        celular_familiar_1="1133557797",
        email_familiar_1="juan.navarro@gmail.com",
        escolaridad_familiar_1="Secundario",
        ocupacion_familiar_1="Estudiante",
        propuesta_trabajo="Equitación",
        condicion="Rentado",
        sede="AAAA",
        dia="Viernes",
        profesor_terapeuta=empleado1.id,
        conductor=empleado2.id,
        auxiliar_pista=empleado3.id,
        caballo=caballo3.id,
    )

    jinete3 = jinetes_amazonas.create_jinete_amazona(
        nombre="Sofía",
        apellido="Pérez",
        dni="34456789",
        edad=30,
        fecha_nacimiento=datetime(1993, 10, 12),
        lugar_nacimiento_localidad="Rosario",
        lugar_nacimiento_provincia="Santa Fe",
        domicilio_actual="Calle Central 456",
        telefono="123321123",
        contacto_emergencia="Laura Pérez",
        telefono_emergencia="987123456",
        becado=True,
        beca_observaciones="Beca completa",
        certificado_discapacidad=True,
        diagnostico_discapacidad="Pérdida auditiva parcial",
        tipo_discapacidad="Sensorial",
        percibe_asignacion_familiar=True,
        asignacion_hijo=True,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=True,
        pension="Provincial",
        obra_social="IOMA",
        numero_afiliado="334455",
        curatela=False,
        observaciones_previsionales="Sin observaciones",
        institucion_escolar="Instituto de Rehabilitación Rosario",
        direccion_institucion="Calle Principal 456",
        telefono_institucion="123123123",
        grado_anio_actual="4to año",
        observaciones_institucion="Regular apoyo académico",
        profesionales_atienden="Psicólogo, Kinesiólogo",
        parentesco_familiar_1="Padre",
        nombre_familiar_1="Jorge",
        apellido_familiar_1="Pérez",
        dni_familiar_1="23456789",
        domicilio_familiar_1="Calle Central 456",
        celular_familiar_1="123321123",
        email_familiar_1="jorge.perez@gmail.com",
        escolaridad_familiar_1="Secundario",
        ocupacion_familiar_1="Agrónomo",
        propuesta_trabajo="Equinoterapia",
        condicion="Rentado",
        sede="CASJ",
        dia="Viernes",
        profesor_terapeuta=empleado1.id,
        conductor=empleado2.id,
        auxiliar_pista=empleado3.id,
        caballo=caballo1.id,
    )

    # Continúa de manera similar para los siguientes jinetes, variando los datos opcionales

    jinete4 = jinetes_amazonas.create_jinete_amazona(
        nombre="Ana",
        apellido="Martínez",
        dni="35456789",
        edad=27,
        fecha_nacimiento=datetime(1996, 5, 18),
        lugar_nacimiento_localidad="Mendoza",
        lugar_nacimiento_provincia="Mendoza",
        domicilio_actual="Calle 1234",
        telefono="1165781234",
        contacto_emergencia="Miguel Martínez",
        telefono_emergencia="1145678900",
        becado=False,
        beca_observaciones=None,
        certificado_discapacidad=False,
        diagnostico_discapacidad=None,
        tipo_discapacidad=None,
        percibe_asignacion_familiar=False,
        asignacion_hijo=False,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=False,
        pension=None,
        obra_social="OSDE",
        numero_afiliado="121234",
        curatela=True,
        observaciones_previsionales="Requiere apoyo",
        institucion_escolar="Escuela Inclusiva M",
        direccion_institucion="Av. Independencia 500",
        telefono_institucion="1122334455",
        grado_anio_actual="6to año",
        observaciones_institucion="Soporte en matemáticas",
        profesionales_atienden="Fonoaudiólogo",
        parentesco_familiar_1="Hermano",
        nombre_familiar_1="Juan",
        apellido_familiar_1="Martínez",
        dni_familiar_1="45678901",
        domicilio_familiar_1="Calle 1234",
        celular_familiar_1="1165781234",
        email_familiar_1="juan.martinez@gmail.com",
        escolaridad_familiar_1="Primario",
        ocupacion_familiar_1="Desocupado",
        propuesta_trabajo="Hipoterapia",
        condicion="Voluntario",
        sede="AAAA",
        dia="Sábado",
        profesor_terapeuta=empleado2.id,
        conductor=empleado3.id,
        auxiliar_pista=empleado1.id,
        caballo=caballo3.id,
    )

    jinete11 = jinetes_amazonas.create_jinete_amazona(
        nombre="Juan",
        apellido="Pérez",
        dni="44556677",
        edad=28,
        fecha_nacimiento=datetime(1996, 4, 15),
        lugar_nacimiento_localidad="Rosario",
        lugar_nacimiento_provincia="Santa Fe",
        domicilio_actual="Av. Belgrano 345",
        telefono="0987654321",
        contacto_emergencia="Laura Pérez",
        telefono_emergencia="0987654321",
        becado=True,
        beca_observaciones="Becado por discapacidad",
        certificado_discapacidad=True,
        diagnostico_discapacidad="Visceral",
        tipo_discapacidad="Visceral",
        percibe_asignacion_familiar=True,
        asignacion_hijo=False,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=True,
        pension=None,
        obra_social="OSDE",
        numero_afiliado="112233",
        curatela=False,
        observaciones_previsionales="Discapacidad visceral",
        institucion_escolar="Escuela Especial Nro. 4",
        direccion_institucion="Av. San Martín 321",
        telefono_institucion="1122334455",
        grado_anio_actual="4to año",
        observaciones_institucion="Buen rendimiento académico",
        profesionales_atienden="Médico general, Terapeuta ocupacional",
        parentesco_familiar_1="Madre",
        nombre_familiar_1="Ana",
        apellido_familiar_1="Pérez",
        dni_familiar_1="33445566",
        domicilio_familiar_1="Av. Belgrano 345",
        celular_familiar_1="0987654321",
        email_familiar_1="ana.perez@gmail.com",
        escolaridad_familiar_1="Secundario completo",
        ocupacion_familiar_1="Docente",
        propuesta_trabajo="Monta Terapéutica",
        condicion="Voluntario",
        sede="HLP",
        dia="Lunes y Miércoles",
        profesor_terapeuta=empleado2.id,
        conductor=empleado3.id,
        auxiliar_pista=empleado1.id,
        caballo=caballo2.id,
    )

    # Crear Jinete 12 (Discapacidad Mental)
    jinete12 = jinetes_amazonas.create_jinete_amazona(
        nombre="Sara",
        apellido="Gómez",
        dni="55667788",
        edad=25,
        fecha_nacimiento=datetime(1999, 1, 10),
        lugar_nacimiento_localidad="Mar del Plata",
        lugar_nacimiento_provincia="Buenos Aires",
        domicilio_actual="Calle Ficticia 200",
        telefono="1239876543",
        contacto_emergencia="Pedro Gómez",
        telefono_emergencia="1239876543",
        becado=False,
        beca_observaciones="No becada por falta de fondos",
        certificado_discapacidad=True,
        diagnostico_discapacidad="Mental",
        tipo_discapacidad="Mental",
        percibe_asignacion_familiar=False,
        asignacion_hijo=False,
        asignacion_hijo_discapacidad=False,
        asignacion_ayuda_escolar=False,
        pension=None,
        obra_social="Federada",
        numero_afiliado="667788",
        curatela=True,
        observaciones_previsionales="Discapacidad mental",
        institucion_escolar="Escuela Especial Nro. 6",
        direccion_institucion="Calle Principal 456",
        telefono_institucion="2233445566",
        grado_anio_actual="2do año",
        observaciones_institucion="Excelente comportamiento",
        profesionales_atienden="Psicólogo, Psiquiatra",
        parentesco_familiar_1="Padre",
        nombre_familiar_1="Raúl",
        apellido_familiar_1="Gómez",
        dni_familiar_1="99887766",
        domicilio_familiar_1="Calle Ficticia 200",
        celular_familiar_1="1239876543",
        email_familiar_1="raul.gomez@gmail.com",
        escolaridad_familiar_1="Secundario completo",
        ocupacion_familiar_1="Empleado",
        propuesta_trabajo="Monta Terapéutica",
        condicion="Voluntario",
        sede="HLP",
        dia="Miércoles y Viernes",
        profesor_terapeuta=empleado2.id,
        conductor=empleado3.id,
        auxiliar_pista=empleado1.id,
        caballo=caballo2.id,
    )

 
    cobro1 = cobros.create_cobro(
        id_ja=jinete1.id,
        fecha_pago=datetime(2023, 1, 15),
        tipo_pago="efectivo",
        monto=200.0,
        beneficiario_id=empleado1.id,
        en_deuda=True,
        observaciones="Pago parcial de hipoterapia."
    )

    cobro2 = cobros.create_cobro(
        id_ja=jinete2.id,
        fecha_pago=datetime(2023, 2, 20),
        tipo_pago="transferencia",
        monto=150.0,
        beneficiario_id=empleado2.id,
        en_deuda=False,
        observaciones="Pago completo de monta terapéutica."
    )

    cobro3 = cobros.create_cobro(
        id_ja=jinete3.id,
        fecha_pago=datetime(2023, 3, 5),
        tipo_pago="credito",
        monto=300.0,
        beneficiario_id=empleado3.id,
        en_deuda=True,
        observaciones="Deuda pendiente de equinoterapia."
    )

    cobro4 = cobros.create_cobro(
        id_ja=jinete4.id,
        fecha_pago=datetime(2023, 4, 10),
        tipo_pago="cheque",
        monto=250.0,
        beneficiario_id=empleado1.id,
        en_deuda=False,
        observaciones="Pago realizado para hipoterapia."
    )

    cobro5 = cobros.create_cobro(
        id_ja=jinete1.id,
        fecha_pago=datetime(2023, 5, 15),
        tipo_pago="efectivo",
        monto=180.0,
        beneficiario_id=empleado2.id,
        en_deuda=False,
        observaciones="Pago completo de servicios."
    )

    cobro6 = cobros.create_cobro(
        id_ja=jinete2.id,
        fecha_pago=datetime(2023, 6, 20),
        tipo_pago="transferencia",
        monto=220.0,
        beneficiario_id=empleado3.id,
        en_deuda=True,
        observaciones="Deuda de servicio de equinoterapia."
    )

    cobro7 = cobros.create_cobro(
        id_ja=jinete3.id,
        fecha_pago=datetime(2023, 7, 25),
        tipo_pago="credito",
        monto=350.0,
        beneficiario_id=empleado1.id,
        en_deuda=False,
        observaciones="Pago completo de equinoterapia."
    )

    cobro8 = cobros.create_cobro(
        id_ja=jinete4.id,
        fecha_pago=datetime(2023, 8, 30),
        tipo_pago="debito",
        monto=290.0,
        beneficiario_id=empleado2.id,
        en_deuda=True,
        observaciones="Deuda pendiente de monta terapéutica."
    )