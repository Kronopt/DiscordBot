#!python3
# coding: utf-8


"""
Commands (cogs) .py file.
Each bot command is decorated with a @command decorator.
"""


import functools
import operator
import random
from discord.ext import commands
from DiscordBot import Converters


ERROR_MESSAGES = {
    'ping': 'takes no arguments.',
    'dice': 'takes one of the following arguments: ' + ', '.join(Converters.DICES) + '.',
    'random': 'either takes no arguments or one of the predefined ones (type `!help random` for more info).',
    'between': 'takes 2 integers as arguments.',
    'from': 'takes at least 1 argument.',
    'sum': 'takes at least 1 number.',
    'subtract': 'takes at least 1 number.',
    'divide': 'takes at least 1 number.',
    'zero_division_error': 'can\'t divide by zero.',
    'multiply': 'takes at least 1 number.',
    '8ball': 'needs a phrase on which to apply its fortune-telling powers.',
    'poll': 'takes at least 1 argument.',
    'poll_already_exists': 'A poll is already ongoing with the following options: ',
    'vote': 'takes 1 existing poll option as argument.'
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

    _eightball_emojis = [":white_check_mark:", ":low_brightness:", ":x:"]
    _eightball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                          "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                          "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                          "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                          "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    _polls = {}  # {channel.id: {option: votes}}

    # PING
    @commands.command(name='ping', ignore_extra=False)
    async def command_ping(self):
        """Answers with 'pong'.
        Simple command to test if bot is alive."""
        await self.bot.say('pong')

    # DICE
    @commands.command(name='dice', ignore_extra=False)
    async def command_dice(self, dice: Converters.dice):
        """Rolls one of the specified d4, d6, d8, d10, d12 and d20 dices.
        A dice can either be written as 'D#' or 'd#'."""
        dice_number = int(dice[1:])
        dice_roll = random.randint(1, dice_number)
        await self.bot.say('Rolled a **' + str(dice_roll) + '** with a ' + dice)

    # RANDOM
    @commands.group(name='random', ignore_extra=False, aliases=['rand'], invoke_without_command=True)
    async def command_random(self):
        """Generates a number between 0 and 1 (inclusive)."""
        random_number = random.random()
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM BETWEEN
    @command_random.command(name='between', ignore_extra=False, aliases=['b', 'betw', '-b'])
    async def command_random_between(self, a: int, b: int):
        """Generates a number between a and b (inclusive)."""
        values = [a, b]
        values.sort()  # Either value can be the smallest one
        a, b = values
        random_number = random.randint(a, b)
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM FROM
    @command_random.command(name='from', ignore_extra=False, aliases=['fr', '-f'])
    async def command_random_from(self, *args: str):
        """Randomly selects one of the space separated arguments."""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        result = random.choice(args)
        await self.bot.say('Result: **' + result + '**')

    # SUM
    @commands.command(name='sum', ignore_extra=False, aliases=['add', '+'])
    async def command_sum(self, *numbers: Converters.number):
        """Sums all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        result = Converters.number(functools.reduce(operator.add, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' + '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # SUBTRACT
    @commands.command(name='subtract', ignore_extra=False, aliases=['-'])
    async def command_subtract(self, *numbers: Converters.number):
        """Subtracts all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        result = Converters.number(functools.reduce(operator.sub, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' - '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # DIVIDE
    @commands.command(name='divide', ignore_extra=False, aliases=['/'])
    async def command_divide(self, *numbers: Converters.number):
        """Divides all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        result = Converters.number(functools.reduce(operator.truediv, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' / '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # MULTIPLY
    @commands.command(name='multiply', ignore_extra=False, aliases=['mul', '*'])
    async def command_multiply(self, *numbers: Converters.number):
        """Multiplies all numbers."""
        if len(numbers) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        result = Converters.number(functools.reduce(operator.mul, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' * '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # 8BALL
    @commands.command(name='8ball', ignore_extra=False, aliases=['eightball', '8b'])
    async def command_eightball(self, *args: str):
        """Bot uses its fortune-telling powers to answer your question."""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
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
    async def command_poll(self, context, *args: str):
        """Creates a poll with the arguments passed as options."""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        channel = context.message.channel.id
        if channel in self._polls:  # One active poll per channel
            await self.bot.say(
                ERROR_MESSAGES['poll_already_exists'] + '`' + '`, `'.join(self._polls[channel]) + '`')
        else:  # OK
            self._polls[channel] = {}
            for arg in args:  # Set all poll options at zero votes
                self._polls[channel][arg] = 0
            await self.bot.say('Poll created with ' + str(len(args)) + ' options: `' + '`, `'.join(args) + '`')

        # TODO How to end the poll?

    # POLL VOTE
    @command_poll.command(name='vote', ignore_extra=False, aliases=['vt', 'v', '-v'])
    async def command_poll_vote(self, option: str):
        """Vote on an option in the current existing poll."""
        # TODO option doesn't exist
        # TODO poll doesn't exist yet
        # TODO limit to one vote per user
        pass
