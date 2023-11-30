import jwt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

Score = Namespace(
    name='Score',
    description='점수 조회, 정답 체크를 위한 API',
)

challenge_fields = Score.model('Challenge',{
    'title': fields.String(),
    'score': fields.Integer(),
    'answer': fields.String(),
    'mid': fields.Integer(),
})
@Score.route('/all')
class GetAllScore(Resource):
    @Score.doc(responses={200: 'Success'})
    @Score.doc(responses={500: 'Get All Score Failed'})
    def get(self):
        sql = "SELECT id, nickname, score FROM users;"
        conn = DB()

        all_scores = conn.select_all(sql)
        return all_scores, 200
    
@Score.route('/<int:user_id>')
class GetUserScore(Resource):
    @Score.doc(responses={200: 'Success'})
    @Score.doc(responses={500: 'Get User Score Failed'})
    def get(self, user_id):
        sql = "SELECT id, nickname, score FROM users WHERE id=%d;"%user_id
        conn = DB()

        user_score = conn.select_one(sql)
        return user_score, 200
    
@Score.route('/check_answer')
class AnswerCheck(Resource):
    @Score.expect(challenge_fields)
    @Score.doc(responses={200: 'Success'})
    @Score.doc(responses={401: 'Incorrect Answer'})
    @Score.doc(responses={500: 'Answer Check Failed'})
    def post(self):
        title = request.json['title']
        score = request.json['score']
        answer = request.json['answer']
        mid = request.json['mid']

        header = request.headers.get('Authorization')
        data = jwt.decode(header, "secret", algorithms="HS256")
        uid = data['userID']

        sql = "SELECT id, answer FROM challenges WHERE title='%s' and mid='%d';"%(title, mid)
        conn = DB()

        real_answer = conn.select_one(sql)
        print(real_answer[1])

        if answer != real_answer[1]:
            sql = "INSERT INTO solves (uid, cid, correctness) VALUES (%d, %d, %s);"%(uid, real_answer[0], False)
            conn.insert(sql)
            return 401
        else:
            sql = "INSERT INTO solves (uid, cid, correctness) VALUES (%d, %d, %s);"%(uid, real_answer[0], True)
            conn.insert(sql)
            sql = "SELECT * FROM users WHERE id=%d;"%uid
            user_data = conn.select_one(sql)
            print(user_data)
            sql = "UPDATE users SET id=%d, name='%s', nickname='%s', loginid='%s', password='%s', score=%d WHERE id=%d;"%(uid, user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]+score, uid)
            conn.update(sql)


            return 200
