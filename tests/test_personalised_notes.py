"""
Tests for personalised notes API endpoints.
Tests the PersonalisedNotesAPI class and its methods.
"""

import unittest
import json
from main import app
from models import db, PersonalisedNote


class PersonalisedNotesAPITest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            note1 = PersonalisedNote(
                title="Test Personalised Note 1",
                content="Test personalised note content 1"
            )
            note2 = PersonalisedNote(
                title="Test Personalised Note 2",
                content="Test personalised note content 2"
            )
            db.session.add_all([note1, note2])
            db.session.commit()
            self.note_id = note1.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_notes(self):
        response = self.app.get('/personalised-notes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], "Test Personalised Note 1")
        self.assertEqual(data[1]['title'], "Test Personalised Note 2")

    def test_get_specific_note(self):
        response = self.app.get(f'/personalised-notes/{self.note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Personalised Note 1")
        self.assertEqual(data['content'], "Test personalised note content 1")

    def test_post_note(self):
        note_data = {
            "title": "New Personalised Note",
            "content": "New personalised note content"
        }
        
        response = self.app.post(
            '/personalised-notes',
            data=json.dumps(note_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        with app.app_context():
            note = PersonalisedNote.query.filter_by(title="New Personalised Note").first()
            self.assertIsNotNone(note)
            self.assertEqual(note.content, "New personalised note content")

    def test_put_note(self):
        update_data = {
            "title": "Updated Personalised Note",
            "content": "Updated personalised note content"
        }
        response = self.app.put(
            f'/personalised-notes/{self.note_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            note = PersonalisedNote.query.get(self.note_id)
            self.assertEqual(note.title, "Updated Personalised Note")
            self.assertEqual(note.content, "Updated personalised note content")

    def test_delete_note(self):
        response = self.app.delete(f'/personalised-notes/{self.note_id}')
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            note = PersonalisedNote.query.get(self.note_id)
            self.assertIsNone(note)


if __name__ == '__main__':
    unittest.main()
