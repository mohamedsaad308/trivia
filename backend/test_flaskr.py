import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question
from dotenv import load_dotenv


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'Which player scored the fastest hat-trick in the Premier League?',
            'answer': 'Sadio Mane (2 minutes 56 seconds for Southampton vs Aston Villa in 2015)',
            'category': 6,
            'difficulty': 5}
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
    Write at least one test for each test for successful operation and for expected errors.
    """
    # testing for get questions

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_beyond_available_pages(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_404_delete_non_existing_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_400_if_question_was_not_well_formatted(self):
        res = self.client().post(
            '/questions',
            json={
                'question': 'some question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "bad request")

    def test_422_if_question_creation_failed(self):
        res = self.client().post('/questions/5', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_search_questions_with_result(self):
        res = self.client().post('/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)
        self.assertTrue(len(data['questions']))

    def test_search_questions_without_result(self):
        res = self.client().post('/questions',
                                 json={"searchTerm": "some dummy search"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "Science")

    def test_404_category_not_found(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_play_without_selecting_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [],
                "quiz_category": {
                    "type": "click",
                    "id": 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['question'])

    def test_play_with_selecting_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [],
                "quiz_category": {
                    "type": "Science",
                    "id": 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['question'])

    def test_get_last_question_of_a_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [
                    22,
                    21,
                    20],
                "quiz_category": {
                    "type": "Science",
                    "id": 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertEqual(data['question'], None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
