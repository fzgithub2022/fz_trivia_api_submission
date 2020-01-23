import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import json
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = {}  # create dictionary
        results = Category.query.all()  # query objects from database
        # look through objects and place them as "key"="values" in dictionalry
        for result in results:
            categories[result.id] = result.type
        # return categories
        return jsonify({
            'categories': categories
        })
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        # pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        # get questions from db
        questions = Question.query.all()
        # format questions according to class method
        formatted_questions = [question.format() for question in questions]
        # categories from database
        categories = Category.query.all()
        current_category = 2
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': int(len(formatted_questions)),
            'categories': len(categories),
            'current_category': current_category
        })
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the
    question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        to_delete = Question.query.get(q_id)
        to_delete.delete()
        return jsonify({'succes': True})
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        category = int(body.get('category'))
        difficulty = body.get('difficulty')
        try:  # try to create question and insert
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
                )
            Question.insert(new_question)
        except:  # if not able to send status
            return jsonify({
                'status': 'question post failed!'
            })
        return jsonify({
            'status': 'Successfully posted to new question'
        })
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        searchTerm = body.get('searchTerm')
        results = Question.query.filter(Question.question.match(searchTerm))
        questions = [result.format() for result in results]
        total_questions = int(len(questions))
        current_category = 1
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'current_category': current_category
        })
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:c_id>/questions')
    def q_bycategory(c_id):
        results = Question.query.filter(Question.category == c_id)
        questions = [result.format() for result in results]
        total_questions = int(len(questions))
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'current_category': c_id
        })
    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def start_quizzes():
        body = request.get_json()
        previousQuestions = body.get('previousQuestions')
        quiz_category = body.get('quiz_category')
        category_questions = Question.query.filter(
            Question.category == quiz_category
            )
        available_ids = []
        for category_question in category_questions:
            available_ids.append(category_question.id)
        if not previousQuestions:
            for previousQuestion in previousQuestions:
                available_ids.pop()
        random_number = random.choice(available_ids)
        result = Question.query.get(random_number)
        question = result.format()
        return jsonify({
            'success': True,
            'previousQuestions': previousQuestions,
            'question': question
            })
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({'message': 'Bad Request!'})

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({'message': 'resource not found!'})

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({'message': 'method NOT allowed!'})

    @app.errorhandler(422)
    def handle_422(error):
        return jsonify({'message': 'Unprocessable Entity'})

    return app
