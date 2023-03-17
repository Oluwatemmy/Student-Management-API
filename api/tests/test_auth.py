import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.user import User, Admin
from flask_jwt_extended import create_access_token


class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.client = self.app.test_client()

        self.appctx = self.app.app_context()

        self.appctx.push()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_signup(self):
        # Register an admin
        admin_signup_data = {
            "name": "Test User",
            "email": "admin@aotem.com",
            "user_type": "admin",
            "password": "password"
        }
        admin_signup_response = self.client.post('/auth/signup', json=admin_signup_data)

        admin = User.query.filter_by(email=admin_signup_data['email']).first()

        assert admin.name == "Test User"

        assert admin.email == admin_signup_data['email']

        assert admin_signup_response.status_code == 201

        # Register a student
        student_signup_data = {
            "name": "Student",
            "email": "student@aotem.com",
            "user_type": "student",
            "password": "password"
        }

        student_signup_response = self.client.post('/auth/signup', json=student_signup_data)

        student = User.query.filter_by(email=student_signup_data['email']).first()

        assert student.name == "Student"

        assert student.email == student_signup_data['email']

        assert student_signup_response.status_code == 201


        # Sign an Admin in
        admin_login_data = {
            "email": "admin@aotem.com",
            "password": "password"
        }

        admin_login_response = self.client.post('/auth/login', json=admin_login_data)

        assert admin_login_response.status_code == 200

        token = create_access_token(identity=admin.id)

        headers = {
            'Authorization': f'Bearer {token}'
        }


        # Sign a student in
        student_login_data = {
            "email": 'student@aotem.com',
            "password": "password"
        }

        student_login_response = self.client.post('/auth/login', json=student_login_data)

        assert student_login_response.status_code == 200

        token = create_access_token(identity=student.id)

        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        # Request for password reset
        password_reset_request_data = {
            "email": 'admin@aotem.com'
        }

        password_reset_request_response = self.client.post('/auth/password-reset-request', json=password_reset_request_data)

        assert password_reset_request_response.status_code == 200

        
        # Activate a test admin
        admin_activate_data = {
            "name": "Admin",
            "email": "admin@aotem.com",
            "user_type": "admin",
            "password": "password"
        }

        admin_activate_response = self.client.post('/auth/register', json=admin_activate_data)

        admin = Admin.query.filter_by(email=admin_activate_data['email']).first()

        token1 = create_access_token(identity=admin.id)

        headers = {
            'Authorization': f'Bearer {token1}'
        }

        
