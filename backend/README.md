# Full Stack Trivia API Backend

## Getting Started

* Base URL : At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

* Authentication : This version of the app doesn't require any authentication.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Error Handling

Errors are returned as a JSON object in the following format:

```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
``` 

The API returns 4 error types when a request fails:

* 400 : Bad request
* 404 : Resources Not Found
* 422 : Not Processable
* 405 : Method Not Allowed

## Endpoints

### Get Available Categories

```
GET '/categories'
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
Example:
GET '/categories'

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

### Get All Questions 

```
GET '/questions'
POST ...
DELETE ...

GET '/questions'
- Fetches a list of questions objects, success value, dictionary of categories and total number of questions.
- Request Arguments: optional 'page' takes values starting from 1.
- Returns: An object with keys categories, current_category, success, questions and total_questions
Exameple:
GET '/questions?page=3'

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "March 26, 1827",
            "category": 2,
            "difficulty": 4,
            "id": 25,
            "question": "When did Beethoven die?"
        }
    ],
    "success": true,
    "total_questions": 21
}
 

```

### Delete a Question 

```
DELETE '/questions/{question_id}'
GET ...
POST ...

DELETE '/questions/{question_id}'
- Delete the question with the provided ID, and return the remaining questions and id of deleted question
- Request Arguments:  optional 'page' takes values starting from 1.
- Returns: An object with keys: deleted,  success, questions and total_questions

Example:
DELETE 'questions/12?page=2'
{
    "deleted": 12,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Philo Taylor Farnsworth",
            "category": 4,
            "difficulty": 3,
            "id": 24,
            "question": "Who is the real inventor of television?"
        },
        {
            "answer": "March 26, 1827",
            "category": 2,
            "difficulty": 4,
            "id": 25,
            "question": "When did Beethoven die?"
        }
    ],
    "success": true,
    "total_questions": 20
}
```

### Add a Question  

```
POST '/questions'
POST ...
DELETE ...

POST '/questions'
- Create a new question pased on the provided question, answer, category and difficulty.
-Request Arguments:  question, answer, category and difficulty
- Returns: An object with keys: created,  success, questions and total_questions.
Example:

POST '/questions'
with json = {
    "answer": "98%",
    "category": 1,
    "difficulty": 3,
    "question": "Humans and chimpanzees share roughly how much DNA?'?"
}
Returns

{
    "created": 54,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 21
}

```

### Search Available Questions  

```
POST '/questions'
POST ...
DELETE ...

POST '/questions'
- Fetches questions that match completely or partially a given search term.
-Request Arguments:  searchTerm
- Returns: An JSON object with matched questions, success value and number of returned questions.

Example:
POST '/questions' with json = {searchTerm: "title"}

Returns:
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

```

### Get a Quiz Question

```
POST '/quizzes'
POST ...
DELETE ...

POST '/questions'
- Returns a random questions within the given category, if provided, and that is not one of the previous questions.
- Request Arguments: take category and previous question parameters
- Returns: An JSON object with keys: question, success value and current category.

Example:
POST '/quizzes'  with json = {"previous_questions": [], "quiz_category": {"type": "Science", "id": 1}}

Returns:
{
    "current_category": "Science",
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}

```

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```