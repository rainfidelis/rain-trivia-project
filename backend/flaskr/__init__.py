"""
Initialize and manage the Flask API and its endpoints
"""
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginator(request, selection):
    """
    A function for paginating results from queries. Limits querysets to
    the maximum number specified by the Questions Per Page variable.

    :param request: the request object used to extract the page number
    :param selection: the queryset object to be sent in the response

    :return: A list with a maximum of 10 items for the response
    """

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    stop = start + QUESTIONS_PER_PAGE

    content = [obj.format() for obj in selection]
    current_page = content[start:stop]

    return current_page


def create_app(test_config=None):
    """
    The function powering the entire flask application. Creates the application
    and configures its database. Defines CORS management for the application.

    Also used for defining endpoints and how they behave.
    """
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
        categories = {category.id: category.type
                      for category in all_categories}

        return {
            "success": True,
            "categories": categories
        }

    @app.route("/questions")
    def get_questions():

        categories = Category.query.all()
        all_categories = {category.id: category.type
                          for category in categories}

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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        # if question id doensn't exist, abort operation
        if question is None:
            abort(404)

        question.delete()

        return {
            "success": True,
            "deleted": question_id
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
        # Abort operation if any value is none
        abort(400)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search = request.get_json().get('searchTerm', None)

        if search:
            questions = Question.query.filter(
                            Question.question.ilike(f'%{search}%')).all()
            all_questions = paginator(request, questions)

            return {
                "success": True,
                "questions": all_questions,
                "total_questions": len(questions),
                "current_category": None
            }
        # Reject request if search term is null
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
                            Question.category == cat_id
                            ).order_by(Question.id).all()
        paginated_questions = paginator(request, cat_questions)

        return {
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(cat_questions),
            "current_category": category.type
        }

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        # Extract category id from category dictionary
        # and cast it as an integer
        cat_id = int(quiz_category['id'])

        if cat_id == 0:
            # A category ID of 0 means no category was selected
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions
                                   if question.id not in previous_questions]
            shuffled_questions = random.sample(formatted_questions,
                                               len(formatted_questions))

            # Return the first question on the list; or none if list is empty
            if len(shuffled_questions) > 0:
                question = shuffled_questions[0]
            else:
                question = None
        else:
            # If any category is selected, filter the questions by category ID
            questions = Question.query.filter(
                            Question.category == cat_id).all()
            formatted_questions = [question.format() for question in questions
                                   if question.id not in previous_questions]
            shuffled_questions = random.sample(formatted_questions,
                                               len(formatted_questions))

            if len(shuffled_questions) > 0:
                question = shuffled_questions[0]
            else:
                question = None

        return {
            "success": True,
            "question": question,
            "current_category": quiz_category['type']
        }

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
