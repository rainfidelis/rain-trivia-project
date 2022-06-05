import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginator(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    stop = start + QUESTIONS_PER_PAGE

    content = [obj.format() for obj in selection]
    current_page = content[start:stop]
    
    return current_page


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in all_categories]
        return {
            "success": True,
            "categories": categories
        }

    @app.route("/questions")
    def get_questions():
        
        current_category = request.get_json()["currentCategory"]
        categories = Category.query.all()
        all_categories = [category.format() for category in categories]

        all_questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginator(request, all_questions)

        if len(paginated_questions) == 0:
            abort(404)

        return {
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(all_questions),
            "current_category": current_category,
            "categories": all_categories
        }

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        
        question = Question.query.get(id)

        if question is None:
            abort(404)

        question.delete()

        return {
            "success": True,
            "deleted": id
        }

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        question = data['question']
        answer = data['answer']
        category = data['category']
        difficulty = data['difficulty']

        new_question = Question(question=question,
                                answer=answer,
                                category=category,
                                difficulty=difficulty)

        new_question.insert()

        return {
            "success": True,
            "id": new_question.id
        }

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        return {
            "error": 404,
            "success": False,
            "message": "resource not found"
        }

    return app

