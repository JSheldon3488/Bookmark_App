# Database layer for storing persistent data using SQLite

import sqlite3

class databaseManager:
    def __init__(self, database_filepath:str):
        self.database = sqlite3.connect(database_filepath)

    def __del__(self):
        self.database.close()

    def _execute(self, statement:str, values:list = None):
        # with used to create database transaction (atomic)
        with self.database:
            cursor = self.database.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, tablename:str, columns:dict):
        query = "CREATE TABLE IF NOT EXITS" + tablename + "(" + ", ".join([f'{name} {type}' for name,type in columns.items()]) + ");"
        self._execute(query)

    def add(self, tablename:str, data:dict):
        placeholders = ", ".join('?'*len(data))
        column_values = tuple(data.values())
        column_names = ", ".join(data.keys())
        query = f'''INSERT INTO {tablename}
                    ({column_names})
                    VALUES ({placeholders});'''
        self._execute(query, column_values)

    def delete(self, tablename:str, criteria:dict):
        delete_criteria = " AND ".join([colname + " = " + value for colname,value in criteria.items()])
        query = f'''DELETE FROM {tablename}
                        WHERE {delete_criteria};'''
        self._execute(query)
