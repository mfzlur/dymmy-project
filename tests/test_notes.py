"""
Tests for notes API endpoints.
Tests both NotesAPI and DeleteNotesAPI classes.
"""

import json
import pytest
from main import app
from models import db, Course, Note  


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def test_course():
    with app.app_context():
        course = Course(name="Test Course")
        db.session.add(course)
        db.session.commit()
        course_id = course.id
    
    return course_id

@pytest.fixture
def test_notes(test_course):
    note_ids = []
    with app.app_context():
        note1 = Note(
            course_id=test_course,
            content="Test note 1 content",
            title="Test Note 1",
            week=1
        )
        note2 = Note(
            course_id=test_course,
            content="Test note 2 content",
            title="Test Note 2",
            week=2
        )
        db.session.add_all([note1, note2])
        db.session.commit()
        note_ids = [note1.id, note2.id]
    
    return note_ids


def test_get_notes(client, test_course, test_notes):
    response = client.get(f'/notes/{test_course}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == "Test Note 1"
    assert data[1]['title'] == "Test Note 2"


def test_post_note(client, test_course):
    note_data = {
        "title": "New Test Note",
        "content": "New test note content",
        "week": 3
    }
    
    response = client.post(
        f'/notes/{test_course}',
        data=json.dumps(note_data),
        content_type='application/json'
    )
    
    assert response.status_code in [200, 201]
    data = json.loads(response.data)
    assert 'id' in data
    
    with app.app_context():
        note = Note.query.get(data['id'])
        assert note is not None
        assert note.title == "New Test Note"
        assert note.content == "New test note content"
        assert note.week == 3


def test_put_note(client, test_course, test_notes):
    note_id = test_notes[0]
    
    update_data = {
        "id": note_id,
        "title": "Updated Note Title",
        "content": "Updated note content"
    }
    
    response = client.put(
        f'/notes/{test_course}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    with app.app_context():
        note = Note.query.get(note_id)
        assert note.title == "Updated Note Title"
        assert note.content == "Updated note content"


def test_delete_note(client, test_notes):
    note_id = test_notes[0]
    
    response = client.delete(f'/notes/delete/{note_id}')
    assert response.status_code == 200
    
    with app.app_context():
        note = Note.query.get(note_id)
        assert note is None