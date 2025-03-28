"""
Tests for lecture bookmarks API endpoints.
Tests both LectureBookmarksAPI and DeleteLectureBookmarkAPI classes.
"""

import json
import pytest
from main import app
from models import db, Lecture, LectureBookmark, Course


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
def test_lecture(client):
    lecture_id = None
    with app.app_context():
        course = Course(name="Test Course")
        db.session.add(course)
        db.session.commit()
        course_id = course.id
        
        lecture = Lecture(
            title="Test Lecture", 
            course_id=course_id,
            video_url="https://test.com", 
            week=1,
            video_embed_code="<iframe src='https://test.com'></iframe>"
        )
        db.session.add(lecture)
        db.session.commit()
        lecture_id = lecture.id
    
    return lecture_id


@pytest.fixture
def test_bookmark(test_lecture):
    bookmark_id = None
    with app.app_context():
        bookmark = LectureBookmark(lecture_id=test_lecture, timestamp=60, remarks="Test Remark")
        db.session.add(bookmark)
        db.session.commit()
        bookmark_id = bookmark.id
    
    return bookmark_id


def test_get_bookmarks(client, test_lecture, test_bookmark):
    response = client.get(f'/lecturebookmarks/{test_lecture}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['remarks'] == "Test Remark"
    assert data[0]['timestamp'] == 60


def test_post_bookmark(client, test_lecture):
    bookmark_data = {
        "timestamp": 120,
        "remarks": "New Test Remark"
    }
    response = client.post(
        f'/lecturebookmarks/{test_lecture}',
        data=json.dumps(bookmark_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'id' in data
    
    with app.app_context():
        bookmark = LectureBookmark.query.get(data['id'])
        assert bookmark is not None
        assert bookmark.timestamp == 120
        assert bookmark.remarks == "New Test Remark"


def test_put_bookmark(client, test_lecture, test_bookmark):
    update_data = {
        "id": test_bookmark,
        "timestamp": 90,
        "remarks": "Updated Remark"
    }
    response = client.put(
        f'/lecturebookmarks/{test_lecture}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    with app.app_context():
        bookmark = LectureBookmark.query.get(test_bookmark)
        assert bookmark.timestamp == 90
        assert bookmark.remarks == "Updated Remark"


def test_delete_bookmark(client, test_bookmark):
    response = client.delete(f'/lecturebookmarks/delete/{test_bookmark}')
    assert response.status_code == 200
    
    try:
        data = json.loads(response.data)
        assert 'message' in data
    except json.JSONDecodeError:
        pass
    
    with app.app_context():
        bookmark = LectureBookmark.query.get(test_bookmark)
        assert bookmark is None
