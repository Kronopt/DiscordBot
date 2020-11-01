#!python3
# coding: utf-8


"""
Base Cog class
Each Cog should inherit from this
Each bot command should be decorated with a @command decorator
"""


import functools
import inspect
import logging
from collections import OrderedDict
from discord.ext import commands


def logging_wrapper(command, logger):
    """
    Logging wrapper for command callback
    Every command in a Cog is wrapped in a logging call

    Parameters
    ----------
    command: commands.core.Command
        Command whose callback is to be wrapped
    logger: logging.Logger

    Returns
    -------
    Wrapper function of command callback
    """
    command_callback = command.callback

    @functools.wraps(command_callback)
    async def wrapper(*args, **kwargs):
        context = args[1]  # self, context, ...
        guild = context.message.guild
        channel = context.message.channel
        channel = f'{guild.name}.{channel.name} ' \
                  f'({str(channel.type)})' if guild else 'Private Message'
        user = f'{context.message.author.name}#{context.message.author.discriminator}'

        logger.info(f'command called: {command.qualified_name}; '
                    f'message: {context.message.clean_content}; '
                    f'channel: {channel}; '
                    f'user: {user}')
        await command_callback(*args, **kwargs)
    return wrapper


class CogMeta(commands.CogMeta):
    """
    Cog meta class
    Wraps every command inside a Cog in a logging function and
    forces implementation of command error handler
    """
    def __new__(mcs, name, bases, body):
        logger = logging.getLogger(f'DiscordBot.Cog.{name}')
        body['logger'] = logger

        for attribute in body.values():
            if isinstance(attribute, commands.core.Command):

                # Force implementation of command error handler
                if not hasattr(attribute, 'on_error'):
                    raise NotImplementedError(
                        f'Command: {attribute.name} ({attribute.callback.__name__}) in Cog: '
                        f'{name} has no error handler')

                attribute.callback = logging_wrapper(attribute, logger)
        return super().__new__(mcs, name, bases, body)


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
        bot: discord.ext.commands.Bot
            Bot
        """
        super().__init__()
        self.bot = bot
        self.name = self.__class__.__name__
        # self.logger  # defined in CogMeta.__new__
        self.embed_colour = 16777215  # colour of discord embed used in some messages

        # {command_function_name: command_object, ...}
        self.commands = OrderedDict(
            inspect.getmembers(self, lambda x: issubclass(x.__class__, commands.core.Command)))
        Cog.all_commands[self] = self.commands

        self.logger.info(f'Loaded commands:')
        for command in self.commands.values():
            self.logger.info(f'    {command.qualified_name}')

    @staticmethod
    def format_cooldown_time(seconds):
        """
        Format cooldown time.
        To be used in the handling of commands.CommandOnCooldown exception.

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
            time = '%ss' % str(seconds)
        elif seconds <= 60*60:  # minutes and seconds
            time = '%sm %ss' % (str(seconds // 60), str(seconds % 60))
        else:  # hours, minutes and seconds
            time = '%sh %sm %ss' % (str(seconds // (60*60)),
                                    str(seconds % (60*60) // 60),
                                    str(seconds % (60*60) % 60))
        return time

    def unhandled_exceptions(self, context, error, *unhandled_exceptions):
        """
        Warn about unhandled exceptions.
        To be used on each command's error handler.
        (in case I implement these features and forget to handle the related errors...)

        Parameters
        ----------
        context: commands.context.Context
        error: Exception or commands.CommandInvokeError
        unhandled_exceptions: iter(commands.errors.CommandError)
        """
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, (*unhandled_exceptions,)):
            exceptions = ', '.join([e.__name__ for e in unhandled_exceptions])
            self.logger.warning(
                f'Unhandled Exception \'{error.__class__.__name__}\': '
                f'{exceptions} exceptions are not handled for '
                f'{context.prefix}{context.invoked_with}')

    async def generic_error_handler(
            self, context, error, unhandled_exceptions, *handled_exceptions):
        """
        Base error handler function.
        Warning will be logged if an unhandled exception is thrown.

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
                    f'{error.__class__.__name__} exception in command '
                    f'{context.command.qualified_name}: {error}')
                await context.send(bot_message)
                return
        self.unhandled_exceptions(context, error, unhandled_exceptions)

    def __hash__(self):
        return hash(self.name)
