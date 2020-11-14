#!python3
# coding: utf-8


"""
General Commands.
"""


import random
from discord.ext import commands
from DiscordBot.BaseCog import Cog
from DiscordBot.Services import Converters


class General(Cog):
    """
    General commands that don't fit in other, more specific, categories
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = '🎛️'
        self.greetings = ['Hi', 'Hello', 'Hey', 'Sup', 'What\'s up', 'Greetings', 'Howdy']
        self.greeting_emojis = ['👋', '🤙', '🖖', '🤟', '👊', '🙌']

    ##########
    # COMMANDS
    ##########

    # HI
    @commands.command(name='hi', ignore_extra=False,
                      aliases=['hello', 'hey', 'sup', 'greetings', 'howdy'])
    async def command_hi(self, context):
        """
        Greets user
        """
        greeting = random.choice(self.greetings)
        emoji = random.choice(self.greeting_emojis)
        await context.send(f'{greeting}, {context.author.display_name}! {emoji}')

    # DICE
    @commands.command(name='dice', ignore_extra=False)
    async def command_dice(self, context, *dice: Converters.dice):
        """
        Rolls a die
        Possible dices: `d4`, `d6`, `d8`, `d10`, `d12` and `d20`
        """
        if len(dice) > 1:    # At most one argument
            raise commands.TooManyArguments

        if len(dice) == 0:
            dice = 'd6'  # default
        else:
            dice = dice[0]

        dice_number = int(dice[1:])
        dice_roll = random.randint(1, dice_number)
        await context.send('Rolled a **' + str(dice_roll) + '** with a ' + dice)

    ################
    # ERROR HANDLING
    ################

    @command_hi.error
    @command_dice.error
    async def ping_hi_dice_random_on_error(self, context, error):
        if context.command.callback is self.command_hi.callback:
            bot_message = f'`{context.prefix}{context.invoked_with}` takes no arguments'
        else:
            bot_message = f'`{context.prefix}{context.invoked_with}` either takes no arguments or' \
                          ' one of the following: %s' % (', '.join(Converters.DICES))

        await self.generic_error_handler(
            context, error,
            (commands.MissingRequiredArgument, commands.CommandOnCooldown,
             commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message))
