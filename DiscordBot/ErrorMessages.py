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


ERROR_MESSAGES = {
    # INFO
    'info': '`%s%s` takes no arguments.',
    'help': '`%s%s` takes none or just one command name as argument.',
    # TODO POLL
    'poll': '`%s%s` takes a poll name as first argument and at least 2 options (use `help poll` for more information).',
    'poll_already_exists': 'A poll is already ongoing with the same name having the following options: `%s`.',
    'poll_non_unique_options': 'Poll options must be different from each other.',
    'vote': '`%spoll %s` takes 1 existing poll name and 1 existing option as arguments.',
    'vote_no_poll': 'No poll named `%s` exists on this channel.',
    'vote_no_option': 'No option `%s` exists on poll `%s`.',
    'status': '`%spoll %s` takes either no arguments or 1 existing poll name as argument.'
}
