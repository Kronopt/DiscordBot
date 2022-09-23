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
    from discord import app_commands, Interaction


def logging_wrapper(
    command: "app_commands.Command", logger: "logging.Logger"
) -> "Callable":
    """
    Logging wrapper for command callbacks
    Every command in a Cog should be wrapped in a logging call

    Parameters
    ----------
    command: discord.app_commands.Command
        Command whose callback is to be wrapped
    logger: logging.Logger

    Returns
    -------
    Wrapper function of command callback
    """
    command_callback = command.callback

    @functools.wraps(command_callback)
    async def wrapper(*args, **kwargs):
        interaction = args[1]  # self, interaction, ...
        log_command_call(interaction, logger, command.name)
        await command_callback(*args, **kwargs)

    return wrapper


def log_command_call(
    interaction: "Interaction", logger: "logging.Logger", command_name: str
):
    """
    Logs a command call

    Parameters
    ----------
    context: discord.app_commands.Interaction
    logger: logging.logger
    command_name: str
        name of the command whose call is being logged
    """
    guild = interaction.guild
    channel = interaction.channel
    channel = (
        f"{guild.name}.{channel.name} ({str(channel.type)})"
        if guild
        else "Private Message"
    )
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    logger.info(
        f"command called: {command_name}; " f"channel: {channel}; " f"user: {user}"
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
