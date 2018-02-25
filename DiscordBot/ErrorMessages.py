#!python3
# coding: utf-8


"""
Error messages for commands.
"""


from . import Converters


ERROR_MESSAGES = {
    'ping': 'takes no arguments.',
    'hi': 'takes no arguments.',
    'dice': 'takes one of the following arguments: ' + ', '.join(Converters.DICES) + '.',
    'random': 'either takes no arguments or one of the predefined ones (use `help random` for more information).',
    'between': 'takes 2 integers as arguments.',
    'from': 'takes at least 1 argument.',
    'sum': 'takes at least 1 number.',
    'subtract': 'takes at least 1 number.',
    'divide': 'takes at least 1 number.',
    'zero_division_error': 'can\'t divide by zero.',
    'multiply': 'takes at least 1 number.',
    '8ball': 'needs a phrase on which to apply its fortune-telling powers.',
    'poll': 'takes a poll name as first argument and at least 2 options (use `help poll` for more information).',
    'poll_already_exists': 'A poll is already ongoing with the same name having the following options: ',
    'poll_non_unique_options': 'Poll options must be different from each other.',
    'vote': 'takes 1 existing poll name and 1 existing option as arguments.',
    'status': 'takes either no arguments or 1 existing poll name as argument.'
}
