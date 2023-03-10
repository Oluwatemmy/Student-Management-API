from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.user import User, Student, Admin, Lecturer
from ..utils import db, generate_random_string, send_email, generate_reset_token
from ..utils.blocklist import BLOCKLIST
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from .serializers_utils import login_field, password_reset_field, pasword_reset_request_field, signup_field

auth_namespace = Namespace('auth', description="Namespace for Authentication")

signup_model = auth_namespace.model('Signup', signup_field)
login_model = auth_namespace.model('Login', login_field)
password_reset_request_model = auth_namespace.model('PasswordResetRequest', pasword_reset_request_field)
password_reset_model = auth_namespace.model('PasswordReset', password_reset_field)

@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    def post(self):
        """
            Register a user 
        """
        data = request.get_json()

        # check if user already exists
        user = Student.query.filter_by(email=data.get('email')).first()
        if user:
            return {
                'message': "User already exists"
            }, HTTPStatus.CONFLICT

        username = generate_random_string(10)
        current_year =  str(datetime.now().year)

        if data.get('user_type') == 'student':
            admission = 'STD@' + generate_random_string(5) + current_year
            new_user = Student(
                email = data.get('email'),
                name = data.get('name'),
                username=username,
                password_hash = generate_password_hash(data.get('password')),
                matric_no = admission,
                user_type = 'student'
            )
        elif data.get('user_type') == 'lecturer':
            staff = 'LCT@' + generate_random_string(5) + current_year
            new_user = Lecturer(
                email = data.get('email'),
                name = data.get('name'),
                username=username,
                password_hash = generate_password_hash(data.get('password')),
                staff_no = staff,
                user_type = 'lecturer'
            )
        elif data.get('user_type') == 'admin':
            nomination = 'Admin'
            new_user = Admin(
                email = data.get('email'),
                name = data.get('name'),
                username=username,
                password_hash = generate_password_hash(data.get('password')),
                nomination=nomination,
                user_type = 'admin',
                is_admin=True
            )
        else:
            return {
                'message': 'Invalid user type'
            }, HTTPStatus.BAD_REQUEST
        
        try:
            new_user.save()
            return {
                'message': 'User {} created successfully as {}'.format(new_user.name, new_user.user_type)
            }, HTTPStatus.CREATED
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {
                'message': 'Invalid email or password'
            }, HTTPStatus.UNAUTHORIZED
        
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        response = {
            'message': 'Login Successful',
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response, HTTPStatus.OK



@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {
            "access_token": access_token
        }, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
            Log the User Out by revoking Access/refresh token
        """
        token = get_jwt()
        jti = token['jti']
        token_type = token['type']
        # user_identity = get_jwt_identity()
        BLOCKLIST.add(jti)

        return {
            'message': 'Successfully logged out and token revoked successfully.'
        }, HTTPStatus.OK
    

@auth_namespace.route('/password-reset-request')
class PasswordResetRequest(Resource):
    @auth_namespace.expect(password_reset_request_model)
    def post(self):
        """
            Request for password reset
        """
        data = request.get_json()

        email = data.get('email')

        user = User.query.filter_by(email=email).first()

        if not user:
            return {
                'message': 'User does not exist'
            }, HTTPStatus.NOT_FOUND
        if user:
            token = generate_reset_token(25)
            user.password_reset_token = token
            db.session.commit()

            # Send a password reset email
            send_email(user, token)

            return {
                'message': 'Password reset token generated successfully. Please check your mail!'
            }, HTTPStatus.OK
    

@auth_namespace.route('/password-reset/<token>')
class PasswordReset(Resource):
    @auth_namespace.expect(password_reset_model)
    def post(self, token):
        """
            Reset password
        """
        data = request.get_json()

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        user = User.query.filter_by(password_reset_token=token).first()

        if not user:
            return {
                'message': 'Invalid or expired token'
            }, HTTPStatus.BAD_REQUEST

        if password == confirm_password:
            hashed_password = generate_password_hash(confirm_password)
            user.password_hash = hashed_password
            user.password_reset_token = None
            db.session.commit()

            return {
                'message': 'Password reset successful'
            }, HTTPStatus.OK
        else:
            return {
                'message': 'Passwords do not match'
            }, HTTPStatus.BAD_REQUEST
