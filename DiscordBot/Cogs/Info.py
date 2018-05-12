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

    @staticmethod
    def add_subcommands(command_object, string_before, base_string):
        """
        add subcommands, if there are any

        Args:
            command_object: commands.core.Command
                command to check for subcommands
            string_before: str
                string to be inserted before everything
            base_string: str
                string to be repeated for each subcommand found (must have two '%s')

        Returns: str
            String with subcommands of command_object
        """
        commands_listing = ''
        if isinstance(command_object, commands.core.Group):
            commands_listing += string_before
            command_set = set()
            for subcommand in command_object.walk_commands():
                if subcommand not in command_set:
                    commands_listing += base_string % (subcommand.name, subcommand.short_doc)
                command_set.add(subcommand)
        return commands_listing

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
    @commands.command(name='help', ignore_extra=False)
    async def command_help(self, *command):
        """Shows all commands or info on a command.

        Call without arguments to show all commands.
        Pass a command name (and possible subcommands) as argument for more detailed information on that command."""
        self.log_command_call('help')

        bot_prefix = self.bot.command_prefix_simple

        if len(command) == 0:  # show all commands
            title = 'Commands can be called as follows:'
            description = '\n```{0}{1}``````@Bot {1}```\n**COMMANDS**:'.format(
                bot_prefix, '<command> [subcommand] [arguments]')

            embed_help = discord.Embed(title=title, description=description, colour=self.embed_colour)

            for cog_object, cog_commands in Cog.all_commands.items():
                commands_listing = ''

                # Command Groups
                for command_object in cog_commands.values():
                    if command_object.parent is None:  # not a subcommand
                        commands_listing += '%s%s\t\t%s\n' % (bot_prefix, command_object.name, command_object.short_doc)
                        commands_listing += self.add_subcommands(command_object, '', '\t\t%s\t\t%s\n')

                commands_listing += '\n\u200b'  # separates fields a bit
                embed_help.add_field(name=cog_object.name + ':', value=commands_listing)

            await self.bot.say(embed=embed_help)

        else:  # show info on a command
            main_command_name = command[0].lower()

            # check if argument is an existing command (plus aliases)
            found_command = None
            for cog_commands in Cog.all_commands.values():
                if found_command:
                    break

                for command_object in cog_commands.values():
                    if (main_command_name == command_object.name.lower() or
                            main_command_name in [alias.lower() for alias in command_object.aliases]):
                        found_command = command_object
                        break

            if not found_command:  # argument is not a command
                raise commands.BadArgument

            # argument is a command
            else:
                # TODO be able to do '!help random between' instead of the current '!help between'...
                # TODO should be done in this else statement
                if found_command.parent is not None:  # is subcommand
                    bot_prefix = '%s%s ' % (bot_prefix, found_command.parent)

                # aliases
                if len(found_command.aliases) == 0:
                    title = '%s%s' % (bot_prefix, found_command.name)
                else:
                    title = '%s[%s | %s]' % (bot_prefix, found_command.name, ' | '.join(found_command.aliases))

                # arguments (logic retrieved from HelpFormatter.get_command_signature()
                arguments = found_command.clean_params
                if len(arguments) > 0:
                    for argument_name, argument in arguments.items():
                        title += ' '
                        if argument.default is not argument.empty:
                            should_print = argument.default if isinstance(argument.default,
                                                                          str) else argument.default is not None
                            if should_print:
                                title += '[%s=%s]' % (argument_name, argument.default)
                            else:
                                title += '[%s]' % argument_name
                        elif argument.kind == argument.VAR_POSITIONAL:
                            title += '[%s...]' % argument_name
                        else:
                            title += '<%s>' % argument_name

                description = found_command.help
                description += self.add_subcommands(found_command, '\n\n**subcommands:**\n', '%s\t\t%s\n')

                embed_help_command = discord.Embed(title=title, description=description, colour=self.embed_colour)

                await self.bot.say(embed=embed_help_command)
