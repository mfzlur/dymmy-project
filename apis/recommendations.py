from flask import request, jsonify
from flask_restful import Resource
from models import db, Recommendation

class RecommendationsAPI(Resource):
    def get(self, recommendation_id=None):
        """Fetch all recommendations or a specific recommendation."""
        if recommendation_id:
            recommendation = db.session.get(Recommendation, recommendation_id)
            if not recommendation:
                return {"error": "Recommendation not found"}, 404
            return jsonify({
                "id": recommendation.id,
                "content": recommendation.content
            })

        recommendations = Recommendation.query.all()
        return jsonify([
            {"id": rec.id, "content": rec.content} for rec in recommendations
        ])

    def post(self):
        """Create a new recommendation."""
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        content = data.get("content")

        if not content:
            return {"error": "Content is required"}, 400

        recommendation = Recommendation(content=content)
        db.session.add(recommendation)
        db.session.commit()

        return {"message": "Recommendation added successfully", "id": recommendation.id}

    def put(self, recommendation_id):
        """Update an existing recommendation."""
        recommendation = db.session.get(Recommendation, recommendation_id)
        if not recommendation:
            return {"error": "Recommendation not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        content = data.get("content")

        if content is not None:
            recommendation.content = content

        db.session.commit()
        return {"message": "Recommendation updated successfully"}

    def delete(self, recommendation_id):
        """Delete a recommendation."""
        recommendation = db.session.get(Recommendation, recommendation_id)
        if not recommendation:
            return {"error": "Recommendation not found"}, 404

        db.session.delete(recommendation)
        db.session.commit()
        return {"message": "Recommendation deleted successfully"}
