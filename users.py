import jwt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

Users= Namespace(
    name='Users',
    description='유저 관리를 위한 API',
)

users_fields = Users.model('Users',{
    'nickname': fields.String(),
    'name': fields.Integer(),
})

@Users.route('/all')
class AllUsers(Resource):
    @Users.doc(responses={200: 'Success'})
    @Users.doc(responses={500: 'All Users Failed'})
    def get(self):
        sql = "SELECT id, nickname, name FROM users;"
        conn = DB()

        all_users = conn.select_all(sql)
        for i, user in enumerate(all_users):
            user = list(user)
            user.append("user")
            all_users[i] = user

        sql = "SELECT id, nickname, name FROM maker;"

        all_maker = conn.select_all(sql)
        for i, maker in enumerate(all_maker):
            maker = list(maker)
            maker.append("maker")
            all_maker[i] = maker

        all_um = all_users+all_maker

        conn.cursor.close()
        conn.conn.close()
        return all_um, 200

    def delete(self):
        conn = DB()

        sql = "DELETE FROM solves;"
        conn.delete(sql)
        sql = "DELETE FROM challenges;"
        conn.delete(sql)
        sql = "DELETE FROM users;"
        conn.delete(sql)
        sql = "DELETE FROM maker;"
        conn = DB()
        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()

        return 200
    
@Users.route('/maker/<int:user_id>')
class GetMaker(Resource):
    @Users.doc(response={200: 'Success'})
    @Users.doc(response={500: 'Get Maker Failed'})
    def get(self, user_id):
        conn = DB()
        sql = "SELECT DISTINCT name, nickname, challenges.id, title, challenges.score FROM maker JOIN challenges ON maker.id=challenges.mid WHERE maker.id=%d;"%user_id

        maker = conn.select_all(sql)
        print(maker)
        if len(maker) == 0:
            sql = "SELECT name, nickname FROM maker WHERE id=%d"%user_id
            maker = conn.select_all(sql)
            print(maker)
            
        conn.cursor.close()
        conn.conn.close()

        return maker, 200

@Users.route('/admin/<int:user_id>')
class GetAdmin(Resource):
    @Users.doc(response={200: 'Success'})
    @Users.doc(response={500: 'Get Admin Failed'})
    def get(self, user_id):
        conn = DB()
        sql = "SELECT DISTINCT name, nickname, posts.id, title FROM admin JOIN posts ON admin.id=posts.aid WHERE admin.id=%d;"%user_id

        admin = conn.select_all(sql)
        print(admin)
        if len(admin) == 0:
            sql = "SELECT name, nickname FROM admin WHERE id=%d;"%user_id
            admin = conn.select_all(sql)
            print(admin)
        
        conn.cursor.close()
        conn.conn.close()
        
        return admin, 200

@Users.route('/<int:user_id>')
class DeleteUser(Resource):
    @Users.doc(responses={200: 'Success'})
    @Users.doc(responses={500: 'Delete User Failed'})
    def delete(self, user_id):
        
        conn = DB()
        sql = "DELETE FROM solves WHERE uid=%d"%user_id;
        conn.delete(sql)

        sql = "DELETE FROM users WHERE id=%d"%user_id;

        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()

        return 200

