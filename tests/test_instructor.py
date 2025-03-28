"""
Tests for instructor content API endpoints.
Tests the InstructorContentResource class and its methods.
"""

import unittest
import json
from main import app
from models import db, InstructorContent


class InstructorContentResourceTest(unittest.TestCase):
    """Test cases for InstructorContentResource."""
    
    def setUp(self):
        """Set up test client and create test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create test instructor content
            content1 = InstructorContent(
                difficult_topics="Recursion, Dynamic Programming",
                most_frequent_doubts="How to optimize algorithms?",
                average_assignment_scores=78.5,
                quiz_completion_rates=85.2,
                avg_lecture_watch_time_percentage=76.3
            )
            content2 = InstructorContent(
                difficult_topics="Object-Oriented Programming, Design Patterns",
                most_frequent_doubts="How to structure large applications?",
                average_assignment_scores=82.1,
                quiz_completion_rates=88.7,
                avg_lecture_watch_time_percentage=79.5
            )
            db.session.add_all([content1, content2])
            db.session.commit()
            self.content_id = content1.id

    def tearDown(self):
        """Clean up after test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_content(self):
        """Test fetching all instructor content."""
        response = self.app.get('/content')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn('difficult_topics', data[0])
        self.assertIn('most_frequent_doubts', data[0])
        self.assertIn('average_assignment_scores', data[0])

    def test_get_specific_content(self):
        """Test fetching specific instructor content."""
        response = self.app.get(f'/content/{self.content_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['difficult_topics'], "Recursion, Dynamic Programming")
        self.assertEqual(data['most_frequent_doubts'], "How to optimize algorithms?")
        self.assertEqual(data['average_assignment_scores'], 78.5)


if __name__ == '__main__':
    unittest.main()
