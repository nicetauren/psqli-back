from flask import Flask
from flask_restx import Resource, Api
from auth import Auth
import psycopg2

app = Flask(__name__)
api = Api(app)

api.add_namespace(Auth, '/auth')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)