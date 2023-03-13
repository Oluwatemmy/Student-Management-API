from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import Student, Lecturer, Admin
from ..models.course import Course, StudentCourse
from ..utils import db
from http import HTTPStatus
from ..utils import generate_random_string
from ..student.serializers_utils import student_model, course_retrieve_model, create_course_model, student_register_for_course_model, course_lecturer_model


courses_namespace = Namespace('courses', description="Namespace for course")

course_model = courses_namespace.model('Course Creation', create_course_model)

course_retrieve_model = courses_namespace.model('Course Retrieve', course_retrieve_model)

student_register_for_course_model = courses_namespace.model('Student Register for Course', student_register_for_course_model)

course_lecturer_model = courses_namespace.model('Course Lecturer', course_lecturer_model)

student_field = courses_namespace.model('Student Model', student_model)


@courses_namespace.route('/course')
class CourseList(Resource):
    @courses_namespace.doc('List all courses')
    @courses_namespace.marshal_with(course_retrieve_model)
    def get(self):
        """List all courses available"""
        courses = Course.query.all()
        return courses, HTTPStatus.OK


    @courses_namespace.doc('Create a new course')
    @courses_namespace.expect(course_model)
    @jwt_required()
    def post(self):
        """Create a new course"""
        # current_user = get_jwt_identity()
        # admin = Admin.query.filter_by(id=current_user).first()
        # if not admin:
        #     return {'message': 'Admin Priviledge Required'}, HTTPStatus.UNAUTHORIZED
        data = request.get_json()
        lecturer = Lecturer.query.filter_by(id=data.get('lecturer_id')).first()
        if lecturer:
            code = generate_random_string(7)
            course = Course(
                course_code=code,
                lecturer_id=lecturer.id,
                name=data.get('name'),
            )
            try:
                course.save()
                return {'message': 'Course registered successfully'}, HTTPStatus.CREATED
            except:
                return {'message': 'An error occurred while saving course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Invalid teacher id'}, HTTPStatus.BAD_REQUEST
    

@courses_namespace.route('/<int:course_id>')
class GetDeleteCourse(Resource):
    @courses_namespace.doc('Get a course')
    @courses_namespace.marshal_with(course_retrieve_model)
    def get(self, course_id):
        """Get a course by ID"""
        course = Course.get_by_id(course_id)
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        else:
            return course, HTTPStatus.OK

    @courses_namespace.doc('Delete a course')
    @jwt_required()
    def delete(self, course_id):
        """Delete a course by ID"""
        # current_user = get_jwt_identity()
        # lecturer = Lecturer.query.filter_by(id=current_user).first()
        # if not lecturer:
        #     return {'message': 'Lecturer Priviledge Required'}, HTTPStatus.UNAUTHORIZED
        
        course = Course.get_by_id(course_id)
        if course:
            try:
                course.delete()
                return {'message': 'Course deleted successfully'}, HTTPStatus.OK
            except:
                db.session.rollback()
                return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
    

@courses_namespace.route('/<int:course_id>/students')
class CourseStudents(Resource):
    @courses_namespace.doc('List all students in a course')
    @courses_namespace.marshal_with(student_field)
    def get(self, course_id):
        """List all students in a course"""
        course = Course.get_by_id(course_id)
        get_course_student = StudentCourse.get_students_in_course_by(course.id)
        return get_course_student, HTTPStatus.OK