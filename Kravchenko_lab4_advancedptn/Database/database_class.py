import sqlite3
from .database import DB_PATH


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()

    def connect_to_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    def _execute_query(self, sql, value):
        self.connect_to_db()
        self.cursor.execute(sql, value)
        self.close_connection()

    def _execute_select_query(self, sql, values=None):
        self.connect_to_db()
        if values is not None:
            self.cursor.execute(sql, values)
        else:
            self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.close_connection()
        return rows
