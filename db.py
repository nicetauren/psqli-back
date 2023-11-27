import psycopg2

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database = 'sample2023',
            user = 'db2023',
            password = 'db!2023',
            host = '127.0.0.1',
            port = '5432'
        )
        self.cursor = self.conn.cursor()

    def select_n(self, sql, nums):
        self.cursor.execute(sql)
        result = self.cursor.fetchmany(nums)
        return result
    
    def select_one(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def select_all(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_many(self, sql, vals):
        self.cursor.executemany(sql, vals)
        self.conn.commit()

    def update(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def update_many(self, sql, vals):
        self.cur.executemany(sql, vals)
        self.conn.commit()

    def delete(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_many(self, sql, vals):
        self.cursor.executemany(sql, vals)
        self.conn.commit()
