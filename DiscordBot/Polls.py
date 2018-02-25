#!python3
# coding: utf-8


"""
Poll handler.
"""


from .ErrorMessages import ERROR_MESSAGES


class Polls:
    def __init__(self):
        self._polls = {}  # {channel_id: {poll_name: {option: set(user_name)}}}
        self._poll_creator = {}  # {channel_id: {poll_name: author.id}}

    def new_poll(self, context, poll_name, *options):
        """
        Creates a new poll.

        :param context: Context
            bot context
        :param poll_name: str
            name of new poll
        :param options: str
            options of the new poll
        :return: (bool, str)
            False if error message was returned, True if poll was created successfully; text to be sent by the bot
        """
        channel = context.message.channel.id
        if channel not in self._polls:
            self._polls[channel] = {}
        if poll_name in self._polls[channel]:  # Polls must have unique names
            return (False,
                    ERROR_MESSAGES['poll_already_exists'] + '`' + '`, `'.join(self._polls[channel][poll_name]) + '`')
        elif len(options) != len(set(options)):  # Options must be different from each other
            return False, ERROR_MESSAGES['poll_non_unique_options']
        else:
            self._polls[channel][poll_name] = {}  # TODO id for poll (for easy voting and deleting)
            for option in options:  # Set all poll options at zero votes
                self._polls[channel][poll_name][option] = set()  # TODO id for each option (for easy voting)

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            if channel not in self._poll_creator:
                self._poll_creator[channel] = {}
            self._poll_creator[channel][poll_name] = context.message.author.id

            return (True, author_name + ' created poll `' + poll_name + '` with ' +
                    str(len(options)) + ' options: `' + '`, `'.join(options) + '`' +
                    '\nFor the next 10 minutes only ' + author_name + ' can end the poll. ' +
                    'End poll with the command `poll end <poll_name>` to end poll')  # TODO more interesting text

    def allow_user_delete_poll(self, channel_id, poll_name):
        """
        Allow every user to delete a poll.

        :param channel_id: str
            channel id
        :param poll_name:
            name of the poll
        """
        del self._poll_creator[channel_id][poll_name]

    # TODO vote
    # TODO status
    # TODO end
