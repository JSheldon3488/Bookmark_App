import commands
import database_manager

''' Presentation Layer for the CLI Bookmark App'''

if __name__ == '__main__':
    print('Welcome to Bark!')
    commands.CreateBookmarksTableCommand().execute()