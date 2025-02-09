import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return None
