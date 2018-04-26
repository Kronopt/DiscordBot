#!python3
# coding: utf-8


"""
Base Cog class.
Each Cog should inherit from this.
Each bot command should be decorated with a @command decorator.
"""


import inspect
import logging
from collections import OrderedDict
from discord.ext import commands


class Cog:

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
        self.logger = logging.getLogger('discord')
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

    def log_command_call(self, command):
        """
        Logs calls to a command as INFO

        Parameters
        ----------
        command: str
            name of command
        """
        self.logger.info('command called: ' + command)
