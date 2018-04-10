#!python3
# coding: utf-8


"""
General Commands.
Each bot command is decorated with a @command decorator.
"""


import functools
import operator
import random
from discord.ext import commands
from .BaseCog import Cog
from DiscordBot import Converters


class GeneralCommands(Cog):
    """General Commands"""

    def __init__(self, bot):
        super(GeneralCommands, self).__init__(bot)

        self._greetings = ['Hi', 'Hello', 'Hey', 'Sup', 'What\'s up', 'Greetings', 'Howdy']
        self._eightball_emojis = [":white_check_mark:", ":low_brightness:", ":x:"]
        self._eightball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                                   "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                                   "Signs point to yes", "Reply hazy, try again", "Ask again later",
                                   "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                                   "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good",
                                   "Very doubtful"]

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
    async def command_dice(self, *dice: Converters.dice):
        """Rolls a six sided die by default. Other dices can be rolled if specified.

        Possible dices: d4, d6, d8, d10, d12 and d20.
        A dice can either be written as 'D#' or 'd#'."""
        if len(dice) > 1:    # At most one argument
            raise commands.TooManyArguments
        self.log_command_call('dice')

        if len(dice) == 0:
            dice = 'd6'  # default
        else:
            dice = dice[0]

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

    # TODO COMMAND send message with delay
    # TODO COMMAND !joke
    # TODO COMMAND !info (author, framework, github page)
    # TODO rich presence or "playing 'type !help'"
    # TODO !xkcd (latest, random, id)
