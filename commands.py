import database_manager
import datetime

""" Commands module for the Business Logic Layer of the CLI Bookmark APP"""
# Note: Might make just a commands class with a bunch of methods like createbookmarkstable and addbookmark


db = database_manager("bookmarks.bd")

#Also would like to be able to pass in a table name to have multiple tables
class CreateBookmarksTableCommand:
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
    def execute(self, data):
        data['date_added'] = datetime.datetime.utcnow().isoformat()
        db.add('bookmarks', data)