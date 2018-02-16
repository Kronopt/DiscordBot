#!python3
# coding: utf-8


import random
from discord.ext import commands
from DiscordBot import Converters


BOT = commands.Bot(command_prefix='!', description='A DiscordBot')


@BOT.event
async def on_ready():
    print('Logged in as:', BOT.user.name + ',', BOT.user.id)
    print('Channels connected to:')
    for channel in BOT.get_all_channels():
        print(' -', channel.server.name + '.' + channel.name + ',', str(channel.type) + '-channel,', channel.id)
    print('Available commands: ', end='')
    print(*BOT.commands, sep=', ')
    print('Ready')


##########
# COMMANDS
##########

# PING
@BOT.command(name='ping')
async def command_ping():  # TODO How to force zero arguments?
    await BOT.say('pong')


@command_ping.error  # TODO check what other errors there are
async def info_error(ctx, error):  # TODO is 'info_error' the default? Can I change the name?
    if isinstance(error, commands.BadArgument):
        await BOT.say('Something about the error...')
    # else:  # TODO I don't know if this is necessary...
    #     BOT.on_command_error(error, ctx)


# DICE
@BOT.command(name='dice')
async def command_dice(dice: Converters.dice):
    dice_number = int(dice[1:])
    dice_roll = random.randint(1, dice_number)
    await BOT.say('Rolled a **' + str(dice_roll) + '** with a ' + dice)


# TODO error handling for dice

# TODO other commands from Commands.py
