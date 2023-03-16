from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required
from ..models.user import Lecturer, Student
from ..models.course import Course, StudentCourse
from ..utils import db
from http import HTTPStatus
from ..utils import generate_random_string
from ..student.serializers_utils import student_model, course_retrieve_model, create_course_model, student_register_for_course_model, course_lecturer_model, course_model
from ..decorators import admin_required, lecturer_required, student_required, admin_or_lecturer_required


courses_namespace = Namespace('courses', description="Namespace for course")

create_course_field = courses_namespace.model('Course Creation', create_course_model)

course_retrieve_model = courses_namespace.model('Course Retrieve', course_retrieve_model)

student_register_for_course_model = courses_namespace.model('Student Register for Course', student_register_for_course_model)

course_lecturer_model = courses_namespace.model('Course Lecturer', course_lecturer_model)

student_field = courses_namespace.model('Student Model', student_model)

student_course_field = courses_namespace.model("Course List Model", course_model)


@courses_namespace.route('/')
class CourseList(Resource):
    @courses_namespace.marshal_with(course_retrieve_model)
    @courses_namespace.doc(
        description="""
            Every user can access this endpoint
            This returns all the courses available
        """
    )
    @jwt_required()
    def get(self):
        """List all courses available"""

        courses = Course.query.all()
        return courses, HTTPStatus.OK


    @courses_namespace.expect(create_course_field)
    @courses_namespace.doc(
        description="""
            Only admin can access this endpoint
            This creates a new course
        """
    )
    @admin_required()
    def post(self):
        """Create a new course"""
        
        data = request.get_json()
        lecturer = Lecturer.query.filter_by(id=data.get('lecturer_id')).first()
        if lecturer:
            course_name = Course.query.filter_by(name=data.get('name')).first()
            if course_name:
                return {'message': 'Course already exists'}, HTTPStatus.BAD_REQUEST
            
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
    @courses_namespace.marshal_with(course_retrieve_model)
    @courses_namespace.doc(
        description="""
            Every user can access this endpoint
            This returns a course by id
        """
    )
    def get(self, course_id):
        """Get a course by ID"""
        course = Course.get_by_id(course_id)
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        else:
            return course, HTTPStatus.OK

    @courses_namespace.doc(
        description="""
            Only admin can access this endpoint
            This deletes a course by id
        """
    )
    @admin_required()
    def delete(self, course_id):
        """Delete a course by ID"""
        
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
    @courses_namespace.marshal_with(student_field)
    @courses_namespace.doc(
        description="""
            Every user can access this endpoint
            This returns all the students in a course
        """
    )
    @admin_or_lecturer_required()
    def get(self, course_id):
        """
            List all registered students in a course
        """

        course = Course.get_by_id(course_id)
        get_course_student = StudentCourse.get_students_in_course_by(course.id)
        return get_course_student, HTTPStatus.OK
    

@courses_namespace.route('/addcourse/<int:course_id>')
class AddDeleteCourse(Resource):
    @courses_namespace.expect(student_course_field)
    @courses_namespace.doc(
        description="""
            Only lecturer can access this endpoint
            It allows a lecturer to add a student to their course
        """
    )
    @lecturer_required()
    def post(self, course_id):
        """
            Register a Student to a course 
        """
        data = request.get_json()
        student_id = data.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {
                'message': "Student or Course not found"
            }, HTTPStatus.NOT_FOUND
        
        if student:
            student_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if student_course:
                return {
                    'message': "{} has already registered for this course".format(student.name)
                }, HTTPStatus.OK
            else:
                student_course = StudentCourse(student_id=student.id, course_id=course.id)
                student_course.save()
                return {
                    'message': "{} registered for the {} course successfully".format(student.name, course.name)
                }, HTTPStatus.CREATED
            
    
    @courses_namespace.doc(
        description="""
            Only lecturer can access this endpoint
            It allows a lecturer to remove a student from their course
        """
    )
    @courses_namespace.expect(student_course_field)
    @lecturer_required()
    def delete(self, course_id):
        """
            Delete a Student from a course
        """
        data = request.get_json()
        student_id = data.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {
                'message': "Student or Course not found"
            }, HTTPStatus.NOT_FOUND
        
        if student:
            student_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if not student_course:
                return {
                    'message': "{} has not registered for this course".format(student.name)
                }, HTTPStatus.OK
            else:
                student_course.delete()
                return {
                    'message': "{} removed from the {} course".format(student.name, course.name)
                }, HTTPStatus.OK
