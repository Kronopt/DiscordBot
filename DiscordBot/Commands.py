#!python3
# coding: utf-8


"""
Commands (cogs) .py file.
Each bot command is decorated with a @command decorator.
"""


import asyncio
import functools
import logging
import operator
import random
from discord.ext import commands
from DiscordBot import Converters


logger = logging.getLogger('discord')


ERROR_MESSAGES = {
    'ping': 'takes no arguments.',
    'hi': 'takes no arguments.',
    'dice': 'takes one of the following arguments: ' + ', '.join(Converters.DICES) + '.',
    'random': 'either takes no arguments or one of the predefined ones (type `!help random`).',
    'between': 'takes 2 integers as arguments.',
    'from': 'takes at least 1 argument.',
    'sum': 'takes at least 1 number.',
    'subtract': 'takes at least 1 number.',
    'divide': 'takes at least 1 number.',
    'zero_division_error': 'can\'t divide by zero.',
    'multiply': 'takes at least 1 number.',
    '8ball': 'needs a phrase on which to apply its fortune-telling powers.',
    'poll': 'takes a poll name as first argument and at least 2 options (type `!help poll`).',
    'poll_already_exists': 'A poll is already ongoing with the same name having the following options: ',
    'vote': 'takes 1 existing poll name and 1 existing option as arguments.',
    'status': 'takes either no arguments or 1 existing poll name as argument.'
}


