#!python3
# coding: utf-8


"""
Bot main .py file.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""


import argparse
import logging
import traceback
from discord.ext import commands
from DiscordBot import HelpFormatter
from DiscordBot.ErrorMessages import ERROR_MESSAGES
from DiscordBot.Commands import Commands


logging.basicConfig(level=logging.INFO)

command_prefix = '!'
bot_description = 'Commands can be called as follows:\n\n' + command_prefix + '<command> [subcommand] [arguments]\n'

BOT = commands.Bot(command_prefix=command_prefix, formatter=HelpFormatter.HelpFormat(), description=bot_description)
BOT.add_cog(Commands(BOT))


@BOT.event
async def on_ready():
    logging.info('started on_ready')

    print('Logged in as:', BOT.user.name + ',', BOT.user.id)
    print('Channels connected to:')
    for channel in BOT.get_all_channels():
        print(' -', channel.server.name + '.' + channel.name + ',', str(channel.type) + '-channel,', channel.id)
    print('Available commands: ', end='')
    print(*BOT.commands, sep=', ')
    print('Ready')


@BOT.event
async def on_command_error(error, context):
    if isinstance(error, commands.CommandNotFound):  # Ignore non-existent commands
        logging.info('command not found: %s', context.message.content.split()[0][len(context.prefix):])

    elif isinstance(error, (commands.TooManyArguments,
                            commands.MissingRequiredArgument,
                            commands.BadArgument,
                            commands.UserInputError)):
        logging.info('bad arguments for command %s: %s',
                     context.command.name,
                     context.message.content[len(context.prefix) + (len(context.command.name) + 1):])
        await BOT.send_message(context.message.channel, '`' + command_prefix +
                               context.command.name + '` ' + ERROR_MESSAGES[context.command.name])

    elif isinstance(error, commands.CommandInvokeError) and isinstance(error.original, ZeroDivisionError):
        logging.info('zero division error on command %s', context.command.name)
        await BOT.send_message(context.message.channel, '`' + command_prefix +
                               context.command.name + '` ' + ERROR_MESSAGES['zero_division_error'])

    else:
        print('Ignoring exception in command ' + context.command.name)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))

    # TODO NoPrivateMessage, CheckFailure, DisabledCommand, CommandOnCooldown,
    # TODO NotOwner, MissingPermissions, BotMissingPermissions


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description='Run Discord Bot')
    cli_parser.add_argument('token', help='Bot token')
    cli_parser = cli_parser.parse_args()

    BOT.run(cli_parser.token)
