import jwt
from flask import request
from flask_restx import Resource, Api, Namespace, fields
from db import DB

Post = Namespace(
    name='Post',
    description='게시물 작성, 삭제 등을 위한 API',
)

post_fields = Post.model('Post',{
    'title': fields.String(),
    'subscriptioin': fields.String(),
})

@Post.route('/add')
class AddPost(Resource):
    @Post.expect(post_fields)
    @Post.doc(responses={200: 'Success'})
    @Post.doc(responses={500: 'Add Failed'})
    def post(self):
        title = request.json['title']
        subscription = request.json['subscription']

        header = request.headers.get('Authorization')
        data = jwt.decode(header, "secret", algorithms="HS256")
        print(data)
        aid = data['userID']

        sql = "INSERT INTO posts(title, subscription, aid) VALUES ('%s', '%s', %d);"%(title, subscription, aid)
        conn = DB()

        conn.insert(sql)

        conn.cursor.close()
        conn.conn.close()

        return 200

@Post.route('/get')
class GetAllPost(Resource):
    @Post.doc(responses={200: 'Success'})
    @Post.doc(responses={500: 'Get All Posts Failed'})
    def get(self):
        sql = "SELECT posts.id, posts.title, admin.nickname FROM posts JOIN admin ON posts.aid=admin.id;"
        conn = DB()

        posts = conn.select_all(sql)

        conn.cursor.close()
        conn.conn.close()
        return posts, 200

@Post.route('/get/<int:post_num>')
class GetPost(Resource):
    @Post.doc(responses={200: 'Success'})
    @Post.doc(responses={500: 'Get Post Failed'})
    def get(self, post_num):
        sql = "SELECT posts.id, posts.title, posts.subscription, admin.id, admin.nickname FROM posts JOIN admin ON posts.aid = admin.id WHERE posts.id = %d;"%post_num
        conn = DB()

        post = conn.select_one(sql)

        conn.cursor.close()
        conn.conn.close()
        return post, 200

@Post.route('/delete/<int:post_num>')
class DeletePost(Resource):
    @Post.doc(responses={200: 'Success'})
    @Post.doc(responses={500: 'Delete Post Failed'})
    def delete(self, post_num):
        sql = "DELETE FROM posts WHERE id = %d;"%post_num
        conn = DB()

        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()
        return 200

@Post.route('/delete')
class DeleteAllPost(Resource):
    @Post.doc(responses={200: 'Success'})
    @Post.doc(responses={500: 'Delete All Posts Failed'})
    def delete(self):
        sql = "DELETE FROM posts;"
        conn = DB()

        conn.delete(sql)

        conn.cursor.close()
        conn.conn.close()
        return 200
