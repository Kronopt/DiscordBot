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
    @commands.group(name='help', ignore_extra=False, invoke_without_command=True)
    async def command_help(self, *command_name):
        """Shows help message."""
        # I should redo this...
        # It's pretty hacky...
        # It works, I guess...
        if len(command_name) > 1:  # at most one argument
            raise commands.TooManyArguments

        self.log_command_call('help')

        bot_prefix = self.bot.command_prefix_simple

        if len(command_name) == 0:  # show all commands
            title = 'Commands can be called as follows:'
            description = '\n```{0}{1}``````@Bot {1}```\n**COMMANDS**:'.format(
                bot_prefix, '<command> [subcommand] [arguments]')

            embed_help = discord.Embed(title=title, description=description, colour=self.embed_colour)

            for cog_object, cog_commands in Cog.all_commands.items():
                commands_listing = ''

                for command_object in cog_commands.values():
                    # assumes commands are always followed by their subcommands inside the cog class
                    if command_object.parent is not None:
                        prefix = '\t\t'
                    else:
                        prefix = bot_prefix
                    commands_listing += '%s%s\t\t%s\n' % (prefix, command_object.name, command_object.short_doc)

                commands_listing += '\n\u200b'  # separates fields a bit
                embed_help.add_field(name=cog_object.name + ':', value=commands_listing)

            await self.bot.say(embed=embed_help)

        else:  # show info on a command
            command_name = command_name[0].lower()

            # check if argument is an existing command
            found_command = None
            for cog_commands in Cog.all_commands.values():
                if found_command:
                    break

                for command_object in cog_commands.values():
                    if command_name == command_object.name.lower():
                        found_command = command_object
                        break

            if not found_command:  # argument is not a command
                raise commands.BadArgument

            else:  # is a command
                if found_command.parent is not None:  # is subcommand
                    bot_prefix = '%s%s ' % (bot_prefix, found_command.parent)

                # aliases
                if len(found_command.aliases) == 0:
                    title = bot_prefix + found_command.name
                else:
                    title = '%s[%s | %s]' % (bot_prefix, found_command.name, ' | '.join(found_command.aliases))

                description = found_command.help

                # add subcommands, if there are any
                if isinstance(found_command, commands.core.Group):
                    description += '\n\n**subcommands:**\n'

                    command_set = set()
                    for subcommand in found_command.walk_commands():
                        if subcommand not in command_set:
                            description += '%s\t\t%s\n' % (subcommand.name, subcommand.short_doc)
                        command_set.add(subcommand)

                embed_help_command = discord.Embed(title=title, description=description, colour=self.embed_colour)

                await self.bot.say(embed=embed_help_command)

    # HELP <command>
    @command_help.command(name='<command>')
    async def command_help_command(self):
        """Shows help message for a command."""
        # This command only exists to enable the creation of an entry on the help message
        # The logic for this command is included in the !help command
        raise commands.BadArgument
