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

    ##########
    # COMMANDS
    ##########

    # PING
    @commands.command(name='ping', ignore_extra=False, pass_context=True)
    async def command_ping(self, context):
        """'pong'.

        Simple command to test if bot is alive."""
        await self.bot.say('pong')

    # HI
    @commands.command(name='hi', ignore_extra=False, aliases=['hello'], pass_context=True)
    async def command_hi(self, context):
        """Greets user."""
        if hasattr(context.message.author, 'nick') and context.message.author.nick is not None:
            author_name = context.message.author.nick
        else:
            author_name = context.message.author.name
        await self.bot.say(random.choice(self.greetings) + ', ' + author_name)

    # DICE
    @commands.command(name='dice', ignore_extra=False, pass_context=True)
    async def command_dice(self, context, *dice: Converters.dice):
        """Rolls a die.

        Possible dices: d4, d6, d8, d10, d12 and d20.
        A dice can either be written as 'D#' or 'd#'."""
        if len(dice) > 1:    # At most one argument
            raise commands.TooManyArguments

        if len(dice) == 0:
            dice = 'd6'  # default
        else:
            dice = dice[0]

        dice_number = int(dice[1:])
        dice_roll = random.randint(1, dice_number)
        await self.bot.say('Rolled a **' + str(dice_roll) + '** with a ' + dice)

    # RANDOM
    @commands.group(name='random', ignore_extra=False, aliases=['rand'], invoke_without_command=True, pass_context=True)
    async def command_random(self, context):
        """Generates a number between 0 and 1.

        (inclusive)"""
        random_number = random.random()
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM BETWEEN
    @command_random.command(name='between', ignore_extra=False, aliases=['b', '-b', 'betw'], pass_context=True)
    async def command_random_between(self, context, a: int, b: int):
        """Generates a number between a and b.

        (inclusive)"""
        values = [a, b]
        values.sort()  # Either value can be the smallest one
        a, b = values
        random_number = random.randint(a, b)
        await self.bot.say('Result: **' + str(random_number) + '**')

    # RANDOM FROM
    @command_random.command(name='from', ignore_extra=False, aliases=['f', '-f', 'fr'], pass_context=True)
    async def command_random_from(self, context, *args: str):
        """Randomly selects one of the given arguments.

        Arguments cen be either space-separated or enclosed in quotes"""
        if len(args) == 0:    # at least one argument
            raise commands.MissingRequiredArgument

        result = random.choice(args)
        await self.bot.say('Result: **' + result + '**')

    ################
    # ERROR HANDLING
    ################

    @command_ping.error
    @command_hi.error
    @command_dice.error
    @command_random.error
    async def ping_hi_dice_random_on_error(self, error, context):
        if context.command.callback in (self.command_ping.callback, self.command_hi.callback):
            bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.invoked_with)
        elif context.command.callback is self.command_dice.callback:
            bot_message = '`%s%s` takes either no arguments or one of the following: %s.'\
                          % (context.prefix, context.invoked_with, ', '.join(Converters.DICES))
        else:
            bot_message = '`{0}{1}` takes no arguments or one of the predefined ones (use `{0}help {1}` for more ' \
                          'information).'.format(context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.MissingRequiredArgument, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))

    @command_random_between.error
    async def random_between_on_error(self, error, context):
        bot_message = '`%s%s` takes 2 integers as arguments.' % (context.prefix, context.command.qualified_name)
        await self.generic_error_handler(error, context,
                                         (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message),
                                         (commands.MissingRequiredArgument, bot_message))

    @command_random_from.error
    async def random_from_on_error(self, error, context):
        bot_message = '`%s%s` takes at least 1 argument.' % (context.prefix, context.command.qualified_name)
        await self.generic_error_handler(error, context,
                                         (commands.TooManyArguments, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.BadArgument, bot_message),
                                         (commands.MissingRequiredArgument, bot_message))
