#!python3
# coding: utf-8


"""
Base Cog class
Each Cog should inherit from this
Each bot command should be decorated with a @command decorator
"""


import inspect
import logging
from collections import OrderedDict
from discord.ext import commands
from discord_bot.services import command_logging


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
            if isinstance(attribute, commands.core.Command):

                # Force implementation of command error handler
                if not hasattr(attribute, "on_error"):
                    raise NotImplementedError(
                        f"Command: {attribute.name} ({attribute.callback.__name__}) in Cog: "
                        f"{name} has no error handler"
                    )

                attribute.callback = command_logging.logging_wrapper(attribute, logger)

        return super().__new__(cls, name, bases, attrs)


class Cog(commands.Cog, metaclass=CogMeta):
    """
    Base Cog class
    """

    # all commands from all instantiated Cogs:
    # {Cog_object: {command_function_name: command_object, ...}, ...}
    all_commands = OrderedDict()

    def __init__(self, bot):
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
                self, lambda x: issubclass(x.__class__, commands.core.Command)
            )
        )
        Cog.all_commands[self] = self.commands

        self.logger.info("Loaded commands:")
        for command in self.commands.values():
            self.logger.info(f"    {command.qualified_name}")

    @staticmethod
    def format_cooldown_time(seconds):
        """
        Format cooldown time
        To be used in the handling of commands.CommandOnCooldown exception

        Parameters
        ----------
        seconds: float

        Returns
        -------
        time: str
            Cooldown remaining time in H:M:S format
        """
        seconds = int(seconds)
        if seconds <= 60:  # only seconds
            time = f"{seconds}s"
        elif seconds <= 60 * 60:  # minutes and seconds
            time = f"{seconds // 60}m {seconds % 60}s"
        else:  # hours, minutes and seconds
            time = (
                f"{seconds // (60 * 60)}h "
                + f"{seconds % (60 * 60) // 60}m "
                + f"{seconds % (60 * 60) % 60}s"
            )
        return time

    def unhandled_exceptions(self, context, error, *unhandled_exceptions):
        """
        Warn about unhandled exceptions
        To be used on each command's error handler
        (in case I implement these features and forget to handle the related errors...)

        Parameters
        ----------
        context: commands.context.Context
        error: Exception or commands.CommandInvokeError
        unhandled_exceptions: iter(commands.errors.CommandError)

        Returns
        -------
        bool
            True if error wasn't defined as an unhandled exception, False otherwise
        """
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, (*unhandled_exceptions,)):
            exceptions = ", ".join([e.__name__ for e in unhandled_exceptions])
            self.logger.warning(
                f"Unhandled Exception '{error.__class__.__name__}': "
                f"{exceptions} exceptions are not handled for "
                f"{context.prefix}{context.invoked_with}"
            )
            return False

        return True

    async def generic_error_handler(
        self, context, error, unhandled_exceptions, *handled_exceptions
    ):
        """
        Base error handler function
        Warning will be logged if an unhandled exception is thrown

        Parameters
        ----------
        context: commands.context.Context
        error: Exception or commands.CommandInvokeError
        unhandled_exceptions: tuple of commands.errors.CommandError
        handled_exceptions: (type of Exception, str)
        """
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        for handled_exception, bot_message in handled_exceptions:
            if isinstance(error, handled_exception):
                self.logger.info(
                    f"{error.__class__.__name__} exception in command "
                    f"{context.command.qualified_name}: {error}"
                )
                await context.send(bot_message)
                await context.send_help(context.command)
                return
        if self.unhandled_exceptions(context, error, unhandled_exceptions):
            command_logging.log_command_exception(
                self.logger, context.command.qualified_name
            )

    def __hash__(self):
        return hash(self.name)
