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

    # DISAPPROVALFACE
    @commands.command(name='disapprovalface', ignore_extra=False, aliases=['disapproval'], pass_context=True)
    async def command_disapprovalface(self, context):
        """ಠ_ಠ

        disapproval emoji."""
        await self.bot.say('ಠ_ಠ')

    # DEVIOUSFACE
    @commands.command(name='deviousface', ignore_extra=False, aliases=['devious'], pass_context=True)
    async def command_deviousface(self, context):
        """ಠ‿ಠ

        devious face emoji."""
        await self.bot.say('ಠ‿ಠ')

    # CUTEFACE
    @commands.command(name='cute', ignore_extra=False, aliases=['cuteface'], pass_context=True)
    async def command_cuteface(self, context):
        """(｡◕‿◕｡)

        cute face emoji."""
        await self.bot.say('(｡◕‿◕｡)')

    # ANGRYFACE
    @commands.command(name='angry', ignore_extra=False, aliases=['angryface'], pass_context=True)
    async def command_angryface(self, context):
        """(╬ ಠ益ಠ)

        angry face emoji."""
        await self.bot.say('(╬ ಠ益ಠ)')

    # CRYINGFACE
    @commands.command(name='cryingface', ignore_extra=False, aliases=['crying'], pass_context=True)
    async def command_cryingface(self, context):
        """ಥ_ಥ

        crying face emoji."""
        await self.bot.say('ಥ_ಥ')

    # INLOVE
    @commands.command(name='inlove', ignore_extra=False, pass_context=True)
    async def command_inlove(self, context):
        """(っ´ω`c)♡

        in love emoji."""
        await self.bot.say('(っ´ω`c)♡')

    # LOL
    @commands.command(name='lol', ignore_extra=False, pass_context=True)
    async def command_lol(self, context):
        """L(° O °L)

        lol emoji."""
        await self.bot.say('L(° O °L)')

    # FINN
    @commands.command(name='finn', ignore_extra=False, pass_context=True)
    async def command_finn(self, context):
        """| (• ◡•)|

        finn emoji."""
        await self.bot.say('| (• ◡•)|')

    # JAKE
    @commands.command(name='jake', ignore_extra=False, pass_context=True)
    async def command_jake(self, context):
        """(❍ᴥ❍ʋ)

        jake emoji."""
        await self.bot.say('(❍ᴥ❍ʋ)')

    ################
    # ERROR HANDLING
    ################

    @command_tableflip.error
    @command_tableunflip.error
    @command_shrug.error
    @command_disapprovalface.error
    @command_deviousface.error
    @command_cuteface.error
    @command_angryface.error
    @command_cryingface.error
    @command_inlove.error
    @command_lol.error
    @command_finn.error
    @command_jake.error
    async def tableflip_tableunflip_shrug_on_error(self, error, context):
        bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.MissingRequiredArgument, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))


# TODO more emojis
