#!python3
# coding: utf-8


"""
Info Commands.
"""


import discord
from discord.ext import commands
from DiscordBot.BaseCog import Cog


class Info(Cog):
    """Info Commands"""

    def __init__(self, bot):
        super().__init__(bot)
        self.help_order = float('inf')  # last cog in !help command output

    @staticmethod
    def add_subcommands(command_object, string_before, base_string):
        """
        add subcommands, if there are any

        Parameters
        ----------
        command_object: commands.core.Command
            command to check for subcommands
        string_before: str
            string to be inserted before everything
        base_string: str
            string to be repeated for each subcommand found (must have two '%s')

        Returns
        -------
        str
            String with subcommands of command_object
        """
        if command_object.enabled:
            commands_listing = ''
            if isinstance(command_object, commands.core.Group):
                commands_listing += string_before
                command_set = set()
                for subcommand in command_object.walk_commands():
                    if subcommand not in command_set:
                        commands_listing += base_string % (subcommand.name, subcommand.short_doc)
                    command_set.add(subcommand)
            return commands_listing
        return ''

    ##########
    # COMMANDS
    ##########

    # INFO
    @commands.command(name='info', ignore_extra=False)
    async def command_info(self, context):
        """Shows author, github page and framework."""
        embed_info = discord.Embed(colour=self.embed_colour)
        embed_info.add_field(name='Author',
                             value='[Kronopt](https://github.com/Kronopt)\n\u200b',
                             inline=False)
        embed_info.add_field(name='Framework',
                             value='[discord.py](https://github.com/Rapptz/discord.py)\n\u200b',
                             inline=False)
        embed_info.add_field(name='Github',
                             value='https://github.com/Kronopt/DiscordBot\n\u200b',
                             inline=False)

        await context.send(embed=embed_info)

    # HELP
    @commands.command(name='help', ignore_extra=False)
    async def command_help(self, context, *command):
        """Shows all commands or info on a command.

        Call without arguments to show all commands.
        Pass a command name (and possible subcommands) as argument for more detailed information
        on that command."""
        bot_prefix = self.bot.command_prefix_simple

        if len(command) == 0:  # show all commands
            title = 'Commands can be called as follows:'
            description = '\n```{0}{1}``````@Bot {1}```\n'.format(bot_prefix, '<command> [subcommands] [arguments]')
            description += 'Subcommands are indented following their respective parent command.\n\n'
            description += 'Some commands have aliases (ex: !8ball can also be called as !eightball or !8b).\n '
            description += 'Type `!help <command> <subcommand>` to know more.\n\n\n\u200b'
            description += '**COMMANDS**:'

            embed_help = discord.Embed(title=title,
                                       description=description,
                                       colour=self.embed_colour)

            sorted_cogs = sorted(Cog.all_commands.items(), key=lambda x: x[0])
            for cog_object, cog_commands in sorted_cogs:
                commands_listing = ''

                # Command Groups
                for command_object in cog_commands.values():
                    # not a subcommand and enabled
                    if command_object.parent is None and command_object.enabled:
                        commands_listing += '%s%s \u200b : \u200b %s\n' % (bot_prefix,
                                                                           command_object.name,
                                                                           command_object.short_doc)
                        commands_listing += self.add_subcommands(
                            command_object, '',
                            '\u200b . \u200b \u200b \u200b %s \u200b : \u200b %s\n')

                commands_listing += '\n\u200b'  # separates fields a bit
                embed_help.add_field(name=cog_object.name + ':', value=commands_listing)

            await context.send(embed=embed_help)

        else:  # show info on a command
            main_command_name = command[0].lower()
            subcommands = command[1:] if len(command) > 1 else []

            # check if argument is an existing command (plus aliases) (not subcommand)
            found_command = None
            for cog_commands in Cog.all_commands.values():
                if found_command:
                    break

                for command_object in cog_commands.values():
                    if ((main_command_name == command_object.name.lower() or main_command_name in
                         [alias.lower() for alias in command_object.aliases]) and
                            command_object.parent is None):
                        found_command = command_object
                        break

            if not found_command:  # argument is not a command
                await context.send('`%s` is not a command or is disabled.' % command[0])
                return
            elif not found_command.enabled:  # argument is a command but is disabled
                await context.send('`%s` is not a command or is disabled.' % command[0])
                return

            else:  # argument is a command and is enabled
                current_command = found_command
                for subcommand in subcommands:  # verify if subcommands are valid
                    if isinstance(current_command, commands.core.Group) and subcommand in current_command.commands:
                        current_command = current_command.commands[subcommand]
                    else:  # argument is not a subcommand
                        await context.send('`%s` is not a subcommand of %s.' % (subcommand, current_command.name))
                        return

                # aliases
                if len(current_command.aliases) == 0:
                    title = '%s%s' % (bot_prefix, current_command.qualified_name)
                else:
                    command_parent = current_command.full_parent_name + ' ' if current_command.full_parent_name else ''
                    title = '%s%s[%s | %s] ' % (bot_prefix, command_parent, current_command.name,
                                                ' | '.join(current_command.aliases))

                # arguments (logic retrieved from HelpFormatter.get_command_signature()
                arguments = current_command.clean_params
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

                description = current_command.help
                description += self.add_subcommands(current_command, '\n\n**subcommands:**\n',
                                                    '%s \u200b : \u200b %s\n')

                embed_help_command = discord.Embed(title=title,
                                                   description=description,
                                                   colour=self.embed_colour)

                await context.send(embed=embed_help_command)

    ################
    # ERROR HANDLING
    ################

    @command_info.error
    @command_help.error
    async def info_help_on_error(self, error, context):
        if context.command.callback is self.command_info.callback:
            bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.invoked_with)
        else:
            bot_message = '`%s%s` takes either no arguments or a command (and possible subcommands).'\
                          % (context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.MissingRequiredArgument, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))
