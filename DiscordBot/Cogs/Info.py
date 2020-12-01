#!python3
# coding: utf-8


"""
Info Commands
"""


import datetime
import platform
import discord
import psutil
from discord.ext import commands
from DiscordBot.BaseCog import Cog


class Info(Cog):
    """
    Commands that show information about the bot
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = 'ℹ️'
        self.info_embed = self.create_info_embed()
        self.system_embed = self.create_system_embed()

    @staticmethod
    async def uptime():
        today = datetime.datetime.today()
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        return str(today - boot_time)

    @staticmethod
    def os_name():
        return platform.platform()

    @staticmethod
    def cpu_info():
        cores = psutil.cpu_count()
        cores = f'{cores} cores' if cores > 1 else f'{cores} core'
        return cores + ' ({:.2f}GHz)'.format(psutil.cpu_freq().current/1000)

    @staticmethod
    def ram():
        return psutil._common.bytes2human(psutil.virtual_memory().total)

    @staticmethod
    def python_version():
        return platform.python_version()

    @staticmethod
    def discord_version():
        return discord.__version__

    def create_info_embed(self):
        embed = discord.Embed(colour=self.embed_colour, title='\u200b')
        embed.set_author(name='📓 Information')
        embed.add_field(name='👨‍💻 Author',
                        value='[Kronopt](https://github.com/Kronopt) \n\u200b')
        embed.add_field(name='🏗️ Framework',
                        value=f'[discord.py v{self.discord_version()}]'
                              '(https://github.com/Rapptz/discord.py) \n\u200b')
        embed.add_field(name='📁 Github',
                        value='[DiscordBot repository](https://github.com/Kronopt/DiscordBot)'
                              '\n\u200b')
        return embed

    def create_system_embed(self):
        embed = discord.Embed(colour=self.embed_colour, title='\u200b')
        embed.set_author(name='🖥️ Host System Information')
        embed.add_field(name='📟  OS', value=(self.os_name()) + '\n\u200b')
        embed.add_field(name='🎛️ CPU', value=(self.cpu_info()) + '\n\u200b')
        embed.add_field(name='🧠 RAM', value=(self.ram()) + '\n\u200b')
        embed.add_field(name='🐍 Python version', value=(self.python_version()) + '\n\u200b')

        return embed

    ##########
    # COMMANDS
    ##########

    # INFO
    @commands.command(name='info', ignore_extra=False, aliases=['information'])
    async def command_info(self, context):
        """
        Shows author, github page and framework

        ex:
        `<prefix>info`
        `<prefix>information`
        """
        await context.send(embed=self.info_embed)

    # SYSTEM
    @commands.command(name='system', ignore_extra=False, aliases=['sys'])
    async def command_system(self, context):
        """
        Shows bot host system information

        OS, CPU, RAM, Python version and Up time

        ex:
        `<prefix>system`
        `<prefix>sys`
        """
        embed = self.system_embed
        embed.add_field(name='🕒 Up time', value=(await self.uptime()) + '\n\u200b')

        await context.send(embed=embed)

        embed.remove_field(-1)

    ################
    # ERROR HANDLING
    ################

    @command_info.error
    @command_system.error
    async def info_on_error(self, context, error):
        if context.command.callback is self.command_info.callback:
            bot_message = f'`{context.prefix}{context.invoked_with}` takes no arguments'
        else:
            bot_message = f'`{context.prefix}{context.invoked_with}` either takes either no ' \
                          'arguments or a command (and possible subcommands)'
        await self.generic_error_handler(
            context, error,
            (commands.MissingRequiredArgument, commands.CommandOnCooldown,
             commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message))
