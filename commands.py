from database_manager import databaseManager
import sys
import datetime
import requests
from abc import ABC, abstractmethod

""" Commands module for the Business Logic Layer of the CLI Bookmark APP"""
db = databaseManager("bookmarks.bd")

class Command(ABC):
    @abstractmethod
    def execute(self,data:dict):
        pass

class CreateBookmarksTableCommand(Command):
    '''
    Currently all bookmarks have to columns of 'id', 'title', 'url', 'notes', and 'date_added'.
        dictionary of data is 'column_name' : 'type + optional constraints/conditions'
    '''
    def execute(self, data = None):
        db.create_table("bookmarks",
                        {
                        'id' : "integer primary key autoincrement",
                        'title' : "text not null",
                        'url' : "text not null",
                        'notes' : 'text',
                        'date_added' : "text not null",
                        })


class AddBookmarkCommand(Command):
    def execute(self, data:dict, timestamp = None):
        # data must be a dict of 'column_name' : 'Correct value type' see CreateBookmarksTableCommand for details
        data['date_added'] = timestamp or datetime.datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return "Bookmard added!"


class ShowBookmarksCommand(Command):
    #Note: This class is missing the ability to set a WHERE condition and select specific columns
    def __init__(self, order_by:str = "date_added"):
        self.order_by = order_by

    def execute(self, data = None):
        return db.select('bookmarks', order_by= self.order_by).fetchall()

class DeleteBookmardCommand(Command):
    #Note sure I like this being an int and add being a dict
    def execute(self, data:dict):
        db.delete('bookmarks', data)
        return f'Successful deletion of record with ID: {data["id"]}'

class QuitCommand(Command):
    def execute(self, data = None):
        sys.exit()


class ImportGitHubStarsCommand(Command):
    def _extract_bookmark_info(self, repo:dict) -> dict:
        return {'title': repo['name'],
                'url': repo['html_url'],
                'notes': repo['description']}

    def execute(self, data:dict) -> str:
        bookmarks_imported = 0
        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'

        while next_page_of_results:
            stars_response = requests.get(next_page_of_results, headers = {'Accept': 'application/vnd.github.v3.star+json'})
            next_page_of_results = stars_response.links.get('next', {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info['repo']
                if data['preserve_timestamps']:
                    timestamp = datetime.datetime.strptime(repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(repo, timestamp=timestamp)

        return f'Imported {bookmarks_imported} bookmarks from starred repos!'