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
        sql = "SELECT id, nickname, score FROM users ORDER BY score desc;"
        conn = DB()

        all_scores = conn.select_all(sql)

        conn.cursor.close()
        conn.conn.close()

        return all_scores, 200
    
@Score.route('/<int:user_id>')
class GetUserScore(Resource):
    @Score.doc(responses={200: 'Success'})
    @Score.doc(responses={500: 'Get User Score Failed'})
    def get(self, user_id):
        sql = "SELECT DISTINCT name, nickname, users.score, challenges.id, title, challenges.score FROM solves JOIN users ON solves.uid=users.id JOIN challenges ON  solves.cid=challenges.id WHERE solves.correctness=True AND users.id=%d;"%user_id        
        conn = DB()

        user_score = conn.select_all(sql)
        print(user_score)
        if len(user_score) != 0:

            conn.cursor.close()
            conn.conn.close()
            return user_score, 200
        else:
            sql = "SELECT name, nickname, score FROM users WHERE id=%d;"%user_id
            conn = DB()
            user_score = conn.select_all(sql)
            print(user_score)
            conn.cursor.close()
            conn.conn.close()
            return user_score, 200
    
@Score.route('/check_answer')
class AnswerCheck(Resource):
    @Score.expect(challenge_fields)
    @Score.doc(responses={200: 'Success'})
    @Score.doc(responses={500: 'Answer Check Failed'})
    def post(self):
        title = request.json['title']
        answer = request.json['answer']
        mid = request.json['mid']

        header = request.headers.get('Authorization')
        data = jwt.decode(header, "secret", algorithms="HS256")
        uid = data['userID']

        sql = "SELECT id, answer, score FROM challenges WHERE title='%s' and mid='%d';"%(title, mid)
        conn = DB()

        real_answer = conn.select_one(sql)
        print(real_answer[1])

        print(real_answer[2])
        print(answer)
        score = real_answer[2]

        if answer != real_answer[1]:
            sql = "INSERT INTO solves (uid, cid, correctness) VALUES (%d, %d, %s);"%(uid, real_answer[0], False)
            conn.insert(sql)

            conn.cursor.close()
            conn.conn.close()

            return "WRONG", 200
        else:
            sql = "INSERT INTO solves (uid, cid, correctness) VALUES (%d, %d, %s);"%(uid, real_answer[0], True)
            conn.insert(sql)
            sql = "SELECT * FROM users WHERE id=%d;"%uid
            user_data = conn.select_one(sql)
            print(user_data)
            sql = "UPDATE users SET id=%d, name='%s', nickname='%s', loginid='%s', password='%s', score=%d WHERE id=%d;"%(uid, user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]+score, uid)
            conn.update(sql)

            conn.cursor.close()
            conn.conn.close()
            return "CORRECT", 200
