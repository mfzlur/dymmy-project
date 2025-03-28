from flask import request, jsonify
from flask_restful import Resource
from models import db, PersonalisedNote


class PersonalisedNotesAPI(Resource):
    def get(self, note_id=None):
        """Fetch all personalised notes or a specific note."""
        if note_id:
            note = db.session.get(PersonalisedNote, note_id)
            if not note:
                return {"error": "Personalised note not found"}, 404
            return jsonify({
                "id": note.id,
                "title": note.title,
                "content": note.content
            })

        notes = PersonalisedNote.query.all()
        return jsonify([
            {"id": n.id, "title": n.title, "content": n.content} for n in notes
        ])

    def post(self):
        """Create a new personalised note."""
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return {"error": "Title and content are required"}, 400

        note = PersonalisedNote(title=title, content=content)
        db.session.add(note)
        db.session.commit()

        return {"message": "Personalised note added successfully", "id": note.id}

    def put(self, note_id):
        """Update an existing personalised note."""
        note = db.session.get(PersonalisedNote, note_id)
        if not note:
            return {"error": "Personalised note not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        title = data.get("title")
        content = data.get("content")

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content

        db.session.commit()
        return {"message": "Personalised note updated successfully"}

    def delete(self, note_id):
        """Delete a personalised note."""
        note = db.session.get(PersonalisedNote, note_id)
        if not note:
            return {"error": "Personalised note not found"}, 404

        db.session.delete(note)
        db.session.commit()
        return {"message": "Personalised note deleted successfully"}
