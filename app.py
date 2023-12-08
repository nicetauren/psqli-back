from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
from auth import Auth
from challenge import Challenge
from score import Score
from post import Post
from users import Users

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_namespace(Auth, '/auth')
api.add_namespace(Challenge, '/challenge')
api.add_namespace(Score, '/score')
api.add_namespace(Post, '/post')
api.add_namespace(Users, '/users')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
