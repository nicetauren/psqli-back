import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="jaeyeol"),
    'nickname': fields.String(description='a Nickname', required=True, example="nicetauren"),
    'isAdmin': fields.Boolean(description='a role is admin', required=True, default=False),
    'isMaker': fields.Boolean(description='a role is maker', required=True, default=False),
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'loginID': fields.String(description='login ID', required=True, example="woduf"),
    'password': fields.String(description='Password', required=True, example="password")
})

user_fields_login = Auth.model('User Login', {
    'loginID': fields.String(description='login ID', required=True, example="woduf"),
    'password': fields.String(description='Password', required=True, example="passowrd"),
    'isAdmin': fields.Boolean(description='a role is admin', required=True, default=False),
    'isMaker': fields.Boolean(description='a role is maker', required=True, dafault=False)
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        nickname = request.json['nickname']
        loginid = request.json['loginID']
        isAdmin = request.json['isAdmin']
        isMaker = request.json['isMaker']

        sql = 'SELECT loginid FROM '
        if isAdmin:
            sql += 'admin'
        elif isMaker:
            sql += 'maker'
        else:
            sql += 'users'
        
        conn = DB()
        id_list = conn.select_all(sql)

        if loginid in id_list:
            return {
                "message": "Register Failed, login ID is already in use"
            }, 500
        else:
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')  # 비밀번호 저장
            if isAdmin:
                sql = "INSERT INTO admin (name, nickname, loginid, password) VALUES ('%s', '%s', '%s', '%s')"%(name, nickname, loginid, password)
            elif isMaker:
                sql = "INSERT INTO maker (name, nickname, loginid, password) VALUES ('%s', '%s', '%s', '%s')"%(name, nickname, loginid, password)
            else:
                sql = "INSERT INTO users (name, nickname, loginid, password) VALUES ('%s', '%s', '%s', '%s')"%(name, nickname, loginid, password)
            
            
            conn.insert(sql)

            if isAdmin:
                sql = "SELECT id FROM admin WHERE loginid = '%s'"%loginid
            elif isMaker:
                sql = "SELECT id FROM maker WHERE loginid = '%s'"%loginid
            else:
                sql = "SELECT id FROM users WHERE loginid = '%s'"%loginid
            
            
            user_id = conn.select_one(sql)

            conn.cursor.close()
            conn.conn.close()

            return {
                'Authorization': jwt.encode({'userID': user_id, 'name': name, 'nickname': nickname, 'isAdmin': isAdmin, 'isMaker': isMaker}, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200

@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_login)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        loginID = request.json['loginID']
        password = request.json['password']
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
        isAdmin = request.json['isAdmin']
        isMaker = request.json['isMaker']

        if isAdmin:
            sql = "SELECT * FROM admin WHERE loginid='%s' and password ='%s'"%(loginID, password)
        elif isMaker:
            sql = "SELECT * FROM maker WHERE loginid='%s' and password='%s'"%(loginID, password)
        else:
            sql = "SELECT * FROM users WHERE loginid='%s' and password ='%s'"%(loginID, password)

        conn = DB()
        result = conn.select_all(sql) #what result?? if not found user or password incorrect

        return result, 200
    '''
        if result is None:
            return {
                "message": "User Not Found"
            }, 404
        else:
            user_id = result["id"]
            return {
                'Authorization': jwt.encode({'userID': user_id, 'name': name, 'nickname': nickname, 'isAdmin': isAdmin, 'isMaker': isMaker}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200
'''
@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'Login Failed'})
    def get(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        
        if header == None:
            return {"message": "Please Login"}, 404
        data = jwt.decode(header, "secret", algorithms="HS256")
        return data, 200
