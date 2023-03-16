from flask_restx import fields


student_model = {
    'id': fields.String(),
    'username': fields.String(required=False, description='Username of the Student'),
    'email': fields.String(required=True, description='Students email address'),
    'name': fields.String(required=True, description="Name of the Student"),
    'matric_no': fields.String(required=True, description="Admission Number of the Student"),
}

update_student_model = {
    'name': fields.String(required=True, description="Name of the Student"),
    'email': fields.String(required=True, description="Email of the Student")
}

student_score_model = {
    'student_id': fields.Integer(required=False, description='ID of student'),
    'score': fields.Integer(required=True, description="Score value"),
}

course_model = {
    'student_id': fields.Integer(required=True),
}

course_retrieve_model =  {
    'id': fields.Integer(),
    'name': fields.String(required=True, description="A course name"),
    'course_code': fields.String(description="A course code"),
    'lecturer_id': fields.Integer(), 
    'created_at': fields.DateTime( description="Course creation date"),
}

create_course_model = {
    'name': fields.String(required=True, description="A course name"),
    'lecturer_id': fields.Integer(required=True, description="Course Lecturer ID")
}

student_register_for_course_model = {
    'student_id': fields.Integer(required=True, description='ID of student'),
}

course_lecturer_model = {
    'username': fields.String(required=True, description='Username of the Lecturer'),
    'email': fields.String(required=True, description='Lecturer email address'),
    'Name': fields.String(required=True, description="Name of the Lecturer"),
    'staff_no': fields.String(required=True, description="COurse Lecturer ID"),
    'created_at': fields.DateTime( description="Course creation date")
}

gpa_model = {
    'student_id': fields.String(required=True, description="Student Name"),
    'gpa': fields.Float(required=True, description="GPA"),
    'score': fields.String(required=True, description="Grade"),
    'percent': fields.String(required=True, description="Percentage")
}