class Commands:
    def __init__(self, bot):
        self.bot = bot

    # def __unload(self):
    #     print('cleanup goes here')
    #
    # def __check(self, ctx):
    #     print('cog global check')
    #     return True

    _greetings = ['Hi', 'Hello', 'Hey', 'Sup', 'What\'s up', 'Greetings', 'Howdy']

    _eightball_emojis = [":white_check_mark:", ":low_brightness:", ":x:"]
    _eightball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                          "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                          "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                          "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                          "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    _polls = {}  # {channel_id: {poll_name: {option: set(user_name)}}}
    _poll_creator = {}  # {channel_id: {poll_name: author.id}}

    @staticmethod
    def log_command_call(command):
        """
        Logs calls to command as INFO

        :param command: str
            name of command
        """
        logger.info('command called: ' + command)

    # PING
    @commands.command(name='ping', ignore_extra=False)
    async def command_ping(self):
        """Answers with 'pong'.
        Simple command to test if bot is alive."""
        self.log_command_call('ping')

        await self.bot.say('pong')

    # HI
    @commands.command(name='hi', ignore_extra=False, aliases=['hello'], pass_context=True)
    async def command_hi(self, context):
        """Answers with a greeting.
        Greets user directly."""
        self.log_command_call('hi')

        if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
            author_name = context.message.author.nick
        else:
            author_name = context.message.author.name
        await self.bot.say(random.choice(self._greetings) + ', ' + author_name)

    # DICE
    @commands.command(name='dice', ignore_extra=False)
    async def command_dice(self, dice: Converters.dice):
        """Rolls one of the specified d4, d6, d8, d10, d12 and d20 dices.
        A dice can either be written as 'D#' or 'd#'."""
        self.log_command_call('dice')

        dice_number = int(dice[1:])
        dice_roll = random.randint(1, dice_number)
        await self.bot.say('Rolled a **' + str(dice_roll) + '** with a ' + dice)

    # RANDOM
    @commands.group(name='random', ignore_extra=False, aliases=['rand'], invoke_without_command=True)
    async def command_random(self):
        """Generates a number between 0 and 1 (inclusive)."""
        self.log_command_call('random')

        random_number = random.random()
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM BETWEEN
    @command_random.command(name='between', ignore_extra=False, aliases=['b', '-b', 'betw'])
    async def command_random_between(self, a: int, b: int):
        """Generates a number between a and b (inclusive)."""
        self.log_command_call('random between')

        values = [a, b]
        values.sort()  # Either value can be the smallest one
        a, b = values
        random_number = random.randint(a, b)
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM FROM
    @command_random.command(name='from', ignore_extra=False, aliases=['f', '-f', 'fr'])
    async def command_random_from(self, *args: str):
        """Randomly selects one of the space separated arguments."""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('random from')

        result = random.choice(args)
        await self.bot.say('Result: **' + result + '**')

    # SUM
    @commands.command(name='sum', ignore_extra=False, aliases=['add', '+'])
    async def command_sum(self, *numbers: Converters.number):
        """Sums all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('sum')

        result = Converters.number(functools.reduce(operator.add, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' + '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # SUBTRACT
    @commands.command(name='subtract', ignore_extra=False, aliases=['-'])
    async def command_subtract(self, *numbers: Converters.number):
        """Subtracts all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('subtract')

        result = Converters.number(functools.reduce(operator.sub, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' - '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # DIVIDE
    @commands.command(name='divide', ignore_extra=False, aliases=['/'])
    async def command_divide(self, *numbers: Converters.number):
        """Divides all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('divide')

        result = Converters.number(functools.reduce(operator.truediv, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' / '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # MULTIPLY
    @commands.command(name='multiply', ignore_extra=False, aliases=['mul', '*'])
    async def command_multiply(self, *numbers: Converters.number):
        """Multiplies all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('multiply')

        result = Converters.number(functools.reduce(operator.mul, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' * '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # 8BALL
    @commands.command(name='8ball', ignore_extra=False, aliases=['eightball', '8b'])
    async def command_eightball(self, *args: str):
        """Bot uses its fortune-telling powers to answer your question."""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('8ball')

        answer = random.randint(0, len(self._eightball_answers) - 1)
        if answer <= 9:  # Affirmative answer
            emoji = self._eightball_emojis[0]
        elif answer <= 14:  # Meh answer
            emoji = self._eightball_emojis[1]
        else:  # Negative answer
            emoji = self._eightball_emojis[2]
        await self.bot.say('`' + ' '.join(args) + '`: ' + self._eightball_answers[answer] + ' ' + emoji)

    # POLL
    @commands.group(name='poll', ignore_extra=False, pass_context=True, invoke_without_command=True)
    async def command_poll(self, context, poll_name: str, *args: str):
        """Creates a poll with the arguments passed as vote options.
        The first argument is the name of the poll, which is used when voting.
        It can be a single word or any number of space-separated words if enclosed within quotation marks.
        ex:
            poll
            poll_name
            "Is this the poll name?"

        A poll ends when the subcommand 'end' is passed with the poll's name.
        Within 5 minutes of the poll's creation only the original author can close the poll."""
        if len(args) < 2:    # at least two poll options
            raise commands.MissingRequiredArgument
        self.log_command_call('poll')

        channel = context.message.channel.id
        if channel not in self._polls:
            self._polls[channel] = {}
        if poll_name in self._polls[channel]:
            await self.bot.say(ERROR_MESSAGES['poll_already_exists'] +
                               '`' + '`, `'.join(self._polls[channel][poll_name]) + '`')
        else:
            self._polls[channel][poll_name] = {}
            for option in args:  # Set all poll options at zero votes
                self._polls[channel][poll_name][option] = set()

            if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
                author_name = context.message.author.nick
            else:
                author_name = context.message.author.name

            await self.bot.say(author_name + ' created poll `' + poll_name + '` with ' +
                               str(len(args)) + ' options: `' + '`, `'.join(args) + '`')
            await self.bot.say('Say `!poll end <poll_name>` to end poll')

            self._poll_creator[channel][poll_name] = context.message.author.id
            await asyncio.sleep(10*60)  # 10 minutes timer
            del self._poll_creator[channel][poll_name]  # every user can now end the poll

    # POLL VOTE
    @command_poll.command(name='vote', ignore_extra=False, aliases=['v', '-v', 'vt'])
    async def command_poll_vote(self, poll: str, option: str):
        """Vote on an option of a certain poll."""
        self.log_command_call('poll vote')

        # TODO poll doesn't exist
        # TODO option doesn't exist
        # TODO limit to one vote per user
        pass

    # POLL STATUS
    @command_poll.command(name='status', ignore_extra=False, aliases=['s', '-s', 'stat'])
    async def command_poll_status(self, *poll: str):
        """Status of all polls or just the one specified.
        Shows who voted for each option."""
        if len(poll) > 1:    # maximum one option
            raise commands.TooManyArguments
        self.log_command_call('poll status')

        if len(poll) == 0:
            # TODO show all poll status
            pass
        else:
            # TODO poll doesn't exist
            # TODO show only the one poll status
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
