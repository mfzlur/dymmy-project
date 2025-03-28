"""
Tests for feedback API endpoints.
Tests the FeedbackAPI class and its methods.
"""

import unittest
import json
from main import app
from models import db, Feedback


class FeedbackAPITest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            feedback1 = Feedback(
                title="Test Feedback 1",
                conmment="Test feedback content 1",
                attachments="attachment1.pdf"
            )
            feedback2 = Feedback(
                title="Test Feedback 2",
                conmment="Test feedback content 2",
                attachments="attachment2.pdf"
            )
            db.session.add_all([feedback1, feedback2])
            db.session.commit()
            self.feedback_id = feedback1.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_feedback(self):
        response = self.app.get('/feedback')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], "Test Feedback 1")
        self.assertEqual(data[1]['title'], "Test Feedback 2")

    def test_get_specific_feedback(self):
        response = self.app.get(f'/feedback/{self.feedback_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Feedback 1")
        
        if 'comment' in data:
            self.assertEqual(data['comment'], "Test feedback content 1")
        elif 'conmment' in data:
            self.assertEqual(data['conmment'], "Test feedback content 1")
        else:
            self.fail("Neither 'comment' nor 'conmment' field found in response")

    def test_post_feedback(self):
        feedback_data = {
            "title": "New Feedback",
            "comment": "New feedback content",
            "attachments": "new_attachment.pdf"
        }
        response = self.app.post(
            '/feedback',
            data=json.dumps(feedback_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        with app.app_context():
            feedback = Feedback.query.filter_by(title="New Feedback").first()
            self.assertIsNotNone(feedback)
            self.assertEqual(feedback.conmment, "New feedback content")

    def test_delete_feedback(self):
        response = self.app.delete(f'/feedback/{self.feedback_id}')
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            feedback = Feedback.query.get(self.feedback_id)
            self.assertIsNone(feedback)


if __name__ == '__main__':
    unittest.main()
