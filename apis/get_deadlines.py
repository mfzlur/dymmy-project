from flask import jsonify
from flask_restful import Resource
from datetime import datetime
from sqlalchemy import and_
from models import  Assignment



class GetDeadlines(Resource):
    def get(self):
        today = datetime.now().date()
        
        upcoming_deadlines = Assignment.query.filter(
            and_(
                Assignment.due_date >= today,
                Assignment.submitted == False
            )
        ).order_by(Assignment.due_date).limit(3).all()

        deadlines_list = []
        for deadline in upcoming_deadlines:
            # Get the course name through the relationship
            course_name = deadline.course.name
            
            deadlines_list.append({
                'id': deadline.id,
                'week': deadline.week,
                'course_name': course_name,  
                'due_date': deadline.due_date.isoformat(),
            })

        return jsonify({
            'deadlines': deadlines_list,
        })


