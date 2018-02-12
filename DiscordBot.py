#!python3
# coding: utf-8

"""
Bot main .py file.
instantiates the discord.py client as well as the CommandsParser class for parsing arguments.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""

import argparse
import asyncio
import discord
from DiscordBot.CommandsParser import CommandsParser


client = discord.Client()
commands_parser = CommandsParser()


@client.event
async def on_ready():
    print('Logged in as:', client.user.name + ',', client.user.id)
    print('Channels connected to:')
    for channel in client.get_all_channels():
        print(' -', channel.server.name + '.' + channel.name + ',', str(channel.type) + '-channel,', channel.id)
    print('Available commands: ', end='')
    print(*commands_parser.commands_dict, sep=', ')
    print('Ready')


@client.event
async def on_message(message):
    output_message = commands_parser.parse_args(message)
    if output_message is not None:
        await client.send_message(message.channel, output_message)


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description='Run Discord Bot')
    cli_parser.add_argument('token', help='Bot token')
    cli_parser = cli_parser.parse_args()

    client.run(cli_parser.token)


# TODO setup logging (log command calls, etc)
