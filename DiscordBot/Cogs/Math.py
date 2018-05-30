#!python3
# coding: utf-8


"""
Math Commands.
"""


import functools
import operator
from discord.ext import commands
from .BaseCog import Cog
from DiscordBot import Converters


class Math(Cog):
    """Math Commands"""

    def __init__(self, bot):
        super().__init__(bot)

    ##########
    # COMMANDS
    ##########

    # SUM
    @commands.command(name='sum', ignore_extra=False, aliases=['add', '+'])
    async def command_sum(self, *numbers: Converters.number):
        """Sums all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument

        result = Converters.number(functools.reduce(operator.add, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' + '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # SUBTRACT
    @commands.command(name='subtract', ignore_extra=False, aliases=['-'])
    async def command_subtract(self, *numbers: Converters.number):
        """Subtracts all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument

        result = Converters.number(functools.reduce(operator.sub, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' - '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # DIVIDE
    @commands.command(name='divide', ignore_extra=False, aliases=['/'])
    async def command_divide(self, *numbers: Converters.number):
        """Divides all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument

        result = Converters.number(functools.reduce(operator.truediv, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' / '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # MULTIPLY
    @commands.command(name='multiply', ignore_extra=False, aliases=['mul', '*'])
    async def command_multiply(self, *numbers: Converters.number):
        """Multiplies all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument

        result = Converters.number(functools.reduce(operator.mul, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' * '.join(numbers) + ' = ' + '**' + str(result) + '**')

    ################
    # ERROR HANDLING
    ################

    @command_sum.error
    @command_subtract.error
    @command_multiply.error
    async def sum_subtract_divide_multiply_on_error(self, error, context):
        bot_message = '`%s%s` takes at least 1 number.' % (context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.TooManyArguments, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.MissingRequiredArgument, bot_message),
                                         (commands.BadArgument, bot_message))

    @command_divide.error
    async def ping_hi_on_error(self, error, context):
        bot_message = '`%s%s` takes at least 1 number.' % (context.prefix, context.invoked_with)
        bot_message_zero_division_error = '`%s%s` can\'t divide by zero.'
        await self.generic_error_handler(error, context,
                                         (commands.TooManyArguments, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.MissingRequiredArgument, bot_message),
                                         (commands.BadArgument, bot_message))
        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, ZeroDivisionError):
            self.logger.info('%s exception in command %s: %s',
                             error.original.__class__.__name__, context.command.qualified_name, context.message.content)
            await self.bot.say(bot_message_zero_division_error)
