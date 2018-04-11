#!python3
# coding: utf-8


"""
Poll related commands.
Each bot command is decorated with a @command decorator.
"""


import asyncio
from discord.ext import commands
from .BaseCog import Cog
from DiscordBot.ErrorMessages import ERROR_MESSAGES


# TODO use postgres data base


class Polls(Cog):
    """Poll related commands"""

    def __init__(self, bot):
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
        super(Polls, self).__init__(bot)
        self._polls = {}
        self._poll_creator = {}

    def allow_user_delete_poll(self, channel_id, poll_name):
        """
        Allow every user to delete a poll.

        :param channel_id: str
            channel id
        :param poll_name:
            name of the poll
        """
        del self._poll_creator[channel_id][poll_name]

    # POLL
    @commands.group(name='poll', ignore_extra=False, pass_context=True, invoke_without_command=True)
    async def command_poll(self, context, poll_name: str, *options: str):
        """Creates a poll. First argument is its name, remaining arguments are options.
        A poll is confined to the channel where it was created.
        All arguments can be a single word or any number of space-separated words if enclosed within quotation marks.
        ex:
            name option1 option2
            poll_name "option 1" option2
            "Is this the poll name?" "options 1 is reeeeaaally long" option2

        Each voting option must be unique.
        A poll ends when the subcommand 'end' is passed with the poll's name as argument.
        Within 10 minutes of the poll's creation only the original author can close the poll."""
        if len(options) < 2:  # at least two poll options
            raise commands.MissingRequiredArgument
        self.log_command_call('poll')

        channel = context.message.channel.id
        if channel not in self._polls:
            self._polls[channel] = {}
        if poll_name in self._polls[channel]:  # Polls must have unique names
            is_poll_created = False
            message = ERROR_MESSAGES['poll_already_exists'] % '`, `'.join(self._polls[channel][poll_name])
        elif len(options) != len(set(options)):  # Options must be different from each other
            is_poll_created = False
            message = ERROR_MESSAGES['poll_non_unique_options']
        else:
            self._polls[channel][poll_name] = {'users': {},
                                               'options': {}}  # TODO id for poll (easy voting and deleting)
            for option in options:  # Set all poll options at zero votes
                self._polls[channel][poll_name]['options'][option] = set()  # TODO id for each option (easy voting)

            if channel not in self._poll_creator:
                self._poll_creator[channel] = {}
            self._poll_creator[channel][poll_name] = context.message.author  # store author of poll

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            is_poll_created = True
            message = (author_name + ' created poll `' + poll_name + '` with ' + str(len(options)) +
                       ' options: `' + '`, `'.join(options) + '`' +
                       '\nFor the next 10 minutes only ' + author_name + ' can end the poll. ' +
                       'End poll with the command `poll end <poll_name>`')  # TODO more interesting text

        await self.bot.say(message)
        if is_poll_created:
            await asyncio.sleep(60 * 10)  # 10 minutes timer
            self.allow_user_delete_poll(context.message.channel.id, poll_name)  # every user can now end the poll

    # POLL VOTE
    @command_poll.command(name='vote', ignore_extra=False, pass_context=True, aliases=['v', '-v', 'vt'])
    async def command_poll_vote(self, context, poll_name: str, option: str):
        """Vote on option of a certain poll named poll_name."""
        self.log_command_call('poll vote')

        channel = context.message.channel.id
        if channel not in self._polls:  # No poll yet exists on this channel
            message = ERROR_MESSAGES['vote_no_poll'] % poll_name
        elif poll_name not in self._polls[channel]:  # No poll with such name exists on this channel
            message = ERROR_MESSAGES['vote_no_poll'] % poll_name
        elif option not in self._polls[channel][poll_name]['options']:  # No such poll option exists
            message = ERROR_MESSAGES['vote_no_option'] % (option, poll_name)
        else:  # OK
            user = context.message.author
            if user in self._polls[channel][poll_name]['users']:  # Already voted once on this poll
                # remove old vote
                old_vote = self._polls[channel][poll_name]['users'][user]
                self._polls[channel][poll_name]['options'][old_vote].remove(user)

                vote_message = 'changed vote to option `%s`' % option
            else:
                vote_message = 'voted on option `%s`' % option

            # add new vote
            self._polls[channel][poll_name]['users'][user] = option
            self._polls[channel][poll_name]['options'][option].add(user)

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            message = 'Poll `%s`: `%s` %s.' % (poll_name, author_name, vote_message)

        await self.bot.say(message)

    # POLL STATUS
    @command_poll.command(name='status', ignore_extra=False, aliases=['s', '-s', 'stat'])
    async def command_poll_status(self, *poll: str):
        """Shows active polls or status of passed polls."""
        self.log_command_call('poll status')

        if len(poll) == 0:
            # TODO show all poll (names only)
            pass
        else:
            # TODO for each poll name
            #   TODO poll doesn't exist
            #   TODO show poll status (pretty)
            pass

    # POLL END
    @command_poll.command(name='end', ignore_extra=False, pass_context=True, aliases=['e', '-e'])
    async def command_poll_end(self, context, poll_name: str):
        """Ends specified poll and shows results.
        For the first 10 minutes after starting a poll only it's author is able to end it."""
        self.log_command_call('poll end')

        channel = context.message.channel.id
        if poll_name in self._poll_creator[channel]:  # poll created under 10 minutes ago
            if context.message.author.id != self._poll_creator[channel][poll_name]:  # is not original author
                # TODO ERROR: Only the poll author can end the poll during the first 10 minutes
                return
        # TODO show poll results
        del self._poll_creator[channel][poll_name]
        del self._polls[channel][poll_name]
