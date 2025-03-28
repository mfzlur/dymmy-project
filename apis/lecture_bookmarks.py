from flask import request, jsonify
from flask_restful import Resource
from models import db, LectureBookmark, Lecture

class LectureBookmarksAPI(Resource):
    def get(self, lecture_id):
        """Fetch all bookmarks for a given lecture."""
        lecture = db.session.get(Lecture, lecture_id)
        if not lecture:
            return {"error": "Lecture not found"}, 404

        bookmarks = LectureBookmark.query.filter_by(lecture_id=lecture_id).all()
        return jsonify([
            {
                "id": bookmark.id,
                "timestamp": bookmark.timestamp,
                "remarks": bookmark.remarks
            }
            for bookmark in bookmarks
        ])

    def post(self, lecture_id):
        """Add a new bookmark to a lecture."""
        lecture = db.session.get(Lecture, lecture_id)
        if not lecture:
            return {"error": "Lecture not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        timestamp = data.get("timestamp")
        remarks = data.get("remarks", "")

        if timestamp is None:
            return {"error": "Timestamp is required"}, 400

        bookmark = LectureBookmark(lecture_id=lecture_id, timestamp=timestamp, remarks=remarks)
        db.session.add(bookmark)
        db.session.commit()

        return {"message": "Bookmark added successfully", "id": bookmark.id}

    def put(self, lecture_id):
        """Update an existing bookmark for a lecture."""
        lecture = db.session.get(Lecture, lecture_id)
        if not lecture:
            return {"error": "Lecture not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        bookmark_id = data.get("id")
        timestamp = data.get("timestamp")
        remarks = data.get("remarks")

        if not bookmark_id:
            return {"error": "Bookmark ID is required"}, 400

        bookmark = LectureBookmark.query.filter_by(id=bookmark_id, lecture_id=lecture_id).first()
        if not bookmark:
            return {"error": "Bookmark not found"}, 404

        if timestamp is not None:
            bookmark.timestamp = timestamp
        if remarks is not None:
            bookmark.remarks = remarks

        db.session.commit()
        return {"message": "Bookmark updated successfully"}

class DeleteLectureBookmarkAPI(Resource):
    def delete(self, bookmark_id):
        """Delete a bookmark."""
        bookmark = db.session.get(LectureBookmark, bookmark_id)
        if not bookmark:
            return {"error": "Bookmark not found"}, 404

        db.session.delete(bookmark)
        db.session.commit()
        return {"message": "Bookmark deleted successfully"}
