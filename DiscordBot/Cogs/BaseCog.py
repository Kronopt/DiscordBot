#!python3
# coding: utf-8


"""
Base Cog class.
Each Cog should inherit from this.
Each bot command should be decorated with a @command decorator.
"""


import functools
import inspect
import logging
from collections import OrderedDict
from discord.ext import commands


logger = logging.getLogger('discord')


def logging_wrapper(command):
    """
    Logging wrapper for command callback

    Parameters
    ----------
    command: commands.core.Command
        Command whose callback is to be wrapped

    Returns
    -------
    Wrapper function of command callback
    """
    command_callback = command.callback

    @functools.wraps(command_callback)
    async def wrapper(*args, **kwargs):
        logger.info('command called: ' + command.qualified_name)
        await command_callback(*args, **kwargs)
    return wrapper


class CogMeta(type):

    def __new__(mcs, name, bases, body):
        for attribute in body.values():
            if isinstance(attribute, commands.core.Command):  # Wrap every command inside a Cog in a logging function
                attribute.callback = logging_wrapper(attribute)
                if not hasattr(attribute, 'on_error'):  # Force implementation of command error handler
                    raise NotImplementedError('Command: %s (%s) in Cog: %s has no error handler'
                                              % (attribute.name, attribute.callback.__name__, name))
        return super().__new__(mcs, name, bases, body)


class Cog(metaclass=CogMeta):

    # {Cog_object: {command_function_name: command_object, ...}, ...} of all commands from all instantiated Cogs
    all_commands = OrderedDict()

    def __init__(self, bot):
        """
        Parameters
        ----------
        bot: discord.ext.commands.Bot
        """
        self.bot = bot
        self.name = self.__class__.__name__
        self.logger = logger
        self.embed_colour = 16777215

        # {command_function_name: command_object, ...}
        self.commands = OrderedDict(inspect.getmembers(self, lambda x: issubclass(x.__class__, commands.core.Command)))
        Cog.all_commands[self] = self.commands

        self.logger.info('loaded commands from Cog %s: %s' % (self.name,
                                                              ', '.join(command for command in self.commands)))

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

    def unhandled_exceptions(self, error, context, *unhandled_exceptions):
        """
        Warn about unhandled exceptions.
        To be used on each command's error handler.
        (in case I implement these features and forget to handle the related errors...)

        Parameters
        ----------
        error: Exception
        context: commands.context.Context
        unhandled_exceptions: iter(commands.errors.CommandError)
        """
        if isinstance(error, (*unhandled_exceptions,)):
            self.logger.warning('Unhandled Exception \'%s\': %s exceptions are not handled for %s%s'
                                % (error.__class__.__name__, ', '.join([e.__name__ for e in unhandled_exceptions]),
                                   context.prefix, context.invoked_with))

    async def generic_error_handler(self, error, context, unhandled_exceptions, *handled_exceptions):
        """
        Base error handler function.
        Warning will be logged if an unhandled exception is thrown.

        Parameters
        ----------
        error: Exception
        context: commands.context.Context
        unhandled_exceptions: tuple of commands.errors.CommandError
        handled_exceptions: (type of Exception, str)
        """
        for handled_exception, bot_message in handled_exceptions:
            if isinstance(error, handled_exception):
                self.logger.info('%s exception in command %s: %s',
                                 error.__class__.__name__, context.command.qualified_name, context.message.content)
                await self.bot.say(bot_message)
                return
        self.unhandled_exceptions(error, context, unhandled_exceptions)

    def __unload(self):
        """Cleanup goes here"""
        pass

    def __check(self, context):
        """Cog global check goes here"""
        return True
