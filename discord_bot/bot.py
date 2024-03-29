#!python3
# coding: utf-8


"""
Bot class
"""


import logging
import sys
import discord
from discord.ext import commands
import discord_bot.cogs
from discord_bot.services import command_logging, help_command


class Bot(commands.Bot):
    """
    Main Bot class
    """

    def __init__(self, intents: discord.Intents, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.embed_colour = 16777215  # colour of discord embed used in some messages
        self.cog_args = kwargs

        self.logger.info("Starting Bot")

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=help_command.HelpCommand(self.embed_colour),
            *args,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        """
        (Overridden)

        Called to setup the bot.
        To perform asynchronous setup after the bot is logged in
        but before it has connected to the Websocket.
        This is only called once, in login(), and will be called before any events are dispatched,
        making it a better solution than doing such setup in the on_ready() event.
        Sets up Cogs.
        """
        self.logger.info("Setting up Cogs...")

        # add cogs dynamically
        # assumes each Cog is defined in its own file and the name of the Cog class is the name
        # of the file capitalized (ex: 'funny.py' -> Funny())
        for cog_name in discord_bot.cogs.__all__:
            cog_module = __import__(f"discord_bot.cogs.{cog_name}", fromlist=[cog_name])
            class_name = cog_name.capitalize()
            if hasattr(cog_module, class_name):
                cog = getattr(cog_module, class_name)(self)
                await self.add_cog(cog)

        # sync commands
        self.logger.info("Syncing commands...")
        await self.tree.sync()

    async def on_ready(self) -> None:
        """
        (Overridden)

        Called when bot finishes preparing data received from Discord
        """
        self.logger.info("Logged in as: %s (id: %s)", self.user.name, self.user.id)
        self.logger.info("Channels connected to:")
        for channel in self.get_all_channels():
            self.logger.info(
                " • %s.%s (%s) (id: %s)",
                channel.guild.name,
                channel.name,
                channel.type,
                channel.id,
            )

        # set presence message ("Watching for /hi")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for /hi"
            )
        )

        self.logger.info("Bot is ready")

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """
        (Overridden)

        Called when an uncaught/unhandled exception occurs
        """
        self.logger.exception(
            "When handling event: %s\nargs: %s\nkwargs:%s\n%s",
            event,
            args,
            kwargs,
            sys.exc_info()[2],
        )

    async def on_command_error(
        self, ctx: commands.Context, exception: commands.errors.CommandError
    ) -> None:
        """
        (Overridden)

        Called when an exception occurs when executing a command
        """
        # ignore non-existent commands
        if isinstance(exception, commands.CommandNotFound):
            return

        # original on_command_error logic but with logging
        if self.extra_events.get("on_command_error", None):
            return
        command = ctx.command
        if command and command.has_error_handler():
            return

        cog = ctx.cog
        if cog and cog.has_error_handler():
            return

        command_logging.log_command_exception(self.logger, ctx.command.qualified_name)
