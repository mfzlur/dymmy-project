from flask import Flask, jsonify
from flask_restful import Resource
from models import db, Question

class QuestionList(Resource):
    def get(self):
        questions = Question.query.all()
        if not questions:
            return {"message": "No questions found"}, 404
            
        data = []
        for q in questions:
            # Check if assignment exists before accessing its properties
            if q.assignment:
                week = q.assignment.week
            else:
                week = None
                
            data.append({
                "id": q.id,
                "text": q.text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "user_answer": q.user_answer,
                "week": week  # Get `week` from `Assignment` table
            })
        return jsonify(data)
