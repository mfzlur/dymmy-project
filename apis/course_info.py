from flask import request, jsonify
from flask_restful import Resource
from models import db, Course


class Courses(Resource):
    def get(self, course_id=None):  # Make course_id optional
        if course_id:
            # Replace Course.query.get() with db.session.get()
            course = db.session.get(Course, course_id)
            if not course:
                return {"error": "Course not found"}, 404

            response = {
                "id": course.id,
                "name": course.name,
                "progress_percentage": course.progress_percentage,
                "assignments": [
                    {
                        "id": assignment.id,
                        "week": assignment.week,
                        "due_date": assignment.due_date.strftime('%Y-%m-%d'),
                        "submitted": assignment.submitted,
                        "score": assignment.score,
                        "course_id": assignment.course_id
                    }
                    for assignment in course.assignments
                ],
                "lectures": [
                    {   
                        "id": lecture.id,
                        "week": lecture.week,
                        "title": lecture.title,
                        "video_url": lecture.video_url,
                        "video_embed_code": lecture.video_embed_code,
                        "transcript_url": lecture.transcript_url,
                        "bookmarks": [
                            {
                                "id": bookmark.id,
                                "timestamp": bookmark.timestamp,
                                "remarks": bookmark.remarks
                            } for bookmark in lecture.bookmarks
                        ]
                    } for lecture in course.lectures
                ],
                "notes": [
                    {
                        "id": note.id,
                        "course_id": note.course_id,
                        "week": note.week,
                        "title": note.title,
                        "content": note.content
                    } for note in course.notes
                ]
            }
            
            return jsonify(response)
        else:
            courses = Course.query.all()
            response = [
                {
                    "id": course.id,
                    "name": course.name,
                    "assignments": [
                        {
                            "id": assignment.id,
                            "week": assignment.week,
                            "due_date": assignment.due_date.strftime('%Y-%m-%d'),
                            "submitted": assignment.submitted,
                            "score": assignment.score,
                        }
                        for assignment in course.assignments
                    ],
                    "progress_percentage": course.progress_percentage
                }
                for course in courses
            ]

            return jsonify(response)
