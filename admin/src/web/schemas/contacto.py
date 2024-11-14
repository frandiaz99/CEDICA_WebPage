from marshmallow import Schema, fields, validate

class ContactoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_completo = fields.Str(required=True)
    correo_electronico = fields.Email(required=True)
    mensaje = fields.Str(required=True)
    estado = fields.Str(validate=validate.OneOf(["pendiente","en_proceso","leido"]),required=True)
    comentario = fields.Str(allow_none=True)
    inserted_at = fields.DateTime(format="%d/%m/%Y", dump_only=True)
    updated_at = fields.DateTime(format="%d/%m/%Y", dump_only=True)




contacto_schema = ContactoSchema()
contactos_schema = ContactoSchema(many=True)
create_contacto_schema = ContactoSchema(only=("nombre_completo", "correo_electronico", "mensaje"))