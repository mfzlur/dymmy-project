from flask import jsonify
from flask_restful import Resource
from sqlalchemy import and_, func
from datetime import datetime
from models import Course, Assignment, Question

class GetPerformanceData(Resource):
    def get(self, course_id=None, week_num=None):
        # Initialize performance data
        performance_data = []

        if course_id:
            courses = Course.query.filter_by(id=course_id).all()
        else:
            courses = Course.query.all()

        for course in courses:
            if week_num:
                assignments = Assignment.query.filter_by(course_id=course.id, week=week_num).all()
            else:
                assignments = Assignment.query.filter_by(course_id=course.id).order_by(Assignment.week).all()

            # Initialize week-wise data structure
            weeks_data = {}

            for assignment in assignments:
                week_number = assignment.week

                # Skip if this assignment has no questions
                if not assignment.questions:
                    continue

                # Initialize week data if not already present
                if week_number not in weeks_data:
                    weeks_data[week_number] = {
                        "correctly_solved_questions": [],
                        "incorrectly_solved_questions": [],
                        "unanswered_questions": [],
                        "total_questions": 0,
                        "score": assignment.score,
                    }

                # Process each question in the assignment
                for question in assignment.questions:
                    weeks_data[week_number]["total_questions"] += 1

                    # Skip unanswered questions
                    if question.user_answer == -1:
                        weeks_data[week_number]["unanswered_questions"].append({
                            "question": question.text
                        })

                    # Check if user's answer is correct
                    elif question.user_answer == question.correct_answer:
                        weeks_data[week_number]["correctly_solved_questions"].append({
                            "question": question.text,
                        })
                    else:
                        weeks_data[week_number]["incorrectly_solved_questions"].append({
                            "question": question.text,
                        })

            # Format the course data
            course_data = {
                "course_id": course.id,
                "course_name": course.name,
                "progress_percentage": course.progress_percentage,
                "weeks_performance": []
            }

            # Convert weeks_data dictionary to a list for the response
            for week_num, week_data in sorted(weeks_data.items()):
                week_data["week"] = week_num
                course_data["weeks_performance"].append(week_data)

            performance_data.append(course_data)

        return jsonify({
            "performance_data": performance_data,
            "current_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_courses": len(performance_data)
        })
