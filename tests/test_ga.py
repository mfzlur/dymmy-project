"""
Tests for graded assignments API endpoints.
Tests the GradedAssignment class and its methods.
"""

import unittest
import json
from datetime import datetime
from main import app
from models import db, Course, Assignment, Question


class GradedAssignmentTest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            course = Course(name="Test Course")
            db.session.add(course)
            db.session.commit()
            self.course_id = course.id
            
            assignment1 = Assignment(
                course_id=self.course_id,
                week=1,
                due_date=datetime(2023, 12, 1)
            )
            assignment2 = Assignment(
                course_id=self.course_id,
                week=2,
                due_date=datetime(2023, 12, 15)
            )
            db.session.add_all([assignment1, assignment2])
            db.session.commit()
            self.assignment_id = assignment1.id

            # Add questions to the assignment for the post test
            question1 = Question(
                assignment_id=self.assignment_id,
                text="What is 1+1?",
                options=["1", "2", "3", "4"],
                correct_answer=1  # Second option (index 1) is correct
            )
            question2 = Question(
                assignment_id=self.assignment_id,
                text="What is the capital of France?",
                options=["London", "Berlin", "Paris", "Madrid"],
                correct_answer=2  # Third option (index 2) is correct
            )
            db.session.add_all([question1, question2])
            db.session.commit()
            self.question1_id = question1.id
            self.question2_id = question2.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_assignments(self):
        response = self.app.get(f'/ga/{self.course_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['week'], 1)
        self.assertEqual(data[1]['week'], 2)

    def test_post_assignment_submission(self):
        answers = {
            "answers": {
                str(self.question1_id): 1,  # Correct answer
                str(self.question2_id): 1   # Incorrect answer
            }
        }
        
        response = self.app.post(
            f'/ga/{self.course_id}/{self.assignment_id}',
            data=json.dumps(answers),
            content_type='application/json'
        )
        
        # The API returns a 200 status and the score
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('score', data)
        
        # Check that the assignment was marked as submitted
        with app.app_context():
            assignment = Assignment.query.get(self.assignment_id)
            self.assertTrue(assignment.submitted)
            # Score should be 50% (1 correct out of 2)
            self.assertEqual(assignment.score, 50.0)


if __name__ == '__main__':
    unittest.main()
