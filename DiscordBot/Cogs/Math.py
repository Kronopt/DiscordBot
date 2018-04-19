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

    # SUM
    @commands.command(name='sum', ignore_extra=False, aliases=['add', '+'])
    async def command_sum(self, *numbers: Converters.number):
        """Sums all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('sum')

        result = Converters.number(functools.reduce(operator.add, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' + '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # SUBTRACT
    @commands.command(name='subtract', ignore_extra=False, aliases=['-'])
    async def command_subtract(self, *numbers: Converters.number):
        """Subtracts all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('subtract')

        result = Converters.number(functools.reduce(operator.sub, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' - '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # DIVIDE
    @commands.command(name='divide', ignore_extra=False, aliases=['/'])
    async def command_divide(self, *numbers: Converters.number):
        """Divides all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('divide')

        result = Converters.number(functools.reduce(operator.truediv, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' / '.join(numbers) + ' = ' + '**' + str(result) + '**')

    # MULTIPLY
    @commands.command(name='multiply', ignore_extra=False, aliases=['mul', '*'])
    async def command_multiply(self, *numbers: Converters.number):
        """Multiplies all numbers."""
        if len(numbers) == 0:  # at least one argument
            raise commands.MissingRequiredArgument
        self.log_command_call('multiply')

        result = Converters.number(functools.reduce(operator.mul, numbers))
        numbers = map(str, numbers)
        await self.bot.say(' * '.join(numbers) + ' = ' + '**' + str(result) + '**')
