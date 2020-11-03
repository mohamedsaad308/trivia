import os
from flask import Flask, request, abort, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys    #for troubleshooting purposes
import random #get random question
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs 
  '''
  CORS(app)        
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow #DONE
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  #helper function to return categories as a dictionary
  def categories_dict():
    categories_restul = Category.query.order_by(Category.id).all()
    categories_dict = {}
    for category in categories_restul:
      categories_dict[category.id] = category.type
    return categories_dict
    
  @app.route('/categories')
  def get_categories():
    categories = categories_dict()
    return jsonify({
      'success' : True,
      'categories' : categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

  @app.route('/questions')
  def get_paginated_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    categories = [category.type for category in Category.query.order_by(Category.id).all()]
    categories = categories_dict()
    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success' : True,
      'questions' : current_questions,
      'total_questions' : len(questions),
      'categories': categories,
      'current_category' : None
    })
    
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success' : True,
        'deleted' : question_id,
        'questions' : current_questions,
        'total_questions' : len(questions),
      })
    except:
      print(sys.exc_info())
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_new_question():
    body = request.get_json()
    if body is None:
      abort(400)
    
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('searchTerm', None)
    
    if search:
      search_term = f'%{search}%'
      result = Question.query.filter(Question.question.ilike(search_term)).order_by(Question.id).all()
      current_questions = paginate_questions(request, result)
      return jsonify({
      'success' : True,
      'questions': current_questions,
      'total_questions': len(result),
      # 'current_category' : None
      })
    if new_question is None or new_answer is None:
      abort(400)
    

    try:
      
      question = Question(question=new_question,
                          answer=new_answer,
                          category=new_category,
                          difficulty=new_difficulty)
      question.insert()
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success':True,
        'created' : question.id,
        'questions' : current_questions,
        'total_questions' : len(questions),
    })
    except:
      print(sys.exc_info())
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
# Search requests goes to ('questions/') with a search word and handled by create_new_question()
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    try:
      current_category = Category.query.filter(Category.id == category_id).one_or_none()
      if current_category is None:
        abort(404)
      current_category_questions = current_category.questions
      current_questions = paginate_questions(request, current_category_questions)
      return jsonify({
        'success': True,
        'current_category': current_category.type,
        'questions' : current_questions,
        'total_questions' : len(current_category_questions),
      })
    except:
      abort(404)
    

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
  def play():
    body = request.get_json()
    
    if body is None:
      abort(400)
      
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)
    if quiz_category['id'] == 0:
      # all_questions = Question.query.order_by(Question.id).all()
      not_asked_questions = Question.query.filter(~Question.id.in_(previous_questions)).order_by(Question.id).all()
      if len(not_asked_questions) > 0:
        next_question = random.choice(not_asked_questions)
        formatted_question = next_question.format()
        previous_questions.append(next_question)
      else:
        formatted_question = None
      return jsonify({
        'success' : True,
        'question' : formatted_question,
        'current_category': None
      })
    else:
      current_category = Category.query.filter(Category.id==quiz_category['id']).one_or_none()
      current_category_questions = current_category.questions
      not_asked_questions = [question for question in current_category_questions if question.id not in (previous_questions)]
      if len(not_asked_questions) > 0:
        next_question = random.choice(not_asked_questions)
        formatted_question = next_question.format()
        previous_questions.append(next_question)
      else:
        formatted_question = None
      return jsonify({
        'success' : True,
        'question' : formatted_question,
        'current_category': current_category.type
      })
      
      
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  return app

    