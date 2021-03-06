import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = config('DATABASE_TEST_URL')
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

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_page_out_of_range(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_create_question(self):
        res = self.client().post('/questions', json={
            "question": "Who is the president of America",
            "answer": "Joe Biden",
            "category": 4,
            "difficulty": 1
            })
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['id'])

    def test_create_question_missing_data(self):
        res = self.client().post('/questions', json={
            "question": "",
            "answer": "Joe Biden",
            "category": 4,
            "difficulty": 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_delete_question(self):
        res = self.client().delete('/questions/19')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 19)
        self.assertTrue(data['success'])

    def test_delete_question_no_data(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])

    def test_get_questions_by_fake_category_id(self):
        res = self.client().get('/categories/300/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_search_questions(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'what'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_search_questions_no_data(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {
                "type": "Geography",
                "id": "3"
            },
            "previous_questions": [13, 14]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_play_quiz_empty_question_list(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {
                "type": "Geography",
                "id": "3"
            },
            "previous_questions": [13, 14, 15]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
