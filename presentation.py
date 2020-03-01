import commands
import database_manager
import collections
import os

''' Presentation Layer for the CLI Bookmark App'''

class Option:
    def __init__(self, name:str, command, prep_call = None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


def print_options(options:dict):
    for key, option_text in options.items():
        print(f'({key}) {option_text}')
    print()


def get_user_choice(user_options:dict):
    user_input = input("Choose an option: ").upper()
    while (user_input not in user_options.keys()):
        print("\nInvalid Option, try again\n")
        print_options(user_options)
        user_input = input("Choose an option: ").upper()
    return user_options[user_input]


def get_data(request:str, required:bool):
    user_input = input(f'{request}')
    while (required and not user_input):
        print("\nInvalid Input: ")
        user_input = input(f'{request}')
    return user_input

def get_add_data() -> dict:
    title = get_data("Enter Bookmark Title: ", True)
    url = get_data("Enter Bookmark URL: ", True)
    notes = get_data("Enter Bookmark Notes: ", False)
    return {'title': title, 'url': url, 'notes': notes}

def get_delete_data() -> dict:
    id = get_data("Enter ID to delete: ", True)
    while (not isinstance(id,int)):
        id = get_data("Enter ID to delete: ", True)
    return {'id': int(id)}

def get_github_import_options():
    return {'github_username' : get_data('GitHub username: ', required=True),
            'preserve_timestamps': get_data('Preserve timestamps [Y/N]: ', required=False) in {'Y', 'y', None}}


def clear_screen():
    print()
    print()
    input("Enter any key to return to the Menu: ")
    print()
    print()


def application_loop():
    user_options = {'A': Option("Add a bookmark", commands.AddBookmarkCommand(), prep_call=get_add_data),
                    'B': Option("List bookmarks by Date", commands.ShowBookmarksCommand()),
                    'T': Option("List bookmarks by Title", commands.ShowBookmarksCommand(order_by="title")),
                    'D': Option("Delete a bookmark", commands.DeleteBookmardCommand(), prep_call=get_delete_data),
                    'G': Option("Import GitHub stars", commands.ImportGitHubStarsCommand(), prep_call=get_github_import_options),
                    'Q': Option("Quit", commands.QuitCommand())
                    }

    print_options(user_options)
    user_option = get_user_choice(user_options)
    user_option.choose()
    clear_screen()



if __name__ == '__main__':
    print('Welcome to BookMark App!')
    commands.CreateBookmarksTableCommand().execute()

    while True:
        application_loop()

