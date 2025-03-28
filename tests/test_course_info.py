"""
Tests for course information API endpoints.
Tests the Courses class and its methods.
"""

import unittest
import json
from main import app
from models import db, Course, Lecture


class CoursesAPITest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            course1 = Course(name="Python Programming")
            course2 = Course(name="Web Development")
            db.session.add_all([course1, course2])
            db.session.commit()
            
            self.course_id = course1.id
            
            lecture1 = Lecture(
                title="Python Basics", 
                course_id=self.course_id, 
                video_url="https://test.com/1", 
                week=1,
                video_embed_code="<iframe src='https://test.com/embed/1'></iframe>"
            )
            lecture2 = Lecture(
                title="Python Functions", 
                course_id=self.course_id, 
                video_url="https://test.com/2", 
                week=1,
                video_embed_code="<iframe src='https://test.com/embed/2'></iframe>"
            )
            db.session.add_all([lecture1, lecture2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_courses(self):
        response = self.app.get('/courses')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Python Programming")
        self.assertEqual(data[1]['name'], "Web Development")

    def test_get_specific_course(self):
        response = self.app.get(f'/course/{self.course_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Python Programming")
        self.assertIn('lectures', data)
        self.assertEqual(len(data['lectures']), 2)

    def test_get_nonexistent_course(self):
        # Test requesting a nonexistent course - returns 404 status
        nonexistent_id = 9999  # ID that doesn't exist
        response = self.app.get(f'/course/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()