#!python3
# coding: utf-8

"""
The 'Commands' class represents all the commands a bot understands.
Classes inside the 'Commands' class ARE bot commands.

To add a new command create a class inside the Commands class with the following required attributes:
- class attributes:
    - name: str
        command name to be passed by a user to the bot, (ex: ping or 8ball)
    - n_args: None/int >= 0
        how many arguments to expect (None=unlimited and at least 1)
    - args_type: any type
        type to which each detected argument is to be converted to
        OR
        a function in the form of 'f(_, string)' that converts strings to the required type
    - get_message: bool
        True if the original discord.Message class is needed, False otherwise (will be supplied in args[0])
    - message_on_fail: str
        message to be displayed by the bot if command arguments are wrong
- functions:
    - command(*args)
        the actual command function. Should return the message (str) to be delivered by the bot
"""

import functools
import operator
import random
from . import Types


class Commands:

    class Help:
        name = 'help'
        n_args = 0
        args_type = None
        get_message = False
        message_on_fail = '`!help` takes no arguments.'
        help_message = '''Available Commands:\n
`!help` : Bot shows this help message\n
`!ping` : Bot answers with pong\n
`!dice <str dice>` : Bot rolls one of the specified d4, d6, d8, d10, d12 and d20 dices\n
`!random` : Bot generates a number between 0 and 1 (inclusive)\n
`!random_between <int a> <int b>` : Bot generates a number between a and b (inclusive)\n
`!random_from <str a> <str b> ...` : Bot randomly selects one of the space separated arguments\n
`!sum <number a> <number b> ...` : Bot sums all numbers\n
`!subtract <number a> <number b> ...` : Bot subtracts all numbers\n
`!divide <number a> <number b> ...` : Bot divides all numbers\n
`!multiply <number a> <number b> ...` : Bot multiplies all numbers\n
`!8ball <str>` : Bot uses its fortune-telling powers to answer your question'''

        def command(self):
            return self.help_message

    class Ping:
        name = 'ping'
        n_args = 0
        args_type = None
        get_message = False
        message_on_fail = '`!ping` takes no arguments.'

        @staticmethod
        def command():
            return 'pong'

    class Dice:
        name = 'dice'
        n_args = 1
        args_type = Types.Dice
        get_message = False
        dices = Types.Dice.dices
        message_on_fail = '`!dice` takes one of the following arguments: ' + ', '.join(dices) + '.'

        @staticmethod
        def command(*args):
            dice = str(args[0])
            dice_number = int(dice[1:])
            dice_roll = random.randint(1, dice_number)
            return 'Rolled a **' + str(dice_roll) + '** with a ' + dice

    class Random:
        name = 'random'
        n_args = 0
        args_type = None
        get_message = False
        message_on_fail = '`!random` takes no arguments.'

        @staticmethod
        def command():
            random_number = random.random()
            return 'Result: **' + str(random_number) + '**'

    class RandomBetween:
        name = 'random_between'
        n_args = 2
        args_type = int
        get_message = False
        message_on_fail = '`!random_between` takes 2 integers as arguments.'

        @staticmethod
        def command(*args):
            a = args[0]
            b = args[1]
            values = [a, b]
            values.sort()  # Either value can be the smallest one
            a, b = values
            random_number = random.randint(a, b)
            return 'Result: **' + str(random_number) + '**'

    class RandomFrom:
        name = 'random_from'
        n_args = None
        args_type = str
        get_message = False
        message_on_fail = '`!random_from` takes at least 1 argument.'

        @staticmethod
        def command(*args):
            result = random.choice(args)
            return'Result: **' + result + '**'

    class Sum:
        name = 'sum'
        n_args = None
        args_type = Types.Number
        get_message = False
        message_on_fail = '`!sum` takes at least 1 number.'

        def command(self, *args):
            result = self.args_type(functools.reduce(operator.add, args))
            numbers = map(str, args)
            return ' + '.join(numbers) + ' = ' + '**' + str(result) + '**'

    class Subtract:
        name = 'subtract'
        n_args = None
        args_type = Types.Number
        get_message = False
        message_on_fail = '`!subtract` takes at least 1 number.'

        def command(self, *args):
            result = self.args_type(functools.reduce(operator.sub, args))
            numbers = map(str, args)
            return ' - '.join(numbers) + ' = ' + '**' + str(result) + '**'

    class Divide:
        name = 'divide'
        n_args = None
        args_type = Types.Number
        get_message = False
        message_on_fail = '`!divide` takes at least 1 number.'
        divide_by_zero_message_on_fail = '`!divide` can\'t divide by zero.'

        def command(self, *args):
            try:
                result = self.args_type(functools.reduce(operator.truediv, args))
            except ZeroDivisionError:  # Divided by zero
                return self.divide_by_zero_message_on_fail
            else:  # OK
                numbers = map(str, args)
                return ' / '.join(numbers) + ' = ' + '**' + str(result) + '**'

    class Multiply:
        name = 'multiply'
        n_args = None
        args_type = Types.Number
        get_message = False
        message_on_fail = '`!multiply` takes at least 1 number.'

        def command(self, *args):
            result = self.args_type(functools.reduce(operator.mul, args))
            numbers = map(str, args)
            return ' * '.join(numbers) + ' = ' + '**' + str(result) + '**'

    class EightBall:
        name = '8ball'
        n_args = None
        args_type = str
        get_message = False
        message_on_fail = '`!8ball` needs a phrase on which to apply its fortune-telling powers.'
        emojis = [":white_check_mark:", ":low_brightness:", ":x:"]
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                   "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                   "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                   "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                   "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

        def command(self, *args):
            answer = random.randint(0, len(self.answers) - 1)
            if answer <= 9:  # Affirmative answer
                emoji = self.emojis[0]
            elif answer <= 14:  # Meh answer
                emoji = self.emojis[1]
            else:  # Negative answer
                emoji = self.emojis[2]
            return '`' + ' '.join(args) + '`: ' + self.answers[answer] + ' ' + emoji

    class Poll:
        name = 'poll'
        n_args = None
        args_type = str
        get_message = True
        message_on_fail = '`!poll` takes at least 1 argument.'
        message_on_fail_poll_ongoing = 'A poll is already ongoing with the following options: '
        polls = {}  # {channel.id: {poll: [(option, votes)]}}

        def command(self, *args):
            message, *args = args  # args[0] is a discord.Message
            if message.channel.id in self.polls:  # One active poll per channel
                return self.message_on_fail_poll_ongoing + '`' + '`, `'.join(self.polls[message.channel.id]) + '`'
            else:
                self.polls[message.channel.id] = args

            # TODO
            # !poll vote
            # !poll finish
            # ???

            #     votes = {key: list() for key in vote_options}  # dict of poll_option : list_of_users_that_voted
            #     polls[''.join(vote_options)] = votes  # each poll_options combinations is a new distinct poll
            #
            #     await client.send_message(message.channel, message.author.display_name + ' started a poll')
            #     help_string = ''
            #     for option in vote_options:
            #         help_string += '`' + option + '`: ' + str(len(votes[option])) + ' votes'
            #         if len(votes[option]) != 0:
            #             help_string += ' by ' + ', '.join(votes[option]) + '\n'
            #         else:
            #             help_string += '\n'
            #     await client.send_message(message.channel, help_string)
            #
            # else:  # Wrong number of parameters
            #     await client.send_message(message.channel, message_on_fail)
