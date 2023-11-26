import psycopg2

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database = 'sample2023',
            user = 'db2023',
            password = 'db!2023',
            host = '::1',
            port = '5432'
        )
        self.cursor = conn.cursor()

    def select_n(self, sql, nums):
        self.cursor.execute(sql)
        result = self.cursor.fetchmany(nums)
        self.cursor.close()
        self.conn.close()
        return result
    
    def select_one(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result

    def select_all(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return result

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insert_many(self, sql, vals):
        self.cursor.executemany(sql, vals)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def update(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def update_many(self, sql, vals):
        self.cur.executemany(sql, vals)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def delete(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def delete_many(self, sql, vals):
        self.cursor.executemany(sql, vals)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()