#!python3
# coding: utf-8


"""
Ascii emojis Commands.
"""


from discord.ext import commands
from .BaseCog import Cog


class AsciiEmojis(Cog):
    """Ascii based emojis"""

    def __init__(self, bot):
        super().__init__(bot)

    ##########
    # COMMANDS
    ##########

    # TABLEFLIP
    @commands.command(name='tableflip', ignore_extra=False, aliases=['tf', 'flip'], pass_context=True)
    async def command_tableflip(self, context):
        """(╯°□°）╯︵ ┻━┻

        tableflip emoji."""
        await self.bot.say('(╯°□°）╯︵ ┻━┻')  # Discord already has this emoji implemented

    # TABLEUNFLIP
    @commands.command(name='tableunflip', ignore_extra=False, aliases=['tuf', 'unflip'], pass_context=True)
    async def command_tableunflip(self, context):
        """┬─┬ ノ(゜-゜ノ)

        tableunflip emoji."""
        await self.bot.say('┬─┬ ノ( ゜-゜ノ)')  # Discord already has this emoji implemented

    # SHRUG
    @commands.command(name='shrug', ignore_extra=False, pass_context=True)
    async def command_shrug(self, context):
        """¯\_(ツ)_/¯

        shrug emoji."""
        await self.bot.say('¯\_(ツ)_/¯')  # Discord already has this emoji implemented

    ################
    # ERROR HANDLING
    ################

    @command_tableflip.error
    @command_tableunflip.error
    @command_shrug.error
    async def tableflip_tableunflip_shrug_on_error(self, error, context):
        bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.MissingRequiredArgument, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))


# TODO more emojis
