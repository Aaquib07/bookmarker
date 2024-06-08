import os
import uuid
from collections import OrderedDict

import commands


def format_bookmark(bookmark):
    return '\t'.join(str(field) if field else '' for field in bookmark)


class Option:
    def __init__(self, name, command, prep_call=None, success_message='{result}'):
        self.name = name  # <1>
        self.command = command  # <2>
        self.prep_call = prep_call  # <3>
        self.success_message = success_message

    def choose(self):  # <4>
        data = self.prep_call() if self.prep_call else None  # <5>
        success, result = self.command.execute(data)

        formatted_result = ''

        if isinstance(result, list):
            for bookmark in result:
                formatted_result += '\n' + format_bookmark(bookmark)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    def __str__(self):  # <7>
        return self.name


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options  # <1>


def get_option_choice(options):
    choice = input('Choose an option: ')  # <2>
    while not option_choice_is_valid(choice, options):  # <3>
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]  # <4>


def get_user_input(label, required=True):  # <1>
    value = input(f'{label}: ') or None  # <2>
    while required and not value:  # <3>
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():  # <4>
    return {
        'id': str(uuid.uuid4()),
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),  # <5>
    }


def get_bookmark_id_for_deletion():  # <6>
    return get_user_input('Enter a bookmark ID to delete')

def get_new_bookmark_info():
    bookmark_id = get_user_input('Enter a bookmark ID to edit')
    field = get_user_input('Choose a value to edit (title, URL, notes)')
    new_value = get_user_input(f'Enter the new value for {field}')
    return {
        'id': bookmark_id,
        'update': {field: new_value},
    }


def loop():  # <1>
    clear_screen()

    options = OrderedDict({
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data, success_message='Bookmark added!'),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'E': Option('Edit a bookmark', commands.EditBookmarkCommand(), prep_call=get_new_bookmark_info, success_message='Bookmark updated!'),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion, success_message='Bookmark deleted!'),
        'Q': Option('Quit', commands.QuitCommand()),
    })
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    _ = input('Press ENTER to return to menu')  # <2>


if __name__ == '__main__':
    while True:  # <3>
        loop()
