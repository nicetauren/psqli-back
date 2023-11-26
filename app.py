from flask import Flask
from flask_restx import Resource, Api
from auth import Auth
from challenge import Challenge

app = Flask(__name__)
api = Api(app)

api.add_namespace(Auth, '/auth')
api.add_namespace(Challenge, '/challenge')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)