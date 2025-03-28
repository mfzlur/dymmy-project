"""
Tests for recommendations API endpoints.
Tests the RecommendationsAPI class and its methods.
"""

import unittest
import json
from main import app
from models import db, Recommendation


class RecommendationsAPITest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            recommendation1 = Recommendation(
                content="Try the advanced algorithms course next"
            )
            recommendation2 = Recommendation(
                content="Complete the machine learning assignments"
            )
            db.session.add_all([recommendation1, recommendation2])
            db.session.commit()
            self.recommendation_id = recommendation1.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_recommendations(self):
        response = self.app.get('/recommendations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['content'], "Try the advanced algorithms course next")
        self.assertEqual(data[1]['content'], "Complete the machine learning assignments")

    def test_get_specific_recommendation(self):
        response = self.app.get(f'/recommendations/{self.recommendation_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['content'], "Try the advanced algorithms course next")

    def test_post_recommendation(self):
        rec_data = {
            "content": "Review the database concepts before the exam"
        }
        response = self.app.post(
            '/recommendations',
            data=json.dumps(rec_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        with app.app_context():
            rec = Recommendation.query.get(data['id'])
            self.assertIsNotNone(rec)
            self.assertEqual(rec.content, "Review the database concepts before the exam")

    def test_put_recommendation(self):
        update_data = {
            "content": "Updated recommendation content"
        }
        response = self.app.put(
            f'/recommendations/{self.recommendation_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            rec = Recommendation.query.get(self.recommendation_id)
            self.assertEqual(rec.content, "Updated recommendation content")

    def test_delete_recommendation(self):
        response = self.app.delete(f'/recommendations/{self.recommendation_id}')
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            rec = Recommendation.query.get(self.recommendation_id)
            self.assertIsNone(rec)


if __name__ == '__main__':
    unittest.main()
