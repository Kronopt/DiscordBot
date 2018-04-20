#!python3
# coding: utf-8


"""
Base Cog class.
Each Cog should inherit from this.
Each bot command should be decorated with a @command decorator.
"""


import inspect
import logging
from discord.ext import commands


class Cog:

    all_commands = []  # list of name-object of all commands from all instantiated Cogs

    def __init__(self, bot):
        """
        :param bot: discord.ext.commands.Bot
        """
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.commands = inspect.getmembers(self, lambda x: issubclass(x.__class__, commands.core.Command))
        Cog.all_commands += self.commands

        self.logger.info('loaded commands from Cog %s: %s' % (self.__class__.__name__,
                                                              ', '.join(command[0] for command in self.commands)))

    def __unload(self):
        """Cleanup goes here"""
        pass

    def __check(self, context):
        """Cog global check goes here"""
        return True

    def log_command_call(self, command):
        """
        Logs calls to a command as INFO

        :param command: str
            name of command
        """
        self.logger.info('command called: ' + command)
