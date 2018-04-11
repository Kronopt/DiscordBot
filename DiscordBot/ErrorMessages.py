#!python3
# coding: utf-8


"""
Error messages for commands.
"""


from . import Converters


ERROR_MESSAGES = {
    'ping': '`%s%s` takes no arguments.',
    'hi': '`%s%s` takes no arguments.',
    'dice': '`%s%s` takes no arguments or one of the following: ' + ', '.join(Converters.DICES) + '.',
    'random': '`%s%s` takes no arguments or one of the predefined ones (use `help random` for more information).',
    'between': '`%s%s` takes 2 integers as arguments.',
    'from': '`%s%s` takes at least 1 argument.',
    'sum': '`%s%s` takes at least 1 number.',
    'subtract': '`%s%s` takes at least 1 number.',
    'divide': '`%s%s` takes at least 1 number.',
    'zero_division_error': '`%s%s` can\'t divide by zero.',
    'multiply': '`%s%s` takes at least 1 number.',
    '8ball': '`%s%s` needs a phrase on which to apply its fortune-telling powers.',
    'poll': '`%s%s` takes a poll name as first argument and at least 2 options (use `help poll` for more information).',
    'poll_already_exists': 'A poll is already ongoing with the same name having the following options: `%s`.',
    'poll_non_unique_options': 'Poll options must be different from each other.',
    'vote': '`%s%s` takes 1 existing poll name and 1 existing option as arguments.',
    'vote_no_poll': 'No poll named `%s` exists on this channel.',
    'vote_no_option': 'No option `%s` exists on poll `%s`.',
    'status': '`%s%s` takes either no arguments or 1 existing poll name as argument.',
    'xkcd': '`%s%s` takes no arguments or one of the predefined ones (use `help xkcd` for more information).',
    'latest': '`%s%s` takes no arguments.',
    'id': '`%s%s` takes exactly 1 number.'
}
