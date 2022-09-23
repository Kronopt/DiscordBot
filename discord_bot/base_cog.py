#!python3
# coding: utf-8


"""
Base Cog class
Each Cog should inherit from this
Each bot command should be decorated with a @command decorator
"""


import inspect
import logging
from typing import TYPE_CHECKING, Type
from collections import OrderedDict
from discord import app_commands, Interaction
from discord.ext import commands
from discord_bot.services import command_logging

if TYPE_CHECKING:
    from .bot import Bot


class CogMeta(commands.CogMeta):
    """
    Cog meta class
    Wraps every command inside a Cog in a logging function and
    forces implementation of command error handler
    """

    def __new__(cls, *args, **kwargs):
        name, bases, attrs = args
        logger = logging.getLogger(f"discord_bot.cog.{name}")
        attrs["logger"] = logger

        for attribute in attrs.values():
            if isinstance(attribute, app_commands.Command):

                # Force implementation of command error handler
                if not hasattr(attribute, "on_error"):
                    raise NotImplementedError(
                        f"Command: {attribute.name} ({attribute.callback.__name__}) in Cog: "
                        f"{name} has no error handler"
                    )

                attribute._callback = command_logging.logging_wrapper(attribute, logger)

        return super().__new__(cls, name, bases, attrs)


class Cog(commands.Cog, metaclass=CogMeta):
    """
    Base Cog class
    """

    # all commands from all instantiated Cogs:
    # {Cog_object: {command_function_name: command_object, ...}, ...}
    all_commands = OrderedDict()

    def __init__(self, bot: "Bot"):
        """
        Parameters
        ----------
        bot: discord_bot.bot.Bot
            Bot
        """
        super().__init__()
        self.bot = bot
        self.name = self.__class__.__name__
        # self.logger  # defined in CogMeta.__new__
        self.embed_colour = bot.embed_colour
        self.emoji = ""

        # {command_function_name: command_object, ...}
        self.commands = OrderedDict(
            inspect.getmembers(
                self, lambda x: issubclass(x.__class__, app_commands.Command)
            )
        )
        Cog.all_commands[self] = self.commands

        self.logger.info("Loaded commands:")
        for command in self.commands.values():
            self.logger.info(f" • {command.qualified_name}")

    def unhandled_exceptions(
        self,
        interaction: Interaction,
        error: Exception | app_commands.AppCommandError,
        *unhandled_exceptions: Type[app_commands.AppCommandError],
    ) -> bool:
        """
        Warn about unhandled exceptions
        To be used on each command's error handler
        (in case I implement these features and forget to handle the related errors...)

        Parameters
        ----------
        interaction: app_commands.Interaction
        error: Exception or app_commands.AppCommandError
        unhandled_exceptions: tuple(type(app_commands.AppCommandError))

        Returns
        -------
        bool
            True if error wasn't defined as an unhandled exception, False otherwise
        """
        if isinstance(error, unhandled_exceptions):
            exceptions = ", ".join([e.__name__ for e in unhandled_exceptions])
            self.logger.warning(
                f"Unhandled Exception '{error.__class__.__name__}': "
                f"{exceptions} exceptions are not handled for "
                f"{interaction.command.name}"
            )
            return False

        return True

    async def generic_error_handler(
        self,
        interaction: Interaction,
        error: Exception | app_commands.AppCommandError,
        unhandled_exceptions: tuple[Type[app_commands.AppCommandError], ...],
        *handled_exceptions: tuple[Type[Exception], str],
    ) -> None:
        """
        Base error handler function
        Warning will be logged if an unhandled exception is thrown

        Parameters
        ----------
        interaction: app_commands.Interaction
        error: Exception or app_commands.AppCommandError
        unhandled_exceptions: tuple(type(app_commands.AppCommandError))
        handled_exceptions: tuple(type(Exception), str)
        """
        for handled_exception, bot_message in handled_exceptions:
            if isinstance(error, handled_exception):
                self.logger.info(
                    f"{error.__class__.__name__} exception in command "
                    f"{interaction.command.name}: {error}"
                )
                await interaction.response.send_message(bot_message, ephemeral=True)
                return

        if self.unhandled_exceptions(interaction, error, *unhandled_exceptions):
            command_logging.log_command_exception(self.logger, interaction.command.name)

    def __hash__(self):
        return hash(self.name)
