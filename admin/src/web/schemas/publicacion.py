from marshmallow import Schema, fields, validate

class PublicacionSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    autor = fields.Str(required=True)
    fecha_publicacion = fields.DateTime(format="%d/%m/%Y")
    copete = fields.Str(required=True)
    contenido = fields.Str(required=True)
    inserted_at = fields.DateTime(format="%d/%m/%Y", dump_only=True)
    updated_at = fields.DateTime(format="%d/%m/%Y", dump_only=True)
    estado = fields.Str(validate=validate.OneOf(["borrador","publicado","archivado"]),required=True)



publicacion_schema = PublicacionSchema()
publicaciones_schema = PublicacionSchema(many=True)
create_publicacion_schema = PublicacionSchema(only=("titulo", "autor", "fecha_publicacion", "copete", "contenido"))