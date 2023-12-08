import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

salt = bcrypt.gensalt()

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

role_fields = Auth.model('User role', {
    'role': fields.String(description='a role', required=True, default='user')
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
            sql += 'admin;'
        elif isMaker:
            sql += 'maker;'
        else:
            sql += 'users;'
        
        conn = DB()
        id_list = conn.select_all(sql)
        id_list = [login[0] for login in id_list]
        print(id_list)

        sql = 'SELECT nickname FROM '
        if isAdmin:
            sql += 'admin;'
        elif isMaker:
            sql += 'maker;'
        else:
            sql += 'users;'

        nickname_list = conn.select_all(sql)
        nickname_list = [nickname[0] for nickname in nickname_list]
        print(nickname_list)

        if loginid in id_list:
            return {
                "message": "Register Failed, login ID is already in use"
            }, 500
        elif nickname in nickname_list:
            return {
                "message": "Register Failed, nickname is already in use"
            }, 500
        else:
            password = bcrypt.hashpw(password.encode("utf-8"), salt).decode('utf-8')  # 비밀번호 저장
            if isAdmin:
                sql = "INSERT INTO admin (name, nickname, loginid, password) VALUES ('%s', '%s', '%s', '%s');"%(name, nickname, loginid, password)
            elif isMaker:
                sql = "INSERT INTO maker (name, nickname, loginid, password) VALUES ('%s', '%s', '%s', '%s');"%(name, nickname, loginid, password)
            else:
                sql = "INSERT INTO users (name, nickname, loginid, password, score) VALUES ('%s', '%s', '%s', '%s', 0);"%(name, nickname, loginid, password)
            
            
            conn.insert(sql)

            if isAdmin:
                sql = "SELECT id FROM admin WHERE loginid = '%s';"%loginid
            elif isMaker:
                sql = "SELECT id FROM maker WHERE loginid = '%s';"%loginid
            else:
                sql = "SELECT id FROM users WHERE loginid = '%s';"%loginid
            
            
            user_id = conn.select_one(sql)

            conn.cursor.close()
            conn.conn.close()

            return {
                'Authorization': jwt.encode({'userID': user_id[0], 'name': name, 'nickname': nickname, 'isAdmin': isAdmin, 'isMaker': isMaker}, "secret", algorithm="HS256")  # str으로 반환하여 return
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
        password = bcrypt.hashpw(password.encode("utf-8"), salt).decode('utf-8')
        isAdmin = request.json['isAdmin']
        isMaker = request.json['isMaker']

        if isAdmin:
            sql = "SELECT * FROM admin WHERE loginid='%s' and password ='%s';"%(loginID, password)
        elif isMaker:
            sql = "SELECT * FROM maker WHERE loginid='%s' and password='%s';"%(loginID, password)
        else:
            sql = "SELECT * FROM users WHERE loginid='%s' and password ='%s';"%(loginID, password)

        conn = DB()
        result = conn.select_all(sql) #what result?? if not found user or password incorrect

        conn.cursor.close()
        conn.conn.close()

        if len(result) == 0:
            return {
                "message": "User Not Found"
            }, 404
        else:
            user_id = result[0][0]
            name = result[0][1]
            nickname = result[0][2]
            return {
               'Authorization': jwt.encode({'userID': user_id, 'name': name, 'nickname': nickname, 'isAdmin': isAdmin, 'isMaker': isMaker}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200

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

@Auth.route('/delete/all')
class DeleteUsers(Resource):
    @Auth.expect(role_fields)
    @Auth.doc(response={200: 'Success'})
    @Auth.doc(response={500: 'Delete Failed'})
    def get(self):
        role = request.json['role']

        if role == 'user':
            sql = "DELETE FROM users;"
        elif role == 'maker':
            sql = "DELETE FROM maker;"
        elif role == 'admin':
            sql = "DELETE FROM admin;"

        conn = DB()

        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()

        return 200

@Auth.route('/delete')
class DeleteUserById(Resource):
    @Auth.expect(user_fields)
    @Auth.doc(response={200: 'Success'})
    @Auth.doc(response={500: 'Delete Failed'})
    def get(self, user_id):
        name = request.json['name']
        nickname = request.json['nickname']
        isAdmin = request.json['isAdmin']
        isMaker = request.json['isMaker']

        conn = DB()
        if isAdmin:  
            sql = "SELECT id FROM admin WHERE name='%s' and nickname='%s';"%(name, nickname)
            user_id = conn.select_one(sql)
            sql = "DELETE FROM admin WHERE id=%d;"%user_id
        elif isMaker:
            sql = "SELECT id FROM maker WHERE name='%s' and nickname='%s';"%(name, nickname)
            user_id = conn.select_one(sql)
            sql = "DELETE FROM maker WHERE id=%d;"%user_id
        else:
            sql = "SELCET id FROM users WHERE name='%s' and nickname='%s';"%(name, nickname)
            user_id = conn.select_one(sql)
            sql = "DELETE FROM users WHERE id=%d;"%user_id

        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()

        return 200
