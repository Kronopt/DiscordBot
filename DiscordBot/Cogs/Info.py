#!python3
# coding: utf-8


"""
Info Commands.
"""


from discord.ext import commands
from .BaseCog import Cog


class Info(Cog):
    """Info Commands"""

    def __init__(self, bot):
        super().__init__(bot)

    # # INFO
    # @commands.command(name='info', ignore_extra=False)
    # async def command_info(self):
    #     """Shows author, framework and github page."""
    #     self.log_command_call('info')
    #
    #     await self.bot.say('')
    #     TODO maybe an embed with author, framework, github page

    # # HELP
    # @commands.command(name='help', ignore_extra=False)
    # async def command_help(self):
    #     """Shows help message."""
    #     self.log_command_call('help')
    #
    #     await self.bot.say('')
    #     TODO copy most logic from HelpFormatter.format
    #     TODO output help as embed

    #     TODO '!help' shows all commands
    #     TODO '!help <command>' shows detailed info on command
    #     TODO '!help <command group>' shows info on command group and associated commands


# TODO add Cog to BOT in DiscordBot.py
# TODO add errors in ErrorMessages.py
