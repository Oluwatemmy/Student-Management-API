import unittest
from app import app
import json

class TestAuth(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        



    def test_admin_registration(self):
        data = {'first_name':'Admin','last_name': 'AdminOne','email':'admin13@gmail.com','password':'password123', 'user_type':'admin'} 
        response = self.client.post('/auth/register',data=json.dumps(data) , content_type='application/json')
        print(json.loads(response.text))
        print(response.status_code)
        self.assertEqual(response.status_code, 409)