from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

Challenge = Namespace(
    name='Challenge',
    description='문제 출제, 수정, 삭제 등을 위한 API',
)

challenge_fields = Challenge.model('Challenge',{
    'title': fields.String(),
    'subscriptioin': fields.String(),
    'score': fields.Integer(),
    'answer': fields.String(),
})

@Challenge.route('/add')
class AddChallenge(Resource):
    @Challenge.expect(challenge_fields)
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Add Failed'})
    def post(self):
        title = request.json['title']
        subscription = request.json['subscription']
        score = request.json['score']
        answer = request.json['answer']

        header = request.headers.get('Authorization')
        data = jwt.decode(header, "secret", algorithms="HS256")
        mid = data['user_id']

        sql = "INSERT INTO challenges(title, subscription, score, answer, mid) VALUES (%s, %s, %d, %s, %d)"%(title, subscription, score, answer, mid)
        conn = DB()

        conn.insert(sql)
        return 200

@Challenge.route('/modify')
class ModifyChallenge(Resource):
    @Challenge.expect(challenge_fields)
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Modify Failed'})
    def post(self):
        title = request.json['title']
        subscription = request.json['subscription']
        score = request.json['score']
        answer = request.json['answer']
        mid = request.json['mid']

        sql = "UPDATE challenges SET title = '%s', subscription = '%s', score = '%d', answer = '%s', mid = '%d' WHERE title = "
        conn = DB()


@Challenge.route('/get')
class GetAllChallenge(Resource):
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Get All Challenges Failed'})
    def get(self):
        sql = "SELECT id, title, score FROM challenges"
        conn = DB()

        challenges = conn.select_all(sql)
        return challenges, 200

@Challenge.route('/get/<int:chall_num>')
class GetChallenge(Resource):
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Get Challenge Failed'})
    def get(self, chall_num):
        sql = "SELECT * FROM challenges WHERE id = %d"%chall_num
        conn = DB()

        challenge = conn.select_one(sql)
        return challenge, 200

@Challenge.route('/delete/<int:chall_num>')
class DeleteChallenge(Resource):
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Delete Challenge Failed'})
    def get(self, chall_num):
        sql = "DELETE FROM challenges WHERE id = %d"%chall_num
        conn = DB()

        conn.delete(sql)
        return 200

@Challenge.route('/delete')
class DeleteAllChallenge(Resource):
    @Challenge.doc(responses={200: 'Success'})
    @Challenge.doc(responses={500: 'Delete All Challenges Failed'})
    def get(self):
        sql = "DELETE FROM challenges"
        conn = DB()

        conn.delete_many(sql)

        return 200