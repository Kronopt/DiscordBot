#!python3
# coding: utf-8


"""
Command logging wrapper
Wraps commands in a logging call
"""


import functools
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging
    from typing import Callable
    from discord.ext import commands


def logging_wrapper(
    command: "commands.Command", logger: "logging.Logger"
) -> "Callable":
    """
    Logging wrapper for command callbacks
    Every command in a Cog should be wrapped in a logging call

    Parameters
    ----------
    command: commands.Command
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
        log_command_call(context, logger, command.qualified_name)
        await command_callback(*args, **kwargs)

    return wrapper


def log_command_call(
    context: "commands.Context", logger: "logging.Logger", command_name: str
):
    """
    Logs a command call

    Parameters
    ----------
    context: discord.ext.commands.Context
    logger: logging.logger
    command_name: str
        name of the command whose call is being logged
    """
    guild = context.message.guild
    channel = context.message.channel
    channel = (
        f"{guild.name}.{channel.name} ({str(channel.type)})"
        if guild
        else "Private Message"
    )
    user = f"{context.message.author.name}#{context.message.author.discriminator}"
    logger.info(
        f"command called: {command_name}; "
        f"message: {context.message.clean_content}; "
        f"channel: {channel}; "
        f"user: {user}"
    )


def log_command_exception(logger: "logging.Logger", command_name: str):
    """
    Logs command error

    Parameters
    ----------
    logger: logging.logger
    command_name: str
        name of the command whose error is being logged
    """
    _, error, traceback = sys.exc_info()
    logger.exception(f"When calling command: {command_name}\n{error}\n{traceback}")
