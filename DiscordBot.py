#!python3
# coding: utf-8


"""
Bot main .py file.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""


import argparse
import logging
import traceback
import beckett.exceptions
import discord
from discord.ext import commands
from DiscordBot.ErrorMessages import ERROR_MESSAGES
from DiscordBot.Cogs.General import General
from DiscordBot.Cogs.Math import Math
from DiscordBot.Cogs.Funny import Funny
from DiscordBot.Cogs.Gifs import Gifs
from DiscordBot.Cogs.AsciiEmojis import AsciiEmojis
from DiscordBot.Cogs.Xkcd import Xkcd


logging.basicConfig(level=logging.INFO)

command_prefix = '!'
BOT = commands.Bot(command_prefix=commands.when_mentioned_or(command_prefix))

# remove default help command
BOT.remove_command('help')

# Add cogs
BOT.add_cog(General(BOT))
BOT.add_cog(Math(BOT))
BOT.add_cog(Funny(BOT))
BOT.add_cog(Gifs(BOT))
BOT.add_cog(AsciiEmojis(BOT))
BOT.add_cog(Xkcd(BOT))
# BOT.add_cog(Polls(BOT))  # TODO not implemented yet


@BOT.event
async def on_ready():
    logging.info('started on_ready')

    logging.info('Logged in as: %s, %s' % (BOT.user.name, BOT.user.id))
    logging.info('Channels connected to:')
    for channel in BOT.get_all_channels():
        logging.info(' -%s.%s, %s-channel %s' % (channel.server.name, channel.name, str(channel.type), channel.id))
    print('Bot is ready')
    print('------------')

    await BOT.change_presence(game=discord.Game(name='Type %shelp' % command_prefix))


@BOT.event
async def on_command_error(error, context):
    if isinstance(error, commands.CommandNotFound):  # Ignore non-existent commands
        pass

    elif isinstance(error, (commands.TooManyArguments,
                            commands.MissingRequiredArgument,
                            commands.BadArgument,
                            commands.UserInputError)):
        logging.info('bad arguments for command %s: %s', context.invoked_with, context.message.content)
        await BOT.send_message(context.message.channel,
                               ERROR_MESSAGES[context.command.name] % (command_prefix, context.invoked_with))

    elif isinstance(error, commands.CommandInvokeError) and isinstance(error.original, ZeroDivisionError):
        logging.info('zero division error on command %s', context.invoked_with)
        await BOT.send_message(context.message.channel,
                               ERROR_MESSAGES['zero_division_error'] % (command_prefix, context.invoked_with))

    elif (isinstance(error, commands.CommandInvokeError) and
          isinstance(error.original, beckett.exceptions.InvalidStatusCodeError)):
        logging.info('Invalid HTTP status code on command %s: %s' % (context.invoked_with, error.original.status_code))

        if context.command.name == 'id':  # xkcd id command
            if error.original.status_code == 404:
                await BOT.send_message(context.message.channel, 'xkcd comic with the given id was not found.')
            else:
                await BOT.send_message(context.message.channel, 'Can\'t reach xkcd.com at the moment.')

        elif context.command.name == 'joke':  # joke command
            await BOT.send_message(context.message.channel, 'Can\'t retrieve a joke from the server at the moment.')

    else:
        print('Ignoring exception in command', context.invoked_with)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))

    # TODO NoPrivateMessage, CheckFailure, DisabledCommand, CommandOnCooldown,
    # TODO NotOwner, MissingPermissions, BotMissingPermissions


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description='Run Discord Bot')
    cli_parser.add_argument('token', help='Bot token')
    cli_parser = cli_parser.parse_args()

    BOT.run(cli_parser.token)

    # https://discordapp.com/developers/applications/me


# TODO COMMAND send message with delay
