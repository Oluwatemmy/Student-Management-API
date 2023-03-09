from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.user import Student
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

student_namespace = Namespace('students', description='Students related operations')

student_model = student_namespace.model(
    'Student', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description='Name of the Student'),
        'email': fields.String(required=True, description='Email of the Student'),
        'password_hash': fields.String(required=True, description='Password of the Student'),   
    }
)

user_model = student_namespace.model(
    'User', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description='Name of the User'),
        'email': fields.String(required=True, description='Email of the User')
    }
)

@student_namespace.route('/student')
class StudentList(Resource):
    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self):
        """
            Get all students
        """
        return Student.query.all()

    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    def post(self):
        """
            Create a new student
        """
        data = request.get_json()

        new_student = Student(
            name = data.get('name'),
            email = data.get('email'),
            password_hash = data.get('password_hash')
        )

        new_student.save()

        return new_student, HTTPStatus.CREATED