"""
Tests for the main application configuration and basic functionality.
Ensures that the Flask application is properly set up and routes are working.
"""

import unittest
from sqlalchemy import text
from main import app
from models import db


class MainAppTest(unittest.TestCase):
    """Test cases for the main Flask application."""
    
    def setUp(self):
        """Set up test client and create test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_app_exists(self):
        """Test that the Flask application exists."""
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        """Test that the application is in testing mode."""
        self.assertTrue(app.config['TESTING'])

    def test_database_connection(self):
        """Test that the database connection works."""
        with app.app_context():
            # Use SQLAlchemy 2.0 execution API
            result = db.session.execute(text("SELECT 1")).scalar()
            self.assertEqual(result, 1)

    def test_routes_are_registered(self):
        """Test that routes are correctly registered in the application."""
        # Get the map of all routes
        rules = list(app.url_map.iter_rules())
        rule_names = [rule.rule for rule in rules]  # Use rule.rule instead of rule.endpoint
        
        # Check that essential routes are registered
        self.assertTrue(any('/courses' in name for name in rule_names), "No courses route found")
        self.assertTrue(any('/ga/' in name for name in rule_names), "No graded assignments route found")
        self.assertTrue(any('/notes/' in name for name in rule_names), "No notes route found")

    def test_404_handling(self):
        """Test that 404 errors are handled properly."""
        response = self.app.get('/nonexistentroute')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
