#!python2
# coding: utf-8

import argparse
import asyncio
import functools
import operator
import random
import discord


client = discord.Client()

# !help
help_text = '''Available Commands:\n
`!help` : Shows this help message\n
`!ping` : Bot answers with pong\n
`!dice <str dice>` : Bot rolls one of the specified d4, d6, d8, d10, d12 and d20 dices\n
`!random` : Bot generates a number between 0 and 1 (inclusive)\n
`!random_between <int a> <int b>` : Bot generates a number between a and b (inclusive)\n
`!random_from <str a> <str b> <str c> ...` : Bot randomly selects one of the space separated words/numbers/whatever\n
`!sum <number a> <number b> ...` : Bot sums all numbers\n
`!subtract <number a> <number b> ...` : Bot subtracts all numbers\n
`!divide <number a> <number b> ...` : Bot divides all numbers\n
`!multiply <number a> <number b> ...` : Bot multiplies all numbers\n
`!8ball <str>` : Bot uses its fortune-telling powers to answer your question'''
help_message_on_fail = '`!help` takes no arguments.'

# !ping
ping_message_on_fail = '`!ping` takes no arguments.'

# !dice
dices = ('d4', 'd6', 'd8', 'd10', 'd12', 'd20')
dice_message_on_fail = '`!dice` takes one of the following arguments: ' + ', '.join(dices) + '.'

# !random
random_message_on_fail = '`!random` takes no arguments.'

# !random_between
random_between_message_on_fail = '`!random_between` takes 2 integers as arguments.'

# !random_from
random_from_message_on_fail = '`!random_from` takes at least 1 argument.'

# !sum
sum_message_on_fail = '`!sum` takes at least 2 numbers.'

# !subtract
subtract_message_on_fail = '`!subtract` takes at least 2 numbers.'

# !divide
divide_message_on_fail = '`!divide` takes at least 2 numbers.'
divide_by_zero_message_on_fail = '`!divide` can\' divide by zero.'

# !multiply
multiply_message_on_fail = '`!multiply` takes at least 2 numbers.'

# !8ball
eight_ball_emojis = [":white_check_mark:", ":low_brightness:", ":x:"]
eight_ball_answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                      "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                      "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                      "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no",
                      "My sources say no", "Outlook not so good", "Very doubtful"]
eight_ball_message_on_fail = '`!8ball` needs a phrase on which to apply its fortune-telling powers.'


def zero_strip(number):
    # ex: for 7.0 return 7
    # ex: for 3.4 return 3.4
    return int(number) if int(number) == number else number


@client.event
async def on_ready():
    print('Logged in as:', client.user.name)
    print('Ready')


