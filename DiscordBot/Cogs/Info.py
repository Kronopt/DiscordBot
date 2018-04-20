#!python3
# coding: utf-8


"""
Info Commands.
"""


import discord
from discord.ext import commands
from .BaseCog import Cog


class Info(Cog):
    """Info Commands"""

    def __init__(self, bot):
        super().__init__(bot)

    # INFO
    @commands.command(name='info', ignore_extra=False)
    async def command_info(self):
        """Shows author, github page and framework."""
        self.log_command_call('info')

        bot_info = await self.bot.application_info()
        bot_owner = bot_info.owner.display_name + '#' + str(bot_info.owner.discriminator)

        embed_info = discord.Embed(colour=self.embed_colour)
        embed_info.add_field(name='Author', value=bot_owner, inline=False)
        embed_info.add_field(name='Framework', value='[discord.py](https://github.com/Rapptz/discord.py)', inline=False)
        embed_info.add_field(name='Github', value='https://github.com/Kronopt/DiscordBot', inline=False)

        await self.bot.say(embed=embed_info)

    # # HELP
    # @commands.command(name='help', ignore_extra=False)
    # async def command_help(self):
    #     """Shows help message."""
    #     self.log_command_call('help')
    #
    #     await self.bot.say('')
    #     TODO copy most logic from HelpFormatter.format
    #     TODO output help as embed
    #     TODO don't forget aliases

    #     TODO '!help' shows all commands
    #     TODO '!help <command>' shows detailed info on command
    #     TODO '!help <command group>' shows info on command group and associated commands


# TODO add Cog to BOT in DiscordBot.py
# TODO add errors in ErrorMessages.py
