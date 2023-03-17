import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.user import User, Admin, Lecturer, Student
from ..models.course import Course, StudentCourse
from flask_jwt_extended import create_access_token

class TestCourses(unittest.TestCase):

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

    def test_course_list(self):
        # Activate an admin
        admin_activation_data = {
            "name": 'Test User',
            "email": "admin@aotem.com",
            "password": "password"
        }

        admin_activation_response = self.client.post('/auth/register', json=admin_activation_data)

        token = create_access_token(identity='Test User')

        headers = {
            'Authorization': f'Bearer {token}'
        }
