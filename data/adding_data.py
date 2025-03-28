from flask import Flask
from flask_restful import Api
from config import Config
from models import *
from flask_cors import CORS
from flask_migrate import Migrate
from data.mlt_GA1 import MLT_GA1
from data.mlt_GA2 import MLT_GA2
from data.mlt_GA3 import MLT_GA3
from data.mlt_GA4 import MLT_GA4
from data.dsa_GA1 import DSA_GA1
from data.dsa_GA2 import DSA_GA2
from data.dsa_GA3 import DSA_GA3
from data.dsa_GA4 import DSA_GA4
from data.config_tests import *


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)
CORS(app)



# Migrate database
migrate = Migrate(app, db)



with app.app_context():
    db.create_all()

    # Check if courses already exist before adding
    if not Course.query.filter_by(name="Machine Learning Techniques").first():
        course2 = Course(name="Machine Learning Techniques")
        db.session.add(course2)
    
    if not Course.query.filter_by(name="Data Structures and Algorithms").first():
        course1 = Course(name="Data Structures and Algorithms")
        db.session.add(course1)

    db.session.commit()  # Commit after course creation to get IDs

    # Fetch the courses again after commit
    course2 = Course.query.filter_by(name="Machine Learning Techniques").first()
    course1 = Course.query.filter_by(name="Data Structures and Algorithms").first()

    # Check if assignments already exist before adding
    if not Assignment.query.filter_by(week=1, course_id=course2.id).first():
        assignment1 = Assignment(week=1, course_id=course2.id, due_date=datetime(2025, 5, 5))
        db.session.add(assignment1)

    if not Assignment.query.filter_by(week=2, course_id=course2.id).first():
        assignment2 = Assignment(week=2, course_id=course2.id, due_date=datetime(2025, 5, 12))
        db.session.add(assignment2)

    if not Assignment.query.filter_by(week=3, course_id=course2.id).first():
        assignment3 = Assignment(week=3, course_id=course2.id, due_date=datetime(2025, 5, 19))
        db.session.add(assignment3)

    if not Assignment.query.filter_by(week=4, course_id=course2.id).first():
        assignment4 = Assignment(week=4, course_id=course2.id, due_date=datetime(2025, 5, 26))
        db.session.add(assignment4)

    db.session.commit()  # Commit after assignment creation to get IDs

    # Fetch assignments again after commit
    assign1_mlt = Assignment.query.filter_by(week=1, course_id=course2.id).first()
    assign2_mlt = Assignment.query.filter_by(week=2, course_id=course2.id).first()
    assign3_mlt = Assignment.query.filter_by(week=3, course_id=course2.id).first()
    assign4_mlt = Assignment.query.filter_by(week=4, course_id=course2.id).first()

    assign1_dsa = Assignment.query.filter_by(week=1, course_id=course1.id).first()
    assign2_dsa = Assignment.query.filter_by(week=2, course_id=course1.id).first()
    assign3_dsa = Assignment.query.filter_by(week=3, course_id=course1.id).first()
    assign4_dsa = Assignment.query.filter_by(week=4, course_id=course1.id).first()

    # Prevent duplicate questions
    def add_questions(assignment, question_data):
        for q_data in question_data:
            if not Question.query.filter_by(assignment_id=assignment.id, text=q_data["text"]).first():
                question = Question(
                    assignment_id=assignment.id,
                    text=q_data["text"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"]
                )
                db.session.add(question)

    add_questions(assign1_mlt, MLT_GA1)
    add_questions(assign2_mlt, MLT_GA2)
    add_questions(assign3_mlt, MLT_GA3)
    add_questions(assign4_mlt, MLT_GA4)
    add_questions(assign1_dsa, DSA_GA1)
    add_questions(assign2_dsa, DSA_GA2)
    add_questions(assign3_dsa, DSA_GA3)    
    add_questions(assign4_dsa, DSA_GA4)

    db.session.commit()

from data.dsa_lectures import dsa_lectures
from data.mlt_lectures import mlt_lectures

with app.app_context():
    for lecture in dsa_lectures:
        existing_lecture = Lecture.query.filter_by(title=lecture["title"]).first()
        if not existing_lecture:
            new_lecture = Lecture(**lecture)
            db.session.add(new_lecture)
    
    for lecture in mlt_lectures:
        existing_lecture = Lecture.query.filter_by(title=lecture["title"]).first()
        if not existing_lecture:
            new_lecture = Lecture(**lecture)
            db.session.add(new_lecture)
    
    db.session.commit()
    save_tests()


with app.app_context():
    # Create the table if it does not exist
    db.create_all()

    # Adding three records
    prog_assignments = [
        ProgrammingAssignment(course_id=1, week=1, question="Define a function solution(a,b,c). It should take as input three integers and return back the sum of the 3 integers."),
        ProgrammingAssignment(course_id=1, week=2, question="Define a function solution(a) that takes as input an integer a and return the square of the integer."),
        ProgrammingAssignment(course_id=1, week=3, question="Define a function solution which takes as input 3 variables x,y,z and returns the sum of the number of letters if the variable is a string otherwise add the integer value.")
    ]

    for assignment in prog_assignments:
        existing_assignment = ProgrammingAssignment.query.filter_by(
            course_id=assignment.course_id,
            week=assignment.week,
            question=assignment.question
        ).first()

        if not existing_assignment:
            db.session.add(assignment)  # Directly add the assignment object

    db.session.commit()
    print("Data inserted successfully!")


if __name__ == '__main__':
    # save_input()
    
    app.run(debug=True)

