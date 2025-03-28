"""
Tests for questions API endpoints.
Tests the Questions class and its methods.
"""

import unittest
import json
from main import app
from models import db, Course, Assignment, Question


class QuestionsAPITest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create a test course
            course = Course(name="Test Course")
            db.session.add(course)
            db.session.commit()
            self.course_id = course.id
            
            # Create a test assignment
            assignment = Assignment(
                course_id=self.course_id,
                week=1
            )
            db.session.add(assignment)
            db.session.commit()
            self.assignment_id = assignment.id
            
            # Create test questions - using Question instead of AssignmentQuestion
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
            self.question_id = question1.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_questions(self):
        # Update the endpoint to match the API implementation
        response = self.app.get('/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) >= 2)
        # Since the order isn't guaranteed, we'll check if our questions exist in the response
        question_texts = [q['text'] for q in data]
        self.assertIn("What is 1+1?", question_texts)
        self.assertIn("What is the capital of France?", question_texts)

if __name__ == '__main__':
    unittest.main()
