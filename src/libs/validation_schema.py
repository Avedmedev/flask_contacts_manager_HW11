from marshmallow import Schema, fields, validate


class RegistrationSchema(Schema):
    nick = fields.Str(validate=validate.Length(min=3, max=10), required=True)
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=4), required=True)


class LoginSchema(Schema):
    remember = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=4), required=True)
