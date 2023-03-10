from flask_restx import fields



student_model = {
    'id': fields.String(),
    'username': fields.String(required=False, description='Username of the Student'),
    'email': fields.String(required=True, description='Students email address'),
    'Name': fields.String(required=True, description="Name of the Student"),
    'Matric_no': fields.String(required=True, description="Admission Number of the Student"),
}



student_score_model = {
    'student_id': fields.Integer(required=False, description='ID of student'),
    'course_id': fields.Integer(required=True, description='ID of course'),
    'score': fields.Integer(required=True, description="Score value"),
}



course_model = {
    'course_id': fields.String(required=True),
}

course_retrieve_model =  {
    'id': fields.Integer(),
    'name': fields.String(required=True, description="A course name"),
    'course_code': fields.String(description="A course code"),
    'lecturer_id': fields.Integer(), 
    'created_at': fields.DateTime( description="Course creation date"),
}