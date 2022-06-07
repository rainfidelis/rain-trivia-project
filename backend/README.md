# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is highly recommended that you work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight PostgreSQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is used to handle cross-origin requests from the frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation
The API interacts with the trivia database, and helps users to retrieve questions or categories, create new questions, and go through a quiz-like gameplay scenario.

### Getting started
- Base URL: The API is currently only accessible via your localhost server and can be accessed locally via http://127.0.0.1:5000/ or localhost:5000
- Authentication: No authentication or API keys are required to access the API at this time.

### Error Handling
The Trivia API uses conventional HTTP response codes for successes and failures of API requests. As a reminder: Codes `2xx` indicate success, `4xx` indicate failures (such as a bad request or a request for non-existent data), and `5xx` indicate server errors (which means something went wrong with your local server). 

Errors are parsed back to the user as JSON-encoded messages in the format below:

    {
            "success": False,
            "error": 404,
            "message": "resource not found"
    }

You can expect the following error codes when using the API:
+ `400 - Bad Request: The request wasn't accepted, often because of a missing parameter`
+ `404 - Not Found: The requested resource doesn't exist on the server`
+ `422 - Unprocessable: An error in your request is preventing the server from processing it`

### Endpoints
#### GET /categories
- General:
    - Returns a success value, and a dictionary of all categories with the category IDs as keys and the category types as values.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /questions
- General:
    - Returns a list of all question objects in the database, a success value, total number of questions, and a dictionary of all the categories.
    - Results are paginated to accept a maximum of 10 questions per page

- Sample: `curl http://127.0.0.1:5000/questions?page=2`
```
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
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
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
        }
    ],
    "success": true,
    "total_questions": 19
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question with the assciated ID from the database and persists the result
- Sample: `curl http://127.0.0.1:5000/questions/33`
```
{
    "deleted": 33,
    "success": true
}
```

#### POST /questions
- General:
    - Creates a new question object and persists it to the database
    - Accepts a json payload with the question, answer, category, and difficulty level
    - Returns the ID of the newly created object upon success
    - Returns a 400 error if any of the values are missing
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who is the president of America", "answer": "Joe Biden", "category": 4, "difficulty": 1}'`
```
{
    "success": True,
    "id": 28
}
```

#### POST /questions/search
- General:
    - Locates any question which contains the provided search string
    - Paginates the result if total questions matching the string are more than 10
    - Returns a 400 error is no search string is provided
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what"}'`
```
{
    "success": True,
    "current_category": null,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
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
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "total_questions": 8
}
```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of all questions with the associated category ID, the total number of questions, and the category ID
    - Paginates results to 10 questions per page
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`
```
{
    "current_category": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
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
        }
    ],
    "success": true,
    "total_questions": 4
}
```

#### POST /quizzes
- General:
    - Releases one question at a time in quiz-like fashion when called, as well as the category type and success value
    - Receives a json payload consisting of the ID of questions already received, as well as a dictionary of the quiz category
    - Treats the category ID of 0 as neutral and releases questions from any category
    - Returns question as None if every question in the database has been released
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type:application/json" -d '{"quiz_category": {"type": "Geography", "id": "3"}, "previous_questions": [13, 14]}'`
```
{
    "current_category": "Geography",
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
