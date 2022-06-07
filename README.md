# Trivia App

Looking to kill boredom while testing your knowledge in a fun environment? The trivia app project is designed to help you do just that! 

The trivia website holds a collection of trivia questions in various niches - Science, History, Geography, Sports, Entertainment, and Art. Come test your knowledge on flimsy but interesting questions. Play with friends and see who's the most knowledgeable of the bunch.

In its current state, the app lets you:
- Add new questions
- Delete existing questions
- View existing questions
- Search for questions using a keyword
- Play a scored quiz from either a specific category or all categories.

## Getting Started
This project is powered by the React JS framework on the frontend and Python/Flask on the backend. It is a decoupled project with the flask backend providing the API endpoints for the React frontend. 
To work with this project on your local device, you'll need to clone/fork the repository to your local device and install both the backend and frontend dependencies. You'll also need to already have Python3, pip, [psql](https://www.postgresql.org/download/) and [node](https://nodejs.org/en/download/) installed on your local machine.

### Backend
After pulling the repo to your local machine, open your terminal and cd (change directory) into the backend directory of the repo. You'll have to install the dependencies from `requirements.txt` using either of:
- `pip install -r requirements.txt`, or
- `pipenv install -r requirements.txt` (for pipenv users)

Once the installation is complete, you can get your server running by running the following commands on a bash terminal: 
```
- export FLASK_APP="flaskr"
- export FLASK_ENV="development"
- flask run
```
> The backend server is run on http://127.0.0.1:5000/ by default

### Frontend
With `npm` installed on your device, navigate into the frontend directory of the project repo and run the following commands to launch the react server:
```
- npm install
- npm start
```
> The frontend server runs on localhost:3000 or http://127.0.0.1:3000 


## API Reference 
The Trivia API is a RESTful, resource-oriented API which returns JSON-encoded responses and uses standard HTTP response codes. 

For detailed information on the API endpoints, methods, expected request payloads, and response payloads, see the backend documentation.

## Authors
This project was authored by myself, as part of the qualification requirements for the Udacity FullStack Developer NanoDegree, and an extension of the original [Udacity provided repository](https://github.com/udacity/cd0037-API-Development-and-Documentation-project).
