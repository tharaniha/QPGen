from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_mod = db.Column(db.Boolean, nullable=False)

    # Many-to-many relationship with subjects
    subjects = db.relationship(
        'Subject', secondary='user_subject', backref=db.backref('users', lazy=True)
    )

    def __repr__(self):
        return f"<User {self.firstname} - {self.email}>"

# Subject Model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # Subject code
    name = db.Column(db.String(150), nullable=False)  # Subject name
    semester = db.Column(db.Integer, nullable=False)  # Semester
    department = db.Column(db.String(100), nullable=False)  # Department
    academic_year = db.Column(db.Integer, nullable=False)  # Academic year
    regulations = db.Column(db.String(100), nullable=False)  # Regulations
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK to User (creator)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for creation

    # Relationship to CourseOutcome
    course_outcomes = db.relationship('CourseOutcome', backref='subject', lazy=True)

    def __repr__(self):
        return f"<Subject {self.code} - {self.name}>"

# Association Table for Many-to-Many Relationship
user_subject = db.Table(
    'user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

# Course Outcome Model
class CourseOutcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each Course Outcome
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)  # FK to Subject
    co_number = db.Column(db.String(10), nullable=False)  # CO identifier (e.g., CO1, CO2)
    description = db.Column(db.Text, nullable=False)  # Description of the Course Outcome

    # Relationship to Questions
    questions = db.relationship('Question', backref='course_outcome', lazy=True)

    def __repr__(self):
        return f"<CourseOutcome {self.co_number} for Subject {self.subject_id}>"

# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each question
    subject_code = db.Column(db.String(20), db.ForeignKey('subject.code'), nullable=False)  # FK to Subject (code)
    module_no = db.Column(db.Integer, nullable=False)  # Module number
    content = db.Column(db.Text, nullable=False)  # The question text
    marks = db.Column(db.Integer, nullable=False)  # Marks allocated to the question
    rbt_level = db.Column(db.String(10), nullable=False)  # RBT level (e.g., L1, L2, etc.)
    co_id = db.Column(db.Integer, db.ForeignKey('course_outcome.id'), nullable=False)  # FK to CourseOutcome
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK to User (creator)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for question creation
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Question {self.id}: {self.content[:30]}... (Subject: {self.subject_code})>"


class QuestionImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    # Relationship to Question
    question = db.relationship('Question', backref=db.backref('images', lazy=True))

    def __repr__(self):
        return f"<QuestionImage {self.filename}>"