@client.event
async def on_message(message):
    if message.content.startswith('!'):

        # !HELP
        if message.content.startswith('!help'):
            if message.content.rstrip() == '!help':  # OK
                await client.send_message(message.channel, help_text)
            elif message.content.startswith('!help ') and len(message.content.split()) > 1:  # Shouldn't have params
                await client.send_message(message.channel, help_message_on_fail)

        # !PING
        if message.content.startswith('!ping'):
            if message.content.rstrip() == '!ping':  # OK
                await client.send_message(message.channel, 'pong')
            elif message.content.startswith('!ping ') and len(message.content.split()) > 1:  # Shouldn't have params
                await client.send_message(message.channel, ping_message_on_fail)

        # !DICE
        if message.content.startswith('!dice'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!dice':
                if len(message_arguments) == 2:
                    dice = message_arguments[1]
                    if dice.lower() in dices:  # OK
                        dice_number = int(dice[1:])
                        dice_roll = str(random.randint(1, dice_number))
                        await client.send_message(message.channel, 'Rolled a **' + dice_roll + '** with a ' + dice)
                    else:  # Wrong parameter
                        await client.send_message(message.channel, dice_message_on_fail)
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, dice_message_on_fail)

        # !RANDOM
        if message.content.startswith('!random'):
            if message.content.rstrip() == '!random':  # OK
                random_number = random.random()
                await client.send_message(message.channel, 'Result: **' + str(random_number) + '**')
            elif message.content.startswith('!random ') and len(message.content.split()) > 1:  # Shouldn't have params
                await client.send_message(message.channel, random_message_on_fail)

        # !RANDOM_BETWEEN
        if message.content.startswith('!random_between'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!random_between':
                if len(message_arguments) == 3:
                    a = message_arguments[1]
                    b = message_arguments[2]
                    try:
                        a = int(a)
                        b = int(b)
                    except ValueError:  # Non integer number
                        await client.send_message(message.channel, random_between_message_on_fail)
                    else:  # OK
                        values = [a, b]
                        values.sort()  # Either value can be the smallest one
                        a, b = values
                        random_number = random.randint(a, b)
                        await client.send_message(message.channel, 'Result: **' + str(random_number) + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, random_between_message_on_fail)

        # !RANDOM_FROM
        if message.content.startswith('!random_from'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!random_from':
                if len(message_arguments) > 1:  # OK
                    result = random.choice(message_arguments[1:])
                    await client.send_message(message.channel, 'Result: **' + result + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, random_from_message_on_fail)

        # !SUM
        if message.content.startswith('!sum'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!sum':
                if len(message_arguments) > 2:
                    arguments = message_arguments[1:]
                    try:
                        numbers = [float(i) for i in arguments]
                    except ValueError:  # Non number arguments
                        await client.send_message(message.channel, sum_message_on_fail)
                    else:  # OK
                        result = zero_strip(sum(numbers))
                        await client.send_message(message.channel,
                                                  ' + '.join(arguments) + ' = ' + '**' + str(result) + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, sum_message_on_fail)

        # !SUBTRACT
        if message.content.startswith('!subtract'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!subtract':
                if len(message_arguments) > 2:
                    arguments = message_arguments[1:]
                    try:
                        numbers = [float(i) for i in arguments]
                    except ValueError:  # Non number arguments
                        await client.send_message(message.channel, subtract_message_on_fail)
                    else:  # OK
                        result = zero_strip(functools.reduce(operator.sub, numbers))
                        await client.send_message(message.channel,
                                                  ' - '.join(arguments) + ' = ' + '**' + str(result) + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, subtract_message_on_fail)

        # !DIVIDE
        if message.content.startswith('!divide'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!divide':
                if len(message_arguments) > 2:
                    arguments = message_arguments[1:]
                    try:
                        numbers = [float(i) for i in arguments]
                    except ValueError:  # Non number arguments
                        await client.send_message(message.channel, divide_message_on_fail)
                    else:
                        try:
                            result = zero_strip(functools.reduce(operator.truediv, numbers))
                        except ZeroDivisionError:  # Divided by zero
                            await client.send_message(message.channel, divide_by_zero_message_on_fail)
                        else:  # OK
                            await client.send_message(message.channel,
                                                      ' / '.join(arguments) + ' = ' + '**' + str(result) + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, divide_message_on_fail)

        # !MULTIPLY
        if message.content.startswith('!multiply'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!multiply':
                if len(message_arguments) > 2:
                    arguments = message_arguments[1:]
                    try:
                        numbers = [float(i) for i in arguments]
                    except ValueError:  # Non number arguments
                        await client.send_message(message.channel, multiply_message_on_fail)
                    else:  # OK
                        result = zero_strip(functools.reduce(operator.mul, numbers))
                        await client.send_message(message.channel,
                                                  ' * '.join(arguments) + ' = ' + '**' + str(result) + '**')
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, multiply_message_on_fail)

        # !8BALL
        if message.content.startswith('!8ball'):
            message_arguments = message.content.split()
            if message_arguments[0] == '!8ball':
                if len(message_arguments) > 1:  # OK
                    answer = random.randint(0, len(eight_ball_answers) - 1)
                    if answer <= 9:  # Affirmative answer
                        emoji = eight_ball_emojis[0]
                    elif answer <= 14:  # Meh answer
                        emoji = eight_ball_emojis[1]
                    else:  # Negative answer
                        emoji = eight_ball_emojis[2]
                    await client.send_message(message.channel,
                                              '`' + ' '.join(message_arguments[1:]) +
                                              '`: ' + eight_ball_answers[answer] + ' ' + emoji)
                else:  # Wrong number of parameters
                    await client.send_message(message.channel, eight_ball_message_on_fail)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Discord Bot')
    parser.add_argument('token', help='Bot token')
    parser = parser.parse_args()

    client.run(parser.token)

# TODO setup logging (log command calls, etc)
# TODO functions and stuff.. too much repetitive code now...
