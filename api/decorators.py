from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from .models.user import User
from http import HTTPStatus


def get_user_type(ui:int):
    """
        Get user type
        
        Args:
            ui (int): User id
    """

    user = User.query.filter_by(id=ui).first()

    if user:
        return user.user_type
    else:
        return None
    

def admin_required():
    """
        Admin required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            return {
                'message': 'Admin access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper

def lecturer_required():
    """
        Lecturer required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if get_user_type(user_id['sub']) == 'lecturer':
                return fn(*args, **kwargs)
            return {
                'message': 'Lecturer access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def student_required():
    """
        Student required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if get_user_type(user_id['sub']) == 'student':
                return fn(*args, **kwargs)
            return {
                'message': 'Student access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def admin_or_lecturer_required():
    """
        Admin or lecturer required decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt()
            print(user_id)
            if get_user_type(user_id['sub']) == 'admin' or get_user_type(user_id['sub']) == 'lecturer':
                return fn(*args, **kwargs)
            return {
                'message': 'Admin or lecturer access required'
            }, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper
