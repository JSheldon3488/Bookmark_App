from database_manager import databaseManager
import datetime
import sys

""" Commands module for the Business Logic Layer of the CLI Bookmark APP"""
# Note: Might make just a commands class with a bunch of methods like createbookmarkstable and addbookmark


db = databaseManager("bookmarks.bd")

#Also would like to be able to pass in a table name to have multiple tables
class CreateBookmarksTableCommand:
    '''
    Currently all bookmarks have to columns of 'id', 'title', 'url', 'notes', and 'date_added'.
        dictionary of data is 'column_name' : 'type + optional constraints/conditions'
    '''
    def execute(self):
        db.create_table("bookmarks",
                        {
                        'id' : "integer primary key autoincrement",
                        'title' : "text not null",
                        'url' : "text not null",
                        'notes' : 'text',
                        'date_added' : "text not null",
                        })


class AddBookmarkCommand:
    def execute(self, data:dict):
        # data must be a dict of 'column_name' : 'Correct value type' see CreateBookmarksTableCommand for details
        data['date_added'] = datetime.datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return "Bookmard added!"


class ShowBookmarksCommand:
    #Note: This class is missing the ability to set a WHERE condition and select specific columns
    def __init__(self, order_by:str = "date_added"):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by= self.order_by).fetchall()

class DeleteBookmardCommand:
    def execute(self, id:int):
        db.delete('bookmarks', {'id': id})
        return f'Successful deletion of record with ID: {id}'

class QuitCommand:
    def execute(self):
        sys.exit()