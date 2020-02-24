import commands
import database_manager
import collections

''' Presentation Layer for the CLI Bookmark App'''

class Option:
    def __init__(self, name:str, command, prep_call = None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name

def print_options(options:dict):
    for key, option_text in options.items():
        print(f'({key}) {option_text}')
    print()

def get_user_choice():
    user_input = input("Choose an option: ").upper()
    while (user_input not in user_options.keys()):
        print("\nInvalid Option, try again\n")
        print_options(user_options)
        user_input = input("Choose an option: ").upper()
    return user_options[user_input]


if __name__ == '__main__':
    print('Welcome to BookMark App!')
    commands.CreateBookmarksTableCommand().execute()

    user_options = {'A': Option("Add a bookmark", commands.AddBookmarkCommand()),
                    'B': Option("List bookmarks by Date", commands.ShowBookmarksCommand()),
                    'T': Option("List bookmarks by Title", commands.ShowBookmarksCommand(order_by="title")),
                    'D': Option("Delete a bookmark", commands.DeleteBookmardCommand()),
                    'Q': Option("Quit", commands.QuitCommand())
                    }

    print_options(user_options)
    user_option = get_user_choice()
    user_option.choose()


