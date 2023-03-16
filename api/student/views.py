from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.user import Student
from ..models.course import Course, StudentCourse, Score
from ..utils import db, letter_grade_to_gpa, grade
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from .serializers_utils import student_model, student_score_model, course_model, course_retrieve_model, update_student_model, gpa_model
from ..decorators import admin_required, lecturer_required, student_required, admin_or_lecturer_required


student_namespace = Namespace('students', description='Students related operations')

student_field = student_namespace.model("Students List Model", student_model)

student_score_field = student_namespace.model("Student Score List Model", student_score_model)

update_student_field = student_namespace.model("Student Update Model", update_student_model)

course_field = student_namespace.model("Course List Model", course_model)

course_retrieve_field = student_namespace.model("Course Retrieve Model", course_retrieve_model)

gpa_field = student_namespace.model("GPA Model", gpa_model)

@student_namespace.route('/')
class GetStudentList(Resource):
    @student_namespace.marshal_with(student_field)
    @student_namespace.doc(
        description="""
            Only admin can access this endpoint
            This returns all the students in the academy
        """
    )
    @admin_required()
    def get(self):
        """
            Get all students
        """
        students = Student.query.all()
        return students , HTTPStatus.OK

@student_namespace.route('/<int:student_id>')
class GetUpdateDeleteStudent(Resource):
    @student_namespace.marshal_with(student_field)
    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the retrieval of a particular student 
        """
    )
    @admin_or_lecturer_required()
    def get(self, student_id):
        """
            Get a student by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        if student:
            return student, HTTPStatus.OK
    
    @student_namespace.expect(update_student_field)
    @student_namespace.marshal_with(student_field)
    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the update of a particular student
        """
    )
    @admin_or_lecturer_required()
    def put(self, student_id):
        """
            Update a student by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        data = request.get_json()
        student.name = data.get('name')
        student.email = data.get('email')
        student.save()
        return student, HTTPStatus.OK
    
    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the deletion of a particular student from the academy
        """
    )
    @admin_required()
    def delete(self, student_id):
        """
            Delete a student by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        student.delete()
        return {'message': 'Student deleted from academy successfully'}, HTTPStatus.OK
    

@student_namespace.route('/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @student_namespace.marshal_with(course_retrieve_field)
    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the retrieval of a particular student courses
        """
    )
    @admin_or_lecturer_required()
    def get(self, student_id):
        """
            Get a student courses by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        student_courses = StudentCourse.get_courses_by_student_id(student_id)
        return student_courses, HTTPStatus.OK
                

@student_namespace.route('/studentcourse/score/<int:course_id>')
class UpdateStudentCourseScore(Resource):
    @student_namespace.expect(student_score_field)
    @student_namespace.doc(
        description="""
            Only course lecturer can access this route
            This allow the update of a particular student score in a course
        """
    )
    @lecturer_required()
    def put(self, course_id):
        """
            Update a Student course score by the Course Lecturer
        """
        data = request.get_json()
        student_id = data.get('student_id')
        score_value = data.get('score')
        
        # check if student and course exist
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND

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
        

@student_namespace.route('/<int:student_id>/<int:course_id>/gpa')
class GetStudentGPA(Resource):
    @student_namespace.marshal_with(gpa_field)
    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the calculation of a particular student course GPA
        """
    )
    @admin_or_lecturer_required()
    def get(self, student_id, course_id):
        """
            Calculate a Student Course GPA
        """
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        
        if student:
            # Calculate the gpa here
            student_courses = StudentCourse.get_courses_by_student_id(student_id)
            if not student_courses:
                return {'message': 'Student not registered for any course'}, HTTPStatus.NOT_FOUND
            
            score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            grades = score.percent.split(",")
            gpa = sum(letter_grade_to_gpa(grade) for grade in grades) / len(grades)
            score.gpa = round(gpa, 2)
            db.session.commit()
            return score, HTTPStatus.OK
            


@student_namespace.route('/<int:student_id>/courses/grades')
class GetStudentCoursesGrades(Resource):

    @student_namespace.doc(
        description="""
            Only admins and lecturers can access this route
            This allow the retrieval of a particular student courses and grades
        """
    )
    @admin_or_lecturer_required()
    def get(self, student_id):
        """
            Get a student all courses and grades by ID
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        student_courses = StudentCourse.get_courses_by_student_id(student_id)
        if not student_courses:
            return {'message': 'Student not registered for any course'}, HTTPStatus.NOT_FOUND
        
        student_courses_grades = []
        for student_course in student_courses:
            course = Course.query.filter_by(id=student_course.id).first()
            score = Score.query.filter_by(student_id=student_id, course_id=student_course.id).first()
            if score:
                student_courses_grades.append({
                    'course_id': course.id,
                    'course_name': course.name,
                    'course_code': course.course_code,
                    'course_score': score.score,
                    'course_gpa': score.gpa,
                    'course_percent': score.percent
                })
            else:
                student_courses_grades.append({
                    'course_id': course.id,
                    'course_name': course.name,
                    'course_code': course.course_code,
                    'course_score': 'Not yet graded',
                    'course_gpa': 'Not yet graded',
                    'course_percent': 'Not yet graded'
                })
        return student_courses_grades, HTTPStatus.OK
