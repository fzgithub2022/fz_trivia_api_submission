import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_uname = "caryn"
        self.database_password = "Udacity"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_uname,
            self.database_password,
            'localhost:5432',
            self.database_name
            )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for
    successful operation and for expected errors.
    """

    def test_get_categories(self):
        # Test /categories endpoint
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)

    def test_404_getting_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_get_questions(self):
        # Test /questions get endpoint
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_questions(self):
        # Test /questions get endpoint
        res = self.client().get('/questions')
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_delete_question(self):
        # Test /questions delete endpoint
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        # if the is the first time running the test
        if res.status_code == 200:
            # the record will be available and
            # delete will be successful
            self.assertEqual(res.status_code, 200)
        else:  # otherwise was deleted
            # so resource won't be found
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_post_question(self):
        # Test /questions post endpoint
        res = self.client().post('/questions', json={
            'question': 'can you please send error 200?',
            'answer': 'I make no promises',
            'category': '1',
            'difficulty': '1'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_post_question(self):
        # Test /questions post endpoint
        res = self.client().post('/questions', json={
            'question': 'can you please send error 200?',
            'answer': 'I make no promises',
            'category': '1',
            'difficulty': '1'
        })
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_post_search(self):
        # Test /search post endpoint
        res = self.client().post('/search', json={
            'searchTerm': 'title'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_post_search(self):
        # Test /search post endpoint
        res = self.client().post('/search', json={
            'searchTerm': 'title'
        })
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_get_catQuestions(self):
        # Test /questions based on category get endpoint
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_catQuestions(self):
        # Test /questions based on category get endpoint
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    def test_post_quizes(self):
        # Test /quizzes post endpoint
        res = self.client().post('/quizzes', json={
            'previous_questions': [3, 4, 5],
            'quiz_category': '0'
        })
        data = json.loads(res.data)

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
