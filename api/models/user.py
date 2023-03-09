from ..utils import db
from datetime import datetime
from decouple import config
from itsdangerous import TimedSerializer as Serializer

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    user_type = db.Column(db.String(15))
    is_admin = db.Column(db.Boolean(), default=False)
    password_reset_token = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(config('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(config('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    nomination = db.Column(db.String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    matric_no = db.Column(db.String(50), unique=True)
    courses = db.relationship('Course', secondary='student_courses')
    score = db.relationship('Score', backref="student_score", lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Lecturer(User):
    __tablename__ = 'lecturers'
    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    staff_no = db.Column(db.String(50), unique=True)
    courses = db.relationship('Course', backref='lecturer_course')

    __mapper_args__ = {
        'polymorphic_identity': 'lecturer'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
