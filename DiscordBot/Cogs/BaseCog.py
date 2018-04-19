#!python3
# coding: utf-8


"""
Base Cog class.
Each Cog should inherit from this.
Each bot command should be decorated with a @command decorator.
"""


import logging


class Cog:
    def __init__(self, bot):
        """
        :param bot: discord.ext.commands.Bot
        """
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.commands = list(filter(lambda command: command.startswith('command_'), self.__dir__()))

        self.logger.info('loaded commands from Cog %s: %s' % (self.__class__.__name__, ', '.join(self.commands)))

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
