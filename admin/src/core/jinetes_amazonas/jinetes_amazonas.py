# src/core/jinete_amazonas/models.py
from datetime import datetime
from src.core.database import db

class JineteAmazona(db.Model):
    __tablename__ = 'jinetes_amazonas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento_localidad = db.Column(db.String(100), nullable=False)
    lugar_nacimiento_provincia = db.Column(db.String(100), nullable=False)
    
    # Domicilio actual
    domicilio_actual = db.Column(db.String(200), nullable=False)
    
    telefono = db.Column(db.String(20), nullable=False)
    contacto_emergencia = db.Column(db.String(200), nullable=False)
    telefono_emergencia = db.Column(db.String(20), nullable=False)
    
    # Beca
    becado = db.Column(db.Boolean, nullable=False, default=False)
    beca_observaciones = db.Column(db.Text, nullable=True)
    
    # Certificado de discapacidad
    certificado_discapacidad = db.Column(db.Boolean, nullable=False, default=False)
    diagnostico_discapacidad = db.Column(db.String(255), nullable=True)
    tipo_discapacidad = db.Column(db.String(50), nullable=True)  # Opciones: Mental, Motora, Sensorial, Visceral
    
    # Asignaciones familiares
    percibe_asignacion_familiar = db.Column(db.Boolean, nullable=False, default=False)
    asignacion_hijo = db.Column(db.Boolean, nullable=False, default=False)
    asignacion_hijo_discapacidad = db.Column(db.Boolean, nullable=False, default=False)
    asignacion_ayuda_escolar = db.Column(db.Boolean, nullable=False, default=False)
    
    # Pensión
    pension = db.Column(db.String(100), nullable=True)  # "Provincial" o "Nacional"
    
    # Situación previsional
    obra_social = db.Column(db.String(100), nullable=True)
    numero_afiliado = db.Column(db.String(50), nullable=True)
    curatela = db.Column(db.Boolean, nullable=False, default=False)
    observaciones_previsionales = db.Column(db.Text, nullable=True)
    
    # Institución escolar
    institucion_escolar = db.Column(db.String(100), nullable=True)
    direccion_institucion = db.Column(db.String(200), nullable=True)
    telefono_institucion = db.Column(db.String(20), nullable=True)
    grado_anio_actual = db.Column(db.String(50), nullable=True)
    observaciones_institucion = db.Column(db.Text, nullable=True)
    
    # Profesionales que lo atienden
    profesionales_atienden = db.Column(db.Text, nullable=True)

    # Datos de familiares o tutores responsables
    parentesco_familiar_1 = db.Column(db.String(50), nullable=True)
    nombre_familiar_1 = db.Column(db.String(100), nullable=True)
    apellido_familiar_1 = db.Column(db.String(100), nullable=True)
    dni_familiar_1 = db.Column(db.String(20), nullable=True)
    domicilio_familiar_1 = db.Column(db.String(200), nullable=True)
    celular_familiar_1 = db.Column(db.String(20), nullable=True)
    email_familiar_1 = db.Column(db.String(100), nullable=True)
    escolaridad_familiar_1 = db.Column(db.String(50), nullable=True)  # Primario, Secundario, Terciario, Universitario
    ocupacion_familiar_1 = db.Column(db.String(100), nullable=True)
    
    parentesco_familiar_2 = db.Column(db.String(50), nullable=True)
    nombre_familiar_2 = db.Column(db.String(100), nullable=True)
    apellido_familiar_2 = db.Column(db.String(100), nullable=True)
    dni_familiar_2 = db.Column(db.String(20), nullable=True)
    domicilio_familiar_2 = db.Column(db.String(200), nullable=True)
    celular_familiar_2 = db.Column(db.String(20), nullable=True)
    email_familiar_2 = db.Column(db.String(100), nullable=True)
    escolaridad_familiar_2 = db.Column(db.String(50), nullable=True)  # Primario, Secundario, Terciario, Universitario
    ocupacion_familiar_2 = db.Column(db.String(100), nullable=True)

    propuesta_trabajo = db.Column(db.String(100), nullable=False)
    condicion = db.Column(db.String(10), nullable=False)
    sede = db.Column(db.String(10), nullable=False)
    dia = db.Column(db.String(100), nullable=False)

    #Relaciones con miembros del equipo
    profesor_terapeuta = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    conductor = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    auxiliar_pista = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)

    #Relacion con caballo
    caballo = db.Column(db.Integer, db.ForeignKey('encuestres.id'), nullable=False)

    # Relacionado con la gestión de archivos/documentos
    documentos = db.relationship('DocumentoJinete', backref='jinete_amazona', lazy=True, cascade="all")

    activo = db.Column(db.Boolean, default=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Función para obtener el jinete/amazona por ID
    @staticmethod
    def obtener_jinete_por_id(jinete_id):
        return db.session.query(JineteAmazona).filter(JineteAmazona.id == jinete_id).first()

