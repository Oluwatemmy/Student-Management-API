from flask_restx import fields

signup_field = {
    'name': fields.String(required=True, description='Name of the User'),
    'email': fields.String(required=True, description='User email address'),
    'user_type': fields.String(required=True, description='User type'),
    'password': fields.String(required=True, description='Password of the User')
}

login_field = {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='Password of the User')
}

pasword_reset_request_field = {
    'email': fields.String(required=True, description='User email address')
}

password_reset_field = {
    'password': fields.String(required=True, description='User Password'),
    'confirm_password': fields.String(required=True, description='User Confirm Password')
}
