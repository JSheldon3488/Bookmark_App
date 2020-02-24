"""
Database layer for storing persistent data using SQLite
"""

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
        columns_with_types = [f'{column_name} {data_type}' for column_name, data_type in columns.items()]
        self._execute(f'CREATE TABLE IF NOT EXISTS {tablename} ({", ".join(columns_with_types)});')

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

    def select(self, tablename:str, columns:str = None, criteria:dict = None, order_by:str = None):
        criteria = criteria or {}
        query = f'SELECT * FROM {tablename}'
        if criteria:
            select_criteria = ' AND '.join([f'{column} = {filter_value}' for column,filter_value in criteria.items()])
            query += f' WHERE {select_criteria}'
        if order_by:
            query += f' ORDER BY {order_by}'
        return self._execute(query)