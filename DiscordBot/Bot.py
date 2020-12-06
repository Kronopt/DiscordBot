#!python3
# coding: utf-8


"""
Bot class
"""


import logging
import sys
import discord
from discord.ext import commands
import DiscordBot.Cogs
from DiscordBot.Services import HelpCommand, CommandLogging


class Bot(commands.Bot):
    """
    Main Bot class
    """
    def __init__(self, prefix, intents, *args, **kwargs):
        self.logger = logging.getLogger('DiscordBot.Bot')
        self.prefix_simple = prefix
        self.embed_colour = 16777215  # colour of discord embed used in some messages
        self.cog_args = kwargs

        prefix = commands.when_mentioned_or(prefix) if prefix else commands.when_mentioned
        intents = intents if intents else discord.Intents.default()

        super().__init__(command_prefix=prefix,
                         intents=intents,
                         help_command=HelpCommand.HelpCommand(self.embed_colour),
                         *args, **kwargs)

        # add cogs dynamically
        for cog_name in DiscordBot.Cogs.__all__:
            cog_module = __import__(f'DiscordBot.Cogs.{cog_name}', fromlist=[cog_name])
            if hasattr(cog_module, cog_name):  # ignores "work in progress" cogs
                cog = getattr(cog_module, cog_name)(self)
                self.add_cog(cog)

    async def on_connect(self):
        """
        Called when the client has successfully connected to Discord
        This is not the same as the client being fully prepared
        Sets up Cogs
        """
        self.logger.info('Setting up Cogs...')
        for cog in self.cogs.values():
            await cog.setup_cog()

        self.logger.info('Cogs are ready')

    async def on_ready(self):
        """
        Called when bot finishes preparing data received from Discord
        """
        self.logger.info(f'Logged in as: {self.user.name}, (id: {self.user.id})')
        self.logger.info('Channels connected to:')
        for channel in self.get_all_channels():
            self.logger.info(f'    {channel.guild.name}.{channel.name} '
                             f'({str(channel.type)}) (id: {channel.id})')

        # set presence message ("Watching for !help")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'for {self.prefix_simple}help'))

        self.logger.info('Bot is ready')

    async def on_error(self, event, *args, **kwargs):
        """
        Called when an uncaught/unhandled exception occurs
        """
        self.logger.exception(
            f'When handling event: {event}, with arguments: {args}\n'
            f'{sys.exc_info()[2]}')

    async def on_command_error(self, ctx, exception):
        """
        Called when an exception occurs when executing a command
        """
        # ignore non-existent commands
        if isinstance(exception, commands.CommandNotFound):
            return

        # original on_command_error logic but with logging
        if self.extra_events.get('on_command_error', None):
            return
        if hasattr(ctx.command, 'on_error'):
            return
        if ctx.cog and commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
            return

        CommandLogging.log_command_exception(self.logger, ctx.command.qualified_name)
