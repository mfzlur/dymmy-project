"""
Tests for programming assignment evaluation API endpoints.
Tests both ProgAssignment and ProgAssignments classes.
"""
import unittest
import json
from main import app
from models import db, ProgrammingAssignment, TestCases, Course


class ProgAssignmentsTest(unittest.TestCase):
    """Test cases for ProgAssignments API."""
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create a test course
            course = Course(name="Test Programming Course")
            db.session.add(course)
            db.session.commit()
            self.course_id = course.id
            
            # Create test programming assignments using only the valid field "question"
            prog_assignment1 = ProgrammingAssignment(
                course_id=self.course_id,
                question="Create a function to add two numbers",
                week=1
            )
            prog_assignment2 = ProgrammingAssignment(
                course_id=self.course_id,
                question="Create a function to reverse a string",
                week=2
            )
            db.session.add_all([prog_assignment1, prog_assignment2])
            db.session.commit()
            self.prog_assignment_id = prog_assignment1.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_assignments(self):
        response = self.app.get('/programming_assignmnets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['question'], "Create a function to add two numbers")
        self.assertEqual(data[1]['question'], "Create a function to reverse a string")


class ProgAssignmentTest(unittest.TestCase):
    """Test cases for ProgAssignment API."""
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create a test course
            course = Course(name="Test Programming Course")
            db.session.add(course)
            db.session.commit()
            self.course_id = course.id
            
            # Create a test programming assignment using only the valid field "question"
            prog_assignment = ProgrammingAssignment(
                course_id=self.course_id,
                question="Create a function to add two numbers",
                week=1
            )
            db.session.add(prog_assignment)
            db.session.commit()
            self.prog_assignment_id = prog_assignment.id
            
            # Create test cases using the valid key "progassignment_id"
            test_case1 = TestCases(
                progassignment_id=self.prog_assignment_id,
                input="[1, 2]",
                output="3"
            )
            test_case2 = TestCases(
                progassignment_id=self.prog_assignment_id,
                input="[-1, 5]",
                output="4"
            )
            db.session.add_all([test_case1, test_case2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_assignment(self):
        response = self.app.get(f'/programming_assignmnet/{self.prog_assignment_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['question'], "Create a function to add two numbers")
    
    def test_post_assignment_evaluation(self):
        # Test with correct solution code
        correct_solution = """
def solution(a, b):
    return a + b
"""
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": correct_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(results))  # All test cases should pass
        
        # Test with incorrect solution code
        incorrect_solution = """
def solution(a, b):
    return a - b
"""
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": incorrect_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        self.assertFalse(all(results))  # Some test cases should fail
        
        # Test with code that raises an exception
        error_solution = """
def solution(a, b):
    return a / 0
"""
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": error_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        # Results should contain error messages
        self.assertTrue(isinstance(results[0], str))
        
        # Test with missing code
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with non-existent assignment ID
        response = self.app.post(
            '/programming_assignmnet/9999',
            json={"code": correct_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
