#!python3
# coding: utf-8


"""
Ascii emojis Commands.
Each bot command is decorated with a @command decorator.
"""


from discord.ext import commands
from .BaseCog import Cog


# TODO more emojis


class AsciiEmojis(Cog):
    """Ascii based emojis"""

    def __init__(self, bot):
        super(AsciiEmojis, self).__init__(bot)

    # TABLEFLIP
    @commands.command(name='tableflip', ignore_extra=False, aliases=['tf', 'flip'])
    async def command_tableflip(self):
        """(╯°□°）╯︵ ┻━┻"""
        self.log_command_call('tableflip')

        await self.bot.say('(╯°□°）╯︵ ┻━┻')  # Discord already has this emoji implemented

    # TABLEUNFLIP
    @commands.command(name='tableunflip', ignore_extra=False, aliases=['tuf', 'unflip'])
    async def command_tableunflip(self):
        """┬─┬ ノ(゜-゜ノ)"""
        self.log_command_call('tableunflip')

        await self.bot.say('┬─┬ ノ( ゜-゜ノ)')  # Discord already has this emoji implemented

    # SHRUG
    @commands.command(name='shrug', ignore_extra=False)
    async def command_shrug(self):
        """¯\_(ツ)_/¯"""
        self.log_command_call('shrug')

        await self.bot.say('¯\_(ツ)_/¯')  # Discord already has this emoji implemented