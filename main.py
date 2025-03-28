from flask import Flask
from flask_restful import Api
from config import Config
from models import *
from apis.course_info import Courses
from flask_cors import CORS
from flask_migrate import Migrate
from apis.ga import GradedAssignment
from apis.lecture_bookmarks import *
from apis.notes import *
from apis.feedback import *
from apis.personalised_notes import *
from apis.recommendations import *
from apis.instructor import *
from apis.instructor import *
from apis.questions import *
from apis.get_deadlines import GetDeadlines
from apis.get_performance_data import GetPerformanceData
from apis.prog_assignment_eval import ProgAssignment, ProgAssignments
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)
CORS(app)

# API endpoints

# Courses, Lectures, Notes
api.add_resource(Courses, "/courses", "/course/<int:course_id>")
api.add_resource(LectureBookmarksAPI, "/lecturebookmarks/<int:lecture_id>")
api.add_resource(DeleteLectureBookmarkAPI, "/lecturebookmarks/delete/<int:bookmark_id>")
api.add_resource(NotesAPI, "/notes/<int:course_id>")
api.add_resource(DeleteNotesAPI, "/notes/delete/<int:note_id>")

# Assignments Questions and Feedback
api.add_resource(GradedAssignment, 
                 "/ga/<int:course_id>", 
                 "/ga/<int:course_id>/<int:week_no>")
  

api.add_resource(ProgAssignment, '/programming_assignment/<int:prog_assignment_id>')
api.add_resource(ProgAssignments, '/programming_assignments')
api.add_resource(QuestionList, '/questions')

# User, Instructor, Feedback, Recommendations and Personalised Notes
api.add_resource(FeedbackAPI, "/feedback", "/feedback/<int:feedback_id>")
api.add_resource(RecommendationsAPI, "/recommendations", "/recommendations/<int:recommendation_id>")
api.add_resource(PersonalisedNotesAPI, "/personalised-notes", "/personalised-notes/<int:note_id>")
api.add_resource(InstructorContentResource, '/instructor')

# Deadlines
api.add_resource(GetDeadlines, '/deadlines')

# Performance Data
api.add_resource(GetPerformanceData, '/performance-data', '/performance-data/<int:course_id>/<int:week_num>', '/performance-data/<int:course_id>')



# Migrate database
migrate = Migrate(app, db)


with app.app_context():

    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
