from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.user import Student, User, Admin
from ..models.course import Course, StudentCourse, Score
from ..utils import db, letter_grade_to_gpa, grade
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from .serializers_utils import student_model, student_score_model, course_model, course_retrieve_model, update_student_model
from functools import wraps

student_namespace = Namespace('students', description='Students related operations')

student_field = student_namespace.model("Students List Model", student_model)

student_score_field = student_namespace.model("Student Score List Model", student_score_model)

update_student_field = student_namespace.model("Student Update Model", update_student_model)

course_field = student_namespace.model("Course List Model", course_model)

course_retrieve_field = student_namespace.model("Course Retrieve Model", course_retrieve_model)

gpa_field = student_namespace.model(
    "GPA Model", {
        'name': fields.String(required=True, description="Student Name"),
        'gpa': fields.Float(required=True, description="GPA"),
        'grade': fields.String(required=True, description="Grade")
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
        if student:
            return student, HTTPStatus.OK
    
    @student_namespace.expect(update_student_field)
    @student_namespace.marshal_with(student_field)
    @jwt_required()
    def put(self, student_id):
        """
            Update a student by ID
        """
        # authenticated_user_id = get_jwt_identity() 
        # student = Student.query.filter_by(id=authenticated_user_id).first()   
        # if not student :
        #     return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        data = request.get_json()
        student.name = data.get('name')
        student.email = data.get('email')
        student.save()
        return student, HTTPStatus.OK
    
    @jwt_required()
    def delete(self, student_id):
        """
            Delete a student by ID
        """
        # authenticated_user_id = get_jwt_identity() 
        # admin = Admin.query.filter_by(id=authenticated_user_id).first()   
        # if not admin :
        #     return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        student.delete()
        return {'message': 'Student deleted from academy successfully'}, HTTPStatus.OK
    

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
    

@student_namespace.route('/addcourse/<int:course_id>')
class CreateDeleteStudentCourse(Resource):
    # @student_namespace.marshal_with(course_retrieve_field)
    @student_namespace.expect(course_field)
    @jwt_required()
    def post(self, course_id):
        """
            Register a Student for a course 
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
        
    # @student_namespace.expect(course_field)
    @jwt_required()
    def delete(self, course_id):
        """
            Delete a Student course
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
                

@student_namespace.route('/studentcourse/score/<int:course_id>')
class UpdateStudentCourseScore(Resource):
    @student_namespace.expect(student_score_field)
    @jwt_required()
    def put(self, course_id):
        """
            Update a Student course score by the Course Lecturer
        """
        authenticated_user_id = get_jwt_identity()
        data = request.get_json()
        student_id = data.get('student_id')
        score_value = data.get('score')
        teacher = User.query.filter_by(id=authenticated_user_id).first()   
        # check if student and course exist
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        #  check if teacher is the course teacher
        # if course.lecturer_id != teacher.id :
        #     return {'message':'You cannot add score for this student in this course'}, HTTPStatus.UNAUTHORIZED
        # check if student is registered for the course
        student_in_course = StudentCourse.query.filter_by(course_id=course.id, student_id=student.id).first() 
        if student_in_course:
            # check if the student already have a score in the course
            score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            gpa = grade(score_value)
            if score:
                score.score = score_value
                score.percent = gpa
            else:
                # create a new score object and save to database
                score = Score(student_id=student_id, course_id=course_id, score=score_value , percent=gpa)
            try:
                score.save()
                return {'message': 'Score added successfully'}, HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while saving student course score'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'The student is not registered for this course'}, HTTPStatus.BAD_REQUEST
        

@student_namespace.route('/student/<int:student_id>/gpa')
class GetStudentGPA(Resource):
    @student_namespace.marshal_with(gpa_field)
    @jwt_required()
    def get(self, student_id):
        """
            Calculate a Student GPA
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
            grades = score.percent.split(",")
            gpa = sum(letter_grade_to_gpa(grade) for grade in grades) / len(grades)
            score.gpa = round(gpa, 2)
            db.session.commit()
            return score, HTTPStatus.OK
            
            
            
            # gpa = 0
            # for course in student_courses:
            #     gpa += course.percent
            # gpa = gpa / len(student_courses)
            # return {
            #     'gpa': gpa
            # }, HTTPStatus.OK
