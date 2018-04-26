#!python3
# coding: utf-8


"""
Info Commands.
"""


import discord
from discord.ext import commands
from .BaseCog import Cog


class Info(Cog):
    """Info Commands"""

    def __init__(self, bot):
        super().__init__(bot)

    # INFO
    @commands.command(name='info', ignore_extra=False)
    async def command_info(self):
        """Shows author, github page and framework."""
        self.log_command_call('info')

        bot_info = await self.bot.application_info()
        bot_owner = bot_info.owner.display_name + '#' + str(bot_info.owner.discriminator)

        embed_info = discord.Embed(colour=self.embed_colour)
        embed_info.add_field(name='Author', value=bot_owner, inline=False)
        embed_info.add_field(name='Framework', value='[discord.py](https://github.com/Rapptz/discord.py)', inline=False)
        embed_info.add_field(name='Github', value='https://github.com/Kronopt/DiscordBot', inline=False)

        await self.bot.say(embed=embed_info)

    # HELP
    @commands.group(name='help', ignore_extra=False)
    async def command_help(self):
        """Shows help message."""
        self.log_command_call('help')

        bot_prefix = self.bot.command_prefix_simple
        title = 'Commands can be called as follows:'
        description = '\n```{0}{1}``````@Bot {1}```\n**COMMANDS**:'.format(
            bot_prefix, '<command> [subcommand] [arguments]')

        embed_help = discord.Embed(title=title, description=description, colour=self.embed_colour)

        for cog_object, cog_commands in Cog.all_commands.items():
            commands_listing = ''

            for command_object in cog_commands.values():
                command_name = command_object.name

                # assumes commands are always followed by their subcommands inside the cog class
                if command_object.parent is not None:
                    prefix = '\t\t'
                else:
                    prefix = bot_prefix
                commands_listing += '%s%s\t\t%s\n' % (prefix, command_name, command_object.short_doc)

            commands_listing += '\n\u200b'  # separates fields a bit
            embed_help.add_field(name=cog_object.name + ':', value=commands_listing)

        await self.bot.say(embed=embed_help)

    # TODO '!help <command>' shows detailed info on command (don't forget aliases)
    # TODO '!help <command group>' shows info on command group and associated commands

    # TODO in the end delete the HelpFormatter.py


# TODO add Cog to BOT in DiscordBot.py
# TODO add errors in ErrorMessages.py
