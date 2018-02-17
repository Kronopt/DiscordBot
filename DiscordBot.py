#!python3
# coding: utf-8


"""
Bot main .py file.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""


import argparse
import traceback
from discord.ext import commands
from DiscordBot.Commands import ERROR_MESSAGES
from DiscordBot.Commands import Commands


BOT = commands.Bot(command_prefix='!')
BOT.add_cog(Commands(BOT))


@BOT.event
async def on_ready():
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
        pass
    elif isinstance(error, (commands.TooManyArguments,
                            commands.MissingRequiredArgument,
                            commands.BadArgument,
                            commands.UserInputError)):
        await BOT.send_message(context.message.channel,
                               '`!' + context.command.name + '` ' + ERROR_MESSAGES[context.command.name])
    elif isinstance(error, commands.CommandInvokeError) and isinstance(error.original, ZeroDivisionError):
        await BOT.send_message(context.message.channel,
                               '`!' + context.command.name + '` ' + ERROR_MESSAGES['zero_division_error'])
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


# TODO setup logging (log command calls, etc)

# TODO clean help section
# TODO subcommands don't show up on the '!help' command (only when calling '!help' on the main command)
