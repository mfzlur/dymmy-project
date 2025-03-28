from flask import request, jsonify
from flask_restful import Resource
from models import *


class GradedAssignment(Resource):
    def get(self, course_id, week_no=None):  
        # Check if course exists first
        if not course_id:
            return {"error": "Course not found"}, 404
            
        if not week_no:
            assignments = Assignment.query.filter_by(course_id=course_id).all()
        
            if not assignments:
                return {"message": "No assignments found for this course"}, 404

            response = [{
                "id": assignment.id,
                "week": assignment.week,
                "due_date": assignment.due_date.strftime('%Y-%m-%d'),
                "submitted": assignment.submitted,
                "score": assignment.score,
                "questions": [
                    {
                        "id": question.id,
                        "text": question.text,
                        "options": question.options,
                        "correct_answer": question.correct_answer,
                        "user_answer": question.user_answer
                    }
                    for question in assignment.questions
                ]
            } for assignment in assignments]

        else:
            assignment = Assignment.query.filter_by(week=week_no, course_id=course_id).first()
        
            if not assignment:
                return {"message": "No assignments found for this course"}, 404

            response = {
                "id": assignment.id,
                "week": assignment.week,
                "due_date": assignment.due_date.strftime('%Y-%m-%d'),
                "submitted": assignment.submitted,
                "score": assignment.score,
                "questions": [
                    {
                        "id": question.id,
                        "text": question.text,
                        "options": question.options,
                        "correct_answer": question.correct_answer,
                        "user_answer": question.user_answer
                    }
                    for question in assignment.questions
                ]
            } 

        return jsonify(response)


    def post(self, course_id, week_no):
        # Check if course exists
        course = db.session.get(Course, course_id)
        if not course:
            return {"error": "Course not found"}, 404
            
        data = request.get_json()

        assignment = Assignment.query.filter_by(week=week_no, course_id=course_id).first()
        if not assignment:
            return {"error": "Assignment not found"}, 404
        

        correct_count = 0
        total_questions = len(assignment.questions)
        wrong_count = 0
        
        submitted_answers = data.get("answers", {})


        for question in assignment.questions:
            user_answer = submitted_answers.get(str(question.id))
           
            if user_answer is not None:
                question.user_answer = user_answer
                if user_answer == question.correct_answer:
                    correct_count += 1
                else:
                    wrong_count += 1

                

        assignment.score = round((correct_count / total_questions) * 100, 2)  # Calculate percentage score
        assignment.submitted = True
        db.session.commit()

        # Update course progress
        if course.assignments:
            total_submitted_assignments = sum(1 for a in course.assignments if a.submitted)
            course.progress_percentage = (total_submitted_assignments / len(course.assignments)) * 100
            db.session.commit()
        else:
            course.progress_percentage = 0
            db.session.commit()

        return {"message": "Graded assignment successfully", "score": assignment.score}, 200
    



