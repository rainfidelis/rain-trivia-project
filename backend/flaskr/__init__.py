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
        categories = {category.id:category.type for category in all_categories}
        return {
            "success": True,
            "categories": categories
        }

    @app.route("/questions")
    def get_questions():

        categories = Category.query.all()
        all_categories = {category.id:category.type for category in categories}

        all_questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginator(request, all_questions)

        if len(paginated_questions) == 0:
            abort(404)

        return {
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(all_questions),
            "current_category": None,
            "categories": all_categories
        }

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        
        question = Question.query.get(id)

        # if question id doensn't exist, abort operation
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

        # Collect question data. Pass none if value is left empty
        question = data.get('question', None)
        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)

        # Ensure no value is empty before proceeding to create new question
        if question and answer and category and difficulty:
            new_question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)

            new_question.insert()

            return {
                "success": True,
                "id": new_question.id
            }
        
        else:
            # Abort operation if any value is none
            abort(400)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search = request.get_json().get('searchTerm', None)

        if search:
            questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
            all_questions = paginator(request, questions)

            return {
                "success": True,
                "questions": all_questions,
                "total_questions": len(questions),
                "current_category": None
            }
        else:
            abort(400)

    @app.route('/categories/<int:cat_id>/questions')
    def get_question_by_cat(cat_id):

        # confirm category exists by attempting to retrieve it
        category = Category.query.get(cat_id)

        # abort operation if category doesn't exist
        if category is None:
            abort(404)

        # if category exists, proceed to filter questions by category
        cat_questions = Question.query.filter(
                            Question.category == cat_id).order_by(Question.id).all()
        paginated_questions = paginator(request, cat_questions)

        return {
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(cat_questions),
            "current_category": category.type
        }

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
        return (jsonify({
            "error": 404,
            "success": False,
            "message": "resource not found"
        }), 404)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
        }), 400)

    return app

