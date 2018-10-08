#!python3
# coding: utf-8


"""
Bot main .py file.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""


import argparse
import logging
import traceback
import sys
import beckett.exceptions
import discord
import DiscordBot.Cogs
from discord.ext import commands
from DiscordBot.Cogs.Math import Math


logging.basicConfig(level=logging.INFO)

command_prefix = '!'
BOT = commands.Bot(command_prefix=commands.when_mentioned_or(command_prefix))
BOT.command_prefix_simple = command_prefix

# remove default help command
BOT.remove_command('help')

# add cogs dynamically
for cog_name in DiscordBot.Cogs.__all__:
    cog_module = __import__('DiscordBot.Cogs.%s' % cog_name, fromlist=[cog_name])
    if hasattr(cog_module, cog_name):  # ignores "work in progress" cogs
        cog = getattr(cog_module, cog_name)(BOT)
        BOT.add_cog(cog)


@BOT.event
async def on_ready():
    logging.info('Logged in as: %s, (id: %s)' % (BOT.user.name, BOT.user.id))
    logging.info('Channels connected to:')
    for channel in BOT.get_all_channels():
        logging.info('    %s.%s (%s) (id: %s)' % (channel.server.name, channel.name, str(channel.type), channel.id))
    print('Bot is ready')
    print('------------')

    await BOT.change_presence(game=discord.Game(name='Type %shelp' % command_prefix))


@BOT.event
async def on_command_error(error, context):
    """
    This will always be called after an exception is raised on a command.
    In order to avoid duplicate log entries, errors that should be treated individually per command are ignored here.
    """
    # Ignore non-existent and disabled commands
    # Handle these 6 exceptions for each command individually
    if isinstance(error, (commands.CommandNotFound, commands.DisabledCommand,
                          commands.TooManyArguments, commands.MissingRequiredArgument,
                          commands.BadArgument, commands.CommandOnCooldown,
                          commands.NoPrivateMessage, commands.CheckFailure)):
        pass
    # Exception handled in Math.command_divide
    elif (isinstance(error, commands.CommandInvokeError) and
          isinstance(error.original, ZeroDivisionError) and
          context.command.callback is Math.command_divide.callback):
        pass
    elif (isinstance(error, commands.CommandInvokeError) and
          isinstance(error.original, beckett.exceptions.InvalidStatusCodeError)):
        pass
    else:
        print('Ignoring exception in command', context.invoked_with, file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description='Run Discord Bot')
    cli_parser.add_argument('token', help='Bot token')
    cli_parser = cli_parser.parse_args()

    BOT.run(cli_parser.token)

    # https://discordapp.com/developers/applications/me


# TODO COMMAND send message with delay
# TODO TESTS!
