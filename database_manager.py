# Database layer for storing persistent data using SQLite

import sqlite3

class databaseManager:
    def __init__(self, database_filepath):
        self.database = sqlite3.connect(database_filepath)

    def __del__(self):
        self.database.close()

    def _execute(self, statement, values = None):
        # with used to create database transaction (atomic)
        with self.database:
            cursor = self.database.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, tablename, columns):
        statement = "CREATE TABLE IF NOT EXITS" + tablename + "(" + ", ".join([f'{name} {type}' for name,type in columns.items()]) + ");"
        self._execute(statement)