from flask_restful import fields

mac_fields = {
    'mac_address': fields.String(),
    'user': fields.String(attribute='user.name')
}

user_fields = {
    'name': fields.String,
    'mac_addresses': fields.List(
        fields.Nested(mac_fields)
    ),
}
user_list_fields = {
    fields.List(
        fields.Nested(user_fields)
    ),
}

logs_fields = {
    'time': fields.String,
    'mac_address': fields.String,
    'user': fields.String,
    'ip': fields.String,
    'hostname': fields.String,
}
