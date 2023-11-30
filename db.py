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
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchmany(nums)
            return result
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()
    
    def select_one(self, sql):
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def select_all(self, sql):
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def insert(self, sql):
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def insert_many(self, sql, vals):
        print('Executing SQL:', sql)
        try:
            self.cursor.executemany(sql, vals)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def update(self, sql):
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def update_many(self, sql, vals):
        print('Executing SQL:', sql)
        try:
            self.cursor.executemany(sql, vals)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def delete(self, sql):
        print('Executing SQL:', sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()

    def delete_many(self, sql, vals):
        print('Executing SQL:', sql)
        try:
            self.cursor.executemany(sql, vals)
            self.conn.commit()
        except Exception as e:
            print('commit failed:', e)
            self.conn.rollback()
