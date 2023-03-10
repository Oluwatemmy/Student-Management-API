from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.user import Student, User, Admin
from ..models.course import Course, StudentCourse, Score
from ..utils import db, letter_grade_to_gpa, grade
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from .serializers_utils import student_model, student_score_model, course_model, course_retrieve_model
from functools import wraps

student_namespace = Namespace('students', description='Students related operations')

student_field = student_namespace.model("Students List Model", student_model)

student_score_field = student_namespace.model("Student Score List Model", student_score_model)

course_field = student_namespace.model("Course List Model", course_model)

course_retrieve_field = student_namespace.model("Course Retrieve Model", course_retrieve_model)

gpa_field = student_namespace.model(
    "GPA Model", {
        'name': fields.String(required=True, description="Student Name"),
        'gpa': fields.Float(required=True, description="GPA"),
        'grade': fields.SyntaxWarning(required=True, description="Grade")
    }
)

@student_namespace.route('/student')
class GetStudentList(Resource):
    @student_namespace.marshal_with(student_field)
    @jwt_required()
    def get(self):
        """
            Get all students
        """
        authenticated_user_id = get_jwt_identity() 
        admin = Admin.query.filter_by(id=authenticated_user_id).first()   
        if not admin :
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        students = Student.query.all()
        return students , HTTPStatus.OK

@student_namespace.route('/student/<int:student_id>')
class GetUpdateDeleteStudent(Resource):
    @student_namespace.marshal_with(student_field)
    @jwt_required()
    def get(self, student_id):
        """
            Get a student by ID
        """
        # authenticated_user_id = get_jwt_identity() 
        # admin = Admin.query.filter_by(id=authenticated_user_id).first()   
        # if not admin :
        #     return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        return student, HTTPStatus.OK
    
    @student_namespace.expect(student_field)
    @student_namespace.marshal_with(student_field)
    @jwt_required()
    def put(self, student_id):
        """
            Update a student by ID
        """
        authenticated_user_id = get_jwt_identity() 
        student = Student.query.filter_by(id=authenticated_user_id).first()   
        if not student :
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        data = request.get_json()
        student.name = data['name']
        student.email = data['email']
        student.save()
        return student, HTTPStatus.OK
    
    @student_namespace.marshal_with(student_field)
    @jwt_required()
    def delete(self, student_id):
        """
            Delete a student by ID
        """
        authenticated_user_id = get_jwt_identity() 
        admin = Admin.query.filter_by(id=authenticated_user_id).first()   
        if not admin :
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        student.delete()
        return {'message': 'Student deleted successfully'}, HTTPStatus.OK
    

@student_namespace.route('/student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @student_namespace.marshal_with(course_field)
    @jwt_required()
    def get(self, student_id):
        """
            Get a student courses by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        student_courses = StudentCourse.get_courses_by_student_id(student_id)
        return student_courses, HTTPStatus.OK
    

@student_namespace.route('/studentcourse/')
class CreateDeleteStudentCourse(Resource):
    @student_namespace.marshal_with(course_retrieve_field)
    @student_namespace.expect(course_field)
    @jwt_required()
    def post(self):
        """
            Register a Student for a course 
        """
        authenticated_user_id = get_jwt_identity() 
        student = Student.query.filter_by(id=authenticated_user_id).first()   
        if not student :
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        data = request.get_json()
        course = Course.query.filter_by(id=data['course_id']).first()
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        
        if course:
            #check if student has registered for the course before
            student_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if student_course:
                return {'message': 'Student already registered for this course'}, HTTPStatus.BAD_REQUEST
        # Register a student for a course
        student_course = StudentCourse(student_id=student.id, course_id=course.id)
        try:
            student_course.save()
            return {
                'message': 'Student registered for course successfully',
            }, HTTPStatus.CREATED
        except:
            db.session.rollback()
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @student_namespace.expect(course_field)
    @jwt_required()
    def delete(self):
        """
            Delete a Student course
        """
        authenticated_user_id = get_jwt_identity() 
        student = Student.query.filter_by(id=authenticated_user_id).first()   
        if not student :
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        data = request.get_json()
        course = Course.query.filter_by(id=data['course_id']).first()
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        
        if course:
            #check if student has registered for the course before
            student_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if not student_course:
                return {'message': 'Student not registered for this course'}, HTTPStatus.BAD_REQUEST
            # Delete a student course
            if student_course:
                try:
                    student_course.delete()
                    return {
                        'message': 'Student deleted from course successfully',
                    }, HTTPStatus.OK
                except:
                    db.session.rollback()
                    return {'message': 'Something went wrong, Please try again'}, HTTPStatus.INTERNAL_SERVER_ERROR
                

@student_namespace.route('/studentcourse/score')
class UpdateStudentCourseScore(Resource):
    @student_namespace.expect(student_score_field)
    @jwt_required()
    def put(self):
        """
            Update a Student course score by the Course Lecturer
        """
        authenticated_user_id = get_jwt_identity() 
        data = request.get_json()
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        mark = data.get('score')
        user = User.query.filter_by(id=authenticated_user_id).first()
        if not user or user.user_type != 'lecturer':
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        
        # Check if Student and course already exists
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        
        if not student or not course:
            return {'message': 'Student or Course not found'}, HTTPStatus.NOT_FOUND
        
        # Check if the Lecturer is the course lecturer
        if course.lecturer_id != user.id :
            return {
                'message': 'You are not the course lecturer and you can not add score for this student in this course.'
            }, HTTPStatus.UNAUTHORIZED

        # Check if student is registered for the course
        student_course = StudentCourse.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not student_course:
            return {'message': 'Student not registered for this course'}, HTTPStatus.BAD_REQUEST
        
        if student_course:
            # Check is score already exists
            score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            percent = grade(mark)
            if score:
                score.score = mark
                score.percent = percent
            else:
                score = Score(student_id=student_id, course_id=course_id, score=mark, percent=percent)

            try:
                student_course.save()
                return {
                    'message': 'Student score updated successfully',
                }, HTTPStatus.OK
            except:
                db.session.rollback()
                return {'message': 'Something went wrong, Please try again'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

@student_namespace.route('/student/<int:student_id>/gpa')
class GetStudentGPA(Resource):
    @student_namespace.marshal_with(gpa_field)
    @jwt_required()
    def get(self, student_id):
        """
            Get a student GPA by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        if student:
            # Calculate the gpa here
            student_courses = StudentCourse.get_courses_by_student_id(student_id)
            if not student_courses:
                return {'message': 'Student not registered for any course'}, HTTPStatus.NOT_FOUND
            
            score = Score.query.filter_by(student_id=student_id).first()
            grades = student.percent.split(",")
            gpa = sum(letter_grade_to_gpa(grade) for grade in grades) / len(grades)
            student.gpa = round(gpa, 2)
            db.session.commit()
            return score, HTTPStatus.OK
            
            
            
            # gpa = 0
            # for course in student_courses:
            #     gpa += course.percent
            # gpa = gpa / len(student_courses)
            # return {
            #     'gpa': gpa
            # }, HTTPStatus.OK
        
