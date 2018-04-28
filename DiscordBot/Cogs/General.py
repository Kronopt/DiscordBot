#!python3
# coding: utf-8


"""
General Commands.
"""


import random
from discord.ext import commands
from .BaseCog import Cog
from DiscordBot import Converters


class General(Cog):
    """General Commands"""

    def __init__(self, bot):
        super().__init__(bot)
        self.greetings = ['Hi', 'Hello', 'Hey', 'Sup', 'What\'s up', 'Greetings', 'Howdy']

    # PING
    @commands.command(name='ping', ignore_extra=False)
    async def command_ping(self):
        """'pong'.

        Simple command to test if bot is alive."""
        self.log_command_call('ping')

        await self.bot.say('pong')

    # HI
    @commands.command(name='hi', ignore_extra=False, aliases=['hello'], pass_context=True)
    async def command_hi(self, context):
        """Greets user."""
        self.log_command_call('hi')

        if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
            author_name = context.message.author.nick
        else:
            author_name = context.message.author.name
        await self.bot.say(random.choice(self.greetings) + ', ' + author_name)

    # DICE
    @commands.command(name='dice', ignore_extra=False)
    async def command_dice(self, *dice: Converters.dice):
        """Rolls a die.

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
        """Generates a number between 0 and 1.

        (inclusive)"""
        self.log_command_call('random')

        random_number = random.random()
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM BETWEEN
    @command_random.command(name='between', ignore_extra=False, aliases=['b', '-b', 'betw'])
    async def command_random_between(self, a: int, b: int):
        """Generates a number between a and b.

        (inclusive)"""
        self.log_command_call('random between')

        values = [a, b]
        values.sort()  # Either value can be the smallest one
        a, b = values
        random_number = random.randint(a, b)
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM FROM
    @command_random.command(name='from', ignore_extra=False, aliases=['f', '-f', 'fr'])
    async def command_random_from(self, *args: str):
        """Randomly selects one of the given arguments.

        Arguments cen be either space-separated or enclosed in quotes"""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('random from')

        result = random.choice(args)
        await self.bot.say('Result: **' + result + '**')
