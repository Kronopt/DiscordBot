#!python3
# coding: utf-8


"""
Base Cog class.
Each Cog should inherit from this.
Each bot command should be decorated with a @command decorator.
"""


import functools
import inspect
import logging
from collections import OrderedDict
from discord.ext import commands


logger = logging.getLogger('discord')


def logging_wrapper(command):
    """
    Logging wrapper for command callback

    Parameters
    ----------
    command: commands.core.Command
        Command whose callback is to be wrapped

    Returns
    -------
    Wrapper function of command callback
    """
    command_callback = command.callback
    command_name = '%s %s' % (command.full_parent_name, command.name) if command.parent else command.name

    @functools.wraps(command_callback)
    async def inner(*args, **kwargs):
        logger.info('command called: ' + command_name)
        await command_callback(*args, **kwargs)
    return inner


class CogMeta(type):

    def __new__(mcs, name, bases, body):
        for attribute in body.values():
            if isinstance(attribute, commands.core.Command):  # Wrap every command inside a Cog in a logging function
                attribute.callback = logging_wrapper(attribute)
        return super().__new__(mcs, name, bases, body)


class Cog(metaclass=CogMeta):

    # {Cog_object: {command_function_name: command_object, ...}, ...} of all commands from all instantiated Cogs
    all_commands = OrderedDict()

    def __init__(self, bot):
        """
        Parameters
        ----------
        bot: discord.ext.commands.Bot
        """
        self.bot = bot
        self.name = self.__class__.__name__
        self.logger = logger
        self.embed_colour = 0xe74c3c

        # {command_function_name: command_object, ...}
        self.commands = OrderedDict(inspect.getmembers(self, lambda x: issubclass(x.__class__, commands.core.Command)))
        Cog.all_commands[self] = self.commands

        self.logger.info('loaded commands from Cog %s: %s' % (self.name,
                                                              ', '.join(command for command in self.commands)))

    def __unload(self):
        """Cleanup goes here"""
        pass

    def __check(self, context):
        """Cog global check goes here"""
        return True
