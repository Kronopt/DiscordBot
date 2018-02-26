#!python3
# coding: utf-8


"""
Poll handler.
"""


from .ErrorMessages import ERROR_MESSAGES


class Polls:
    def __init__(self):
        """
        _polls = {
            channel_id: {
                poll_name: {
                    'users': {
                        discord.User: option
                        ...
                    }
                    'options': {
                        option: set(discord.User, ...)
                        ...
                    }
                }
                ...
            }
            ...
        }

        _poll_creator = {
            channel_id: {
                poll_name: discord.User
                ...
            }
            ...
        }
        """
        self._polls = {}
        self._poll_creator = {}

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
            return False, ERROR_MESSAGES['poll_already_exists'] % '`, `'.join(self._polls[channel][poll_name])
        elif len(options) != len(set(options)):  # Options must be different from each other
            return False, ERROR_MESSAGES['poll_non_unique_options']
        else:
            self._polls[channel][poll_name] = {'users': {}, 'options': {}}  # TODO id for poll (easy voting and deleting)
            for option in options:  # Set all poll options at zero votes
                self._polls[channel][poll_name]['options'][option] = set()  # TODO id for each option (easy voting)

            if channel not in self._poll_creator:
                self._poll_creator[channel] = {}
            self._poll_creator[channel][poll_name] = context.message.author  # store author of poll

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            return (True, author_name + ' created poll `' + poll_name + '` with ' +
                    str(len(options)) + ' options: `' + '`, `'.join(options) + '`' +
                    '\nFor the next 10 minutes only ' + author_name + ' can end the poll. ' +
                    'End poll with the command `poll end <poll_name>`')  # TODO more interesting text

    def allow_user_delete_poll(self, channel_id, poll_name):
        """
        Allow every user to delete a poll.

        :param channel_id: str
            channel id
        :param poll_name:
            name of the poll
        """
        del self._poll_creator[channel_id][poll_name]

    def vote(self, context, poll_name, poll_option):
        """
        Vote on poll_option of poll poll_name.

        :param context: Context
            bot context
        :param poll_name: str
            Name of the poll
        :param poll_option: str
            Name of the option
        :return: str
            Text to be sent by the bot
        """
        channel = context.message.channel.id
        if channel not in self._polls:  # No poll yet exists on this channel
            return ERROR_MESSAGES['vote_no_poll'] % poll_name
        elif poll_name not in self._polls[channel]:  # No poll with such name exists on this channel
            return ERROR_MESSAGES['vote_no_poll'] % poll_name
        elif poll_option not in self._polls[channel][poll_name]['options']:  # No such poll option exists
            return ERROR_MESSAGES['vote_no_option'] % (poll_option, poll_name)
        else:  # OK
            user = context.message.author
            if user in self._polls[channel][poll_name]['users']:  # Already voted once on this poll
                # remove old vote
                old_vote = self._polls[channel][poll_name]['users'][user]
                self._polls[channel][poll_name]['options'][old_vote].remove(user)

                message = 'changed vote to option `' + poll_option + '`'
            else:
                message = 'voted on option `' + poll_option + '`'

            # add new vote
            self._polls[channel][poll_name]['users'][user] = poll_option
            self._polls[channel][poll_name]['options'][poll_option].add(user)

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            return 'Poll `' + poll_name + '`: `' + author_name + '`' + message + '.'

    # TODO status
    # TODO end
