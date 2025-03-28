# Course API Tests
**Description:** These APIs have functionality related to course information retrieval including course details and lectures.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/courses```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_courses()```
Tests retrieving all courses from the database
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/courses
        - No parameters or body data sent
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of all courses
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "name": "Python Programming"
            },
            {
              "id": 2, 
              "name": "Web Development"
            }
          ]
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_courses(self):
            response = self.app.get('/courses')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], "Python Programming")
            self.assertEqual(data[1]['name'], "Web Development")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/course/{course_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_specific_course()```
Tests retrieving a specific course by ID
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/course/1 
        - Where self.course_id = 1 (based on the response data showing "Python Programming")
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Course details including lectures
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "name": "Python Programming",
            "lectures": [
              {
                "id": 1,
                "title": "Introduction to Python",
                "video_url": "https://example.com/python-intro",
                "week": 1
              },
              {
                "id": 2,
                "title": "Python Data Structures",
                "video_url": "https://example.com/python-data-structures",
                "week": 1
              }
            ]
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_specific_course(self):
            response = self.app.get(f'/course/{self.course_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['name'], "Python Programming")
            self.assertIn('lectures', data)
            self.assertEqual(len(data['lectures']), 2)
        ```

2. ```test_get_nonexistent_course()```
Tests retrieving a non-existent course
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/course/9999
        - Using nonexistent_id = 9999 (explicitly set in the test code)
    - Expected Output:
        - ```HTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
        - ```json
          {
            "error": "Course not found"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_nonexistent_course(self):
            nonexistent_id = 9999
            response = self.app.get(f'/course/{nonexistent_id}')
            self.assertEqual(response.status_code, 404)
        ```

# Feedback API Tests
**Description:** These APIs manage feedback functionality, allowing users to create, retrieve, and delete feedback.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/feedback```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_feedback()```
Tests retrieving all feedback entries
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/feedback
        - No parameters or body data sent
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of feedback entries
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "title": "Test Feedback 1",
              "conmment": "Test feedback content 1",
              "attachments": "test1.pdf"
            },
            {
              "id": 2,
              "title": "Test Feedback 2",
              "conmment": "Test feedback content 2",
              "attachments": "test2.pdf"
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_feedback(self):
            response = self.app.get('/feedback')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['title'], "Test Feedback 1")
            self.assertEqual(data[1]['title'], "Test Feedback 2")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.0.1:5000/feedback/{feedback_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_specific_feedback()```
Tests retrieving a specific feedback entry
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/feedback/1
        - Path parameter: feedback_id=1 (from self.feedback_id in setup)
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Details of the requested feedback
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "title": "Test Feedback 1",
            "conmment": "Test feedback content 1",
            "attachments": "test1.pdf"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_specific_feedback(self):
            response = self.app.get(f'/feedback/{self.feedback_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['title'], "Test Feedback 1")
            
            if 'comment' in data:
                self.assertEqual(data['comment'], "Test feedback content 1")
            elif 'conmment' in data:
                self.assertEqual(data['conmment'], "Test feedback content 1")
            else:
                self.fail("Neither 'comment' nor 'conmment' field found in response")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/feedback```
- **Method:** POST

##### Test Cases:
1. ```test_post_feedback()```
Tests creating a new feedback entry
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/feedback
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "title": "New Feedback",
            "comment": "New feedback content",
            "attachments": "new_attachment.pdf"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Response containing the new feedback ID
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 3,
            "message": "Feedback created successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_post_feedback(self):
            feedback_data = {
                "title": "New Feedback",
                "comment": "New feedback content",
                "attachments": "new_attachment.pdf"
            }
            response = self.app.post(
                '/feedback',
                data=json.dumps(feedback_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('id', data)
            
            with app.app_context():
                feedback = Feedback.query.filter_by(title="New Feedback").first()
                self.assertIsNotNone(feedback)
                self.assertEqual(feedback.conmment, "New feedback content")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/feedback/{feedback_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_feedback()```
Tests deleting feedback
    - Passed Inputs:
        - DELETE request to http://127.0.0.1:5000/feedback/1
        - Path parameter: feedback_id=1 (from self.feedback_id in setup)
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Feedback no longer exists in database
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Feedback deleted successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_delete_feedback(self):
            response = self.app.delete(f'/feedback/{self.feedback_id}')
            self.assertEqual(response.status_code, 200)
            
            with app.app_context():
                feedback = Feedback.query.get(self.feedback_id)
                self.assertIsNone(feedback)
        ```

# Graded Assignments API Tests
**Description:** These APIs handle graded assignments functionality, including retrieving assignments and submitting answers.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/ga/{course_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_assignments()```
Tests retrieving all graded assignments for a course
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/ga/1
        - Path parameter: course_id=1 (defined in self.course_id)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of assignments for the course
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "title": "Week 1 Assignment",
              "week": 1,
              "questions": [
                {
                  "id": 1,
                  "text": "What is a variable in Python?",
                  "options": ["A container for data", "A loop construct", "A function", "A module"]
                },
                {
                  "id": 2,
                  "text": "Which of these is a valid Python identifier?",
                  "options": ["my_var", "2var", "for", "class!"]
                }
              ],
              "deadline": "2023-12-10T23:59:59",
              "submitted": false
            },
            {
              "id": 2,
              "title": "Week 2 Assignment",
              "week": 2,
              "questions": [
                {
                  "id": 3,
                  "text": "What is a list comprehension?",
                  "options": ["A concise way to create lists", "A way to iterate lists", "A function", "None of these"]
                }
              ],
              "deadline": "2023-12-17T23:59:59",
              "submitted": false
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_assignments(self):
            response = self.app.get(f'/ga/{self.course_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['week'], 1)
            self.assertEqual(data[1]['week'], 2)
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/ga/{course_id}/{assignment_id}```
- **Method:** POST

##### Test Cases:
1. ```test_post_assignment_submission()```
Tests submitting answers for a graded assignment
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/ga/1/1
        - Path parameters: 
          - course_id=1 (defined in self.course_id)
          - assignment_id=1 (defined in self.assignment_id)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "answers": {
                "1": 1,  
                "2": 1   
            }
        }
        ```
        (where "1" and "2" are question IDs from self.question1_id and self.question2_id, and the values represent the selected answer options)
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Response containing score
        - Assignment marked as submitted with correct score
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "score": 50.0,
            "message": "Assignment submitted successfully",
            "correct_answers": 1,
            "total_questions": 2
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_post_assignment_submission(self):
            answers = {
                "answers": {
                    str(self.question1_id): 1,  # Correct answer
                    str(self.question2_id): 1   # Incorrect answer
                }
            }
            
            response = self.app.post(
                f'/ga/{self.course_id}/{self.assignment_id}',
                data=json.dumps(answers),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('score', data)
            
            with app.app_context():
                assignment = Assignment.query.get(self.assignment_id)
                self.assertTrue(assignment.submitted)
                self.assertEqual(assignment.score, 50.0)
        ```

# Instructor Content API Tests
**Description:** These APIs provide functionality for instructors to access aggregated content and analytics about student performance, difficult topics, and learning patterns.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/content```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_content()```
Tests retrieving all instructor content
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/content
        - No parameters or body data sent
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of instructor content entries
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "course_id": 1,
              "difficult_topics": "Recursion, Dynamic Programming",
              "most_frequent_doubts": "How to optimize algorithms?",
              "average_assignment_scores": 78.5,
              "student_performance_metrics": {
                "assignment_completion_rate": 87.2,
                "average_time_spent": 45.3
              }
            },
            {
              "id": 2,
              "course_id": 2,
              "difficult_topics": "CSS Flexbox, JavaScript Promises",
              "most_frequent_doubts": "How to center a div?",
              "average_assignment_scores": 82.1,
              "student_performance_metrics": {
                "assignment_completion_rate": 91.5,
                "average_time_spent": 38.7
              }
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_content(self):
            response = self.app.get('/content')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertIn('difficult_topics', data[0])
            self.assertIn('most_frequent_doubts', data[0])
            self.assertIn('average_assignment_scores', data[0])
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/content/{content_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_specific_content()```
Tests retrieving specific instructor content by ID
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/content/1
        - Path parameter: content_id=1 (from self.content_id)
        - No query parameters or body data
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Details of the specific instructor content
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "course_id": 1,
            "difficult_topics": "Recursion, Dynamic Programming",
            "most_frequent_doubts": "How to optimize algorithms?",
            "average_assignment_scores": 78.5,
            "student_performance_metrics": {
              "assignment_completion_rate": 87.2,
              "average_time_spent": 45.3
            },
            "recommended_focus_areas": [
              "Algorithm complexity analysis",
              "Dynamic programming patterns"
            ]
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_specific_content(self):
            response = self.app.get(f'/content/{self.content_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['difficult_topics'], "Recursion, Dynamic Programming")
            self.assertEqual(data['most_frequent_doubts'], "How to optimize algorithms?")
            self.assertEqual(data['average_assignment_scores'], 78.5)
        ```

# Lecture Bookmarks API Tests
**Description:** These APIs handle lecture bookmarks functionality, allowing users to save, update, retrieve, and delete bookmarks at specific timestamps in lecture videos.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/lecturebookmarks/{lecture_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_bookmarks()```
Tests retrieving bookmarks for a specific lecture
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/lecturebookmarks/1
        - Path parameter: lecture_id=1 (from test_lecture fixture)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of bookmarks for the lecture
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "lecture_id": 1,
              "timestamp": 60,
              "remarks": "Test Remark",
              "created_at": "2023-12-05T10:30:00"
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_bookmarks(client, test_lecture, test_bookmark):
            response = client.get(f'/lecturebookmarks/{test_lecture}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['remarks'] == "Test Remark"
            assert data[0]['timestamp'] == 60
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/lecturebookmarks/{lecture_id}```
- **Method:** POST

##### Test Cases:
1. ```test_post_bookmark()```
Tests creating a new bookmark for a lecture
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/lecturebookmarks/1
        - Path parameter: lecture_id=1 (from test_lecture fixture)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "timestamp": 120,
            "remarks": "New Test Remark"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Response containing message and bookmark ID
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Bookmark created successfully",
            "id": 2
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
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
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/lecturebookmarks/{lecture_id}```
- **Method:** PUT

##### Test Cases:
1. ```test_put_bookmark()```
Tests updating an existing bookmark
    - Passed Inputs:
        - PUT request to http://127.0.0.1:5000/lecturebookmarks/1
        - Path parameter: lecture_id=1 (from test_lecture fixture)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "id": 1,
            "timestamp": 90,
            "remarks": "Updated Remark"
        }
        ```
        (where id 1 is from test_bookmark fixture)
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Bookmark updated successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
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
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/lecturebookmarks/delete/{bookmark_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_bookmark()```
Tests deleting a bookmark
    - Passed Inputs:
        - DELETE request to http://127.0.0.1:5000/lecturebookmarks/delete/1
        - Path parameter: bookmark_id=1 (from test_bookmark fixture)
        - No request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Bookmark no longer exists in database
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Bookmark deleted successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
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
        ```

# Main Application Tests
**Description:** These tests verify the proper setup and configuration of the Flask application including database connectivity and route registration.

### Endpoint: 
- **URL:** Various application-level tests
- **Method:** Various

##### Test Cases:
1. ```test_app_exists()```
Tests that the Flask application exists
    - Passed Inputs:
        - Direct reference to the Flask application object 'app'
        - Internal assertion: self.assertIsNotNone(app)
    - Expected Output:
        - Application object should not be None
    - Actual Output:
        - Flask application object exists
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_app_exists(self):
            """Test that the Flask application exists."""
            self.assertIsNotNone(app)
        ```

2. ```test_app_is_testing()```
Tests that the application is in testing mode
    - Passed Inputs:
        - Check of app.config['TESTING'] configuration value
        - Internal assertion: self.assertTrue(app.config['TESTING'])
    - Expected Output:
        - app.config['TESTING'] should be True
    - Actual Output:
        - Testing mode confirmed enabled (app.config['TESTING'] = True)
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_app_is_testing(self):
            """Test that the application is in testing mode."""
            self.assertTrue(app.config['TESTING'])
        ```

3. ```test_database_connection()```
Tests that the database connection works properly
    - Passed Inputs:
        - SQLAlchemy execute command with text("SELECT 1")
        - SQL query executed within app context using db.session.execute()
    - Expected Output:
        - Query should execute successfully and return value 1
    - Actual Output:
        - Query executed successfully with result 1
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_database_connection(self):
            """Test that the database connection works."""
            with app.app_context():
                # Use SQLAlchemy 2.0 execution API
                result = db.session.execute(text("SELECT 1")).scalar()
                self.assertEqual(result, 1)
        ```

4. ```test_routes_are_registered()```
Tests that essential routes are correctly registered in the application
    - Passed Inputs:
        - Examination of app.url_map to retrieve all registered routes
        - Check for essential endpoints: '/courses', '/ga/', '/notes/'
    - Expected Output:
        - Key routes should be present in app.url_map
    - Actual Output:
        - Essential routes confirmed registered in the application:
          - /courses endpoint found
          - /ga/ endpoint found
          - /notes/ endpoint found
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_routes_are_registered(self):
            """Test that routes are correctly registered in the application."""
            # Get the map of all routes
            rules = list(app.url_map.iter_rules())
            rule_names = [rule.rule for rule in rules]  # Use rule.rule instead of rule.endpoint
            
            # Check that essential routes are registered
            self.assertTrue(any('/courses' in name for name in rule_names), "No courses route found")
            self.assertTrue(any('/ga/' in name for name in rule_names), "No graded assignments route found")
            self.assertTrue(any('/notes/' in name for name in rule_names), "No notes route found")
        ```

5. ```test_404_handling()```
Tests that 404 errors are handled properly
    - Passed Inputs:
        - GET request to non-existent route: "/nonexistentroute"
        - HTTP request using self.app.get() testing client
    - Expected Output:
        - ```HTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
        - Default 404 error handling correctly triggered
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_404_handling(self):
            """Test that 404 errors are handled properly."""
            response = self.app.get('/nonexistentroute')
            self.assertEqual(response.status_code, 404)
        ```

# Notes API Tests
**Description:** These APIs manage course-specific notes functionality, allowing users to create, retrieve, update, and delete notes.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/notes/{course_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_notes()```
Tests retrieving notes for a specific course
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/notes/1
        - Path parameter: course_id=1 (from test_course fixture)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of notes for the course
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "course_id": 1,
              "title": "Test Note 1",
              "content": "This is test note 1 content",
              "week": 1,
              "created_at": "2023-12-05T14:30:00"
            },
            {
              "id": 2,
              "course_id": 1,
              "title": "Test Note 2",
              "content": "This is test note 2 content",
              "week": 2,
              "created_at": "2023-12-06T15:45:00"
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_notes(client, test_course, test_notes):
            response = client.get(f'/notes/{test_course}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 2
            assert data[0]['title'] == "Test Note 1"
            assert data[1]['title'] == "Test Note 2"
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/notes/{course_id}```
- **Method:** POST

##### Test Cases:
1. ```test_post_note()```
Tests creating a new note for a course
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/notes/1
        - Path parameter: course_id=1 (from test_course fixture)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "title": "New Test Note",
            "content": "New test note content",
            "week": 3
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200``` or ```201```
        - Response containing the new note ID
    - Actual Output:
        - ```HTTP-Status Code: 201```
        - ```json
          {
            "id": 3,
            "message": "Note created successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_post_note(client, test_course):
            note_data = {
                "title": "New Test Note",
                "content": "New test note content",
                "week": 3
            }
            
            response = client.post(
                f'/notes/{test_course}',
                data=json.dumps(note_data),
                content_type='application/json'
            )
            
            assert response.status_code in [200, 201]
            data = json.loads(response.data)
            assert 'id' in data
            
            with app.app_context():
                note = Note.query.get(data['id'])
                assert note is not None
                assert note.title == "New Test Note"
                assert note.content == "New test note content"
                assert note.week == 3
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/notes/{course_id}```
- **Method:** PUT

##### Test Cases:
1. ```test_put_note()```
Tests updating an existing note
    - Passed Inputs:
        - PUT request to http://127.0.0.1:5000/notes/1
        - Path parameter: course_id=1 (from test_course fixture)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "id": 1,
            "title": "Updated Note Title",
            "content": "Updated note content"
        }
        ```
        (where id 1 is the first note from test_notes fixture)
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Note updated successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_put_note(client, test_course, test_notes):
            note_id = test_notes[0]
            
            update_data = {
                "id": note_id,
                "title": "Updated Note Title",
                "content": "Updated note content"
            }
            
            response = client.put(
                f'/notes/{test_course}',
                data=json.dumps(update_data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            
            with app.app_context():
                note = Note.query.get(note_id)
                assert note.title == "Updated Note Title"
                assert note.content == "Updated note content"
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/notes/delete/{note_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_note()```
Tests deleting a note
    - Passed Inputs:
        - DELETE request to http://127.0.0.1:5000/notes/delete/1
        - Path parameter: note_id=1 (first note from test_notes fixture)
        - No request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Note no longer exists in database
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Note deleted successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_delete_note(client, test_notes):
            note_id = test_notes[0]
            
            response = client.delete(f'/notes/delete/{note_id}')
            assert response.status_code == 200
            
            with app.app_context():
                note = Note.query.get(note_id)
                assert note is None
        ```

# Personalized Notes API Tests
**Description:** These APIs manage personalized notes functionality, allowing users to create, retrieve, update, and delete personalized notes.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/personalised-notes```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_notes()```
Tests retrieving all personalized notes
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/personalised-notes
        - No parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of all personalized notes
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "title": "Test Personalised Note 1",
              "content": "Test personalised note content 1",
              "created_at": "2023-12-04T09:15:00"
            },
            {
              "id": 2,
              "title": "Test Personalised Note 2",
              "content": "Test personalised note content 2",
              "created_at": "2023-12-05T10:30:00"
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_notes(self):
            response = self.app.get('/personalised-notes')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['title'], "Test Personalised Note 1")
            self.assertEqual(data[1]['title'], "Test Personalised Note 2")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/personalised-notes/{note_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_specific_note()```
Tests retrieving a specific personalized note
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/personalised-notes/1
        - Path parameter: note_id=1 (from self.note_id in setup)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Details of the requested note
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "title": "Test Personalised Note 1",
            "content": "Test personalised note content 1",
            "created_at": "2023-12-04T09:15:00"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_specific_note(self):
            response = self.app.get(f'/personalised-notes/{self.note_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['title'], "Test Personalised Note 1")
            self.assertEqual(data['content'], "Test personalised note content 1")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/personalised-notes```
- **Method:** POST

##### Test Cases:
1. ```test_post_note()```
Tests creating a new personalized note
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/personalised-notes
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "title": "New Personalised Note",
            "content": "New personalised note content"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Response containing the new note ID
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 3,
            "message": "Note created successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_post_note(self):
            note_data = {
                "title": "New Personalised Note",
                "content": "New personalised note content"
            }
            
            response = self.app.post(
                '/personalised-notes',
                data=json.dumps(note_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('id', data)
            
            with app.app_context():
                note = PersonalisedNote.query.filter_by(title="New Personalised Note").first()
                self.assertIsNotNone(note)
                self.assertEqual(note.content, "New personalised note content")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/personalised-notes/{note_id}```
- **Method:** PUT

##### Test Cases:
1. ```test_put_note()```
Tests updating an existing personalized note
    - Passed Inputs:
        - PUT request to http://127.0.0.1:5000/personalised-notes/1
        - Path parameter: note_id=1 (from self.note_id in setup)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "title": "Updated Personalised Note",
            "content": "Updated personalised note content"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Note updated successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_put_note(self):
            update_data = {
                "title": "Updated Personalised Note",
                "content": "Updated personalised note content"
            }
            response = self.app.put(
                f'/personalised-notes/{self.note_id}',
                data=json.dumps(update_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            
            with app.app_context():
                note = PersonalisedNote.query.get(self.note_id)
                self.assertEqual(note.title, "Updated Personalised Note")
                self.assertEqual(note.content, "Updated personalised note content")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/personalised-notes/{note_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_note()```
Tests deleting a personalized note
    - Passed Inputs:
        - DELETE request to http://127.0.0.1:5000/personalised-notes/1
        - Path parameter: note_id=1 (from self.note_id in setup)
        - No request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Note no longer exists in database
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Note deleted successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_delete_note(self):
            response = self.app.delete(f'/personalised-notes/{self.note_id}')
            self.assertEqual(response.status_code, 200)
            
            with app.app_context():
                note = PersonalisedNote.query.get(self.note_id)
                self.assertIsNone(note)
        ```

# Programming Assignment Evaluation API Tests
**Description:** These APIs handle programming assignments functionality, allowing retrieval of programming assignments and test cases.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/programming_assignmnets```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_assignments()```
Tests retrieving all programming assignments
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/programming_assignmnets
        - No parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of programming assignments
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "question": "Create a function to add two numbers",
              "description": "Write a Python function that takes two numbers as input and returns their sum.",
              "test_cases": [
                {"input": "1,2", "expected_output": "3"},
                {"input": "5,7", "expected_output": "12"}
              ],
              "difficulty": "easy",
              "course_id": 1
            },
            {
              "id": 2,
              "question": "Create a function to reverse a string",
              "description": "Write a Python function that takes a string as input and returns it reversed.",
              "test_cases": [
                {"input": "hello", "expected_output": "olleh"},
                {"input": "python", "expected_output": "nohtyp"}
              ],
              "difficulty": "easy",
              "course_id": 1
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_assignments(self):
            response = self.app.get('/programming_assignmnets')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['question'], "Create a function to add two numbers")
            self.assertEqual(data[1]['question'], "Create a function to reverse a string")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/programming_assignmnet/{assignment_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_assignment()```
Tests retrieving a specific programming assignment
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/programming_assignmnet/1
        - Path parameter: assignment_id=1 (from self.prog_assignment_id in setup)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Details of the requested programming assignment
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "question": "Create a function to add two numbers",
            "description": "Write a Python function that takes two numbers as input and returns their sum.",
            "test_cases": [
              {"input": "1,2", "expected_output": "3"},
              {"input": "5,7", "expected_output": "12"}
            ],
            "difficulty": "easy",
            "course_id": 1,
            "starter_code": "def add(a, b):\n    # Your code here\n    pass"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_assignment(self):
            response = self.app.get(f'/programming_assignmnet/{self.prog_assignment_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['question'], "Create a function to add two numbers")
        ```

### Endpoint: 
- **URL:** `http://127.0.0.1:5000/programming_assignmnet/{assignment_id}`
- **Method:** POST

##### Test Cases:
1. `test_post_assignment_evaluation()`
Tests submitting a solution for a programming assignment.

- **Passed Inputs:**
    - POST request to `/programming_assignmnet/{assignment_id}`
    - Path parameter: `assignment_id` (from `self.prog_assignment_id` in setup)
    - Content-Type: `application/json`
    - Request Body:
    ```json
    {
        "code": "def solution(a, b): return a + b"
    }
    ```

- **Expected Output:**
    - `HTTP-Status Code: 200`
    - Evaluation results with pass/fail status for each test case.

- **Actual Output:**
    - `HTTP-Status Code: 200`
    - ```json
      [true, true]
      ```

- **Result:** 
    - `Passed`

- **Test Code:**
    ```python
    def test_post_assignment_evaluation(self):
        # Test with correct solution code
        correct_solution = """
        def solution(a, b):
            return a + b
        """
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": correct_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(results))  # All test cases should pass
        
        # Test with incorrect solution code
        incorrect_solution = """
        def solution(a, b):
            return a - b
        """
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": incorrect_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        self.assertFalse(all(results))  # Some test cases should fail
        
        # Test with code that raises an exception
        error_solution = """
        def solution(a, b):
            return a / 0
        """
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={"code": error_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)
        self.assertEqual(len(results), 2)
        # Results should contain error messages
        self.assertTrue(isinstance(results[0], str))
        
        # Test with missing code
        response = self.app.post(
            f'/programming_assignmnet/{self.prog_assignment_id}',
            json={},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with non-existent assignment ID
        response = self.app.post(
            '/programming_assignmnet/9999',
            json={"code": correct_solution},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
    ```

# Questions API Tests
**Description:** These APIs manage question functionality, allowing access to questions in the system.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/questions```
- **Method:** GET

##### Test Cases:
1. ```test_get_questions()```
Tests retrieving all questions from the system
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/questions
        - No parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of questions with text, options, and other properties
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "text": "What is 1+1?",
              "options": ["1", "2", "3", "4"],
              "correct_option": 1,
              "explanation": "Basic addition",
              "assignment_id": 1
            },
            {
              "id": 2,
              "text": "What is the capital of France?",
              "options": ["London", "Berlin", "Paris", "Madrid"],
              "correct_option": 2,
              "explanation": "Paris is the capital of France",
              "assignment_id": 1
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_questions(self):
            # Update the endpoint to match the API implementation
            response = self.app.get('/questions')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(len(data) >= 2)
            # Since the order isn't guaranteed, we'll check if our questions exist in the response
            question_texts = [q['text'] for q in data]
            self.assertIn("What is 1+1?", question_texts)
            self.assertIn("What is the capital of France?", question_texts)
        ```

# Recommendations API Tests
**Description:** These APIs manage recommendations functionality, allowing users to create, retrieve, update, and delete recommendations.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/recommendations```
- **Method:** GET

##### Test Cases:
1. ```test_get_all_recommendations()```
Tests retrieving all recommendations
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/recommendations
        - No parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - List of all recommendations
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          [
            {
              "id": 1,
              "content": "Try the advanced algorithms course next"
            },
            {
              "id": 2,
              "content": "Complete the machine learning assignments"
            }
          ]
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_all_recommendations(self):
            response = self.app.get('/recommendations')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['content'], "Try the advanced algorithms course next")
            self.assertEqual(data[1]['content'], "Complete the machine learning assignments")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/recommendations/{recommendation_id}```
- **Method:** GET

##### Test Cases:
1. ```test_get_specific_recommendation()```
Tests retrieving a specific recommendation
    - Passed Inputs:
        - GET request to http://127.0.0.1:5000/recommendations/1
        - Path parameter: recommendation_id=1 (from self.recommendation_id in setup)
        - No query parameters or request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Details of the requested recommendation
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 1,
            "content": "Try the advanced algorithms course next"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_get_specific_recommendation(self):
            response = self.app.get(f'/recommendations/{self.recommendation_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['content'], "Try the advanced algorithms course next")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/recommendations```
- **Method:** POST

##### Test Cases:
1. ```test_post_recommendation()```
Tests creating a new recommendation
    - Passed Inputs:
        - POST request to http://127.0.0.1:5000/recommendations
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "content": "Review the database concepts before the exam"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Response containing the new recommendation ID
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "id": 3,
            "message": "Recommendation created successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_post_recommendation(self):
            rec_data = {
                "content": "Review the database concepts before the exam"
            }
            response = self.app.post(
                '/recommendations',
                data=json.dumps(rec_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('id', data)
            
            with app.app_context():
                rec = Recommendation.query.get(data['id'])
                self.assertIsNotNone(rec)
                self.assertEqual(rec.content, "Review the database concepts before the exam")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/recommendations/{recommendation_id}```
- **Method:** PUT

##### Test Cases:
1. ```test_put_recommendation()```
Tests updating an existing recommendation
    - Passed Inputs:
        - PUT request to http://127.0.0.1:5000/recommendations/1
        - Path parameter: recommendation_id=1 (from self.recommendation_id in setup)
        - Content-Type: application/json
        - Request Body:
        ```json
        {
            "content": "Updated recommendation content"
        }
        ```
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Recommendation updated successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_put_recommendation(self):
            update_data = {
                "content": "Updated recommendation content"
            }
            response = self.app.put(
                f'/recommendations/{self.recommendation_id}',
                data=json.dumps(update_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            
            with app.app_context():
                rec = Recommendation.query.get(self.recommendation_id)
                self.assertEqual(rec.content, "Updated recommendation content")
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/recommendations/{recommendation_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_recommendation()```
Tests deleting a recommendation
    - Passed Inputs:
        - DELETE request to http://127.0.0.1:5000/recommendations/1
        - Path parameter: recommendation_id=1 (from self.recommendation_id in setup)
        - No request body
    - Expected Output:
        - ```HTTP-Status Code: 200```
        - Recommendation no longer exists in database
    - Actual Output:
        - ```HTTP-Status Code: 200```
        - ```json
          {
            "message": "Recommendation deleted successfully"
          }
          ```
    - Result: 
        - ```Passed```
    - Test Code:
        ```python
        def test_delete_recommendation(self):
            response = self.app.delete(f'/recommendations/{self.recommendation_id}')
            self.assertEqual(response.status_code, 200)
            
            with app.app_context():
                rec = Recommendation.query.get(self.recommendation_id)
                self.assertIsNone(rec)
        ```

