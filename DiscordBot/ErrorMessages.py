#!python3
# coding: utf-8


"""
Error messages for commands.
Usually for errors:
 - commands.TooManyArguments
 - commands.MissingRequiredArgument
 - commands.BadArgument
 - commands.UserInputError
"""


from . import Converters


ERROR_MESSAGES = {
    # GENERAL
    'ping': '`%s%s` takes no arguments.',
    'hi': '`%s%s` takes no arguments.',
    'dice': '`%s%s` takes no arguments or one of the following: ' + ', '.join(Converters.DICES) + '.',
    'random': '`%s%s` takes no arguments or one of the predefined ones (use `help random` for more information).',
    'between': '`%srandom %s` takes 2 integers as arguments.',
    'from': '`%srandom %s` takes at least 1 argument.',
    # MATH
    'sum': '`%s%s` takes at least 1 number.',
    'subtract': '`%s%s` takes at least 1 number.',
    'divide': '`%s%s` takes at least 1 number.',
    'zero_division_error': '`%s%s` can\'t divide by zero.',
    'multiply': '`%s%s` takes at least 1 number.',
    # FUNNY
    '8ball': '`%s%s` needs a phrase on which to apply its fortune-telling powers.',
    'joke': '`%s%s` takes no arguments.',
    # GIFS
    'rickroll': '`%s%s` takes no arguments.',
    'ohgodno': '`%s%s` takes no arguments.',
    'rekt': '`%s%s` takes no arguments.',
    # ASCIIEMOJIS
    'tableflip': '`%s%s` takes no arguments.',
    'tableunflip': '`%s%s` takes no arguments.',
    'shrug': '`%s%s` takes no arguments.',
    # XKCD
    'xkcd': '`%s%s` takes no arguments or one of the predefined ones (use `help xkcd` for more information).',
    'latest': '`%sxkcd %s` takes no arguments.',
    'id': '`%sxkcd %s` takes exactly 1 positive number.',
    # INFO
    'info': '`%s%s` takes no arguments.',
    # TODO HELP command
    # TODO POLL
    'poll': '`%s%s` takes a poll name as first argument and at least 2 options (use `help poll` for more information).',
    'poll_already_exists': 'A poll is already ongoing with the same name having the following options: `%s`.',
    'poll_non_unique_options': 'Poll options must be different from each other.',
    'vote': '`%spoll %s` takes 1 existing poll name and 1 existing option as arguments.',
    'vote_no_poll': 'No poll named `%s` exists on this channel.',
    'vote_no_option': 'No option `%s` exists on poll `%s`.',
    'status': '`%spoll %s` takes either no arguments or 1 existing poll name as argument.'
}
