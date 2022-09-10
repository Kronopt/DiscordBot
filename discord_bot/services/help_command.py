#!python3
# coding: utf-8


"""
Help Command
"""


import collections
import logging
import discord
from discord.ext import commands
from discord_bot.services import command_logging


class Paginator:
    """
    Paginates help messages
    Each page is an individual message embed

    Attributes
    -----------
    max_size: int
        The maximum amount of characters allowed in a page
    """

    def __init__(self, embed_colour):
        self.max_size = 2048
        self.embed_colour = embed_colour
        self._current_page = discord.Embed(colour=self.embed_colour, description="")
        self._pages = []

    @property
    def current_page(self):
        """
        Current message embed description

        Returns
        -------
        str
            current page
        """
        return self._current_page.description if self._current_page.description else ""

    @current_page.setter
    def current_page(self, description):
        """
        Updates current message embed description

        Parameters
        ----------
        description : str
            new description (page)
        """
        self._current_page.description = description

    @property
    def pages(self):
        """
        List of embeds

        Returns
        -------
        list(Embed)
            Rendered list of pages
        """
        if self.current_page != "":
            self.close_page()
        return self._pages

    def clear(self):
        """
        Clears the paginator of all pages
        """
        self.current_page = ""
        self._pages = []

    def add_line(self, line=None, *, empty=False):
        """
        Adds a line to the current page (appends a \n at the end)
        If the line exceeds the max_size limit, an exception is raised

        Parameters
        -----------
        line: str or None
            The line to add
        empty: bool
            Indicates if another empty line should be added

        Raises
        ------
        RuntimeError
            The line was too big for the current max_size
        """
        if line is not None:
            if len(line) + 1 > self.max_size:
                raise RuntimeError(f"Line exceeds maximum page size of {self.max_size}")

            if len(line) + 1 + len(self.current_page) > self.max_size:
                self.close_page()

            self.current_page += line + "\n"

            if empty and len(self.current_page) + 1 <= self.max_size:
                self.current_page += "\n"

    def close_page(self):
        """
        Terminate a page
        """
        self._pages.append(self._current_page)
        self._current_page = discord.Embed(colour=self.embed_colour, description="")

    def __len__(self):
        """
        Total of all characters in all pages
        """
        return sum(len(p.description) for p in self._pages)


class HelpCommand(commands.HelpCommand):
    """
    Help Command
    """

    def __init__(self, embed_colour, **options):
        super().__init__(**options)
        self.command_attrs["help"] = "Shows command help message"
        self.logger = logging.getLogger("discord_bot.Help")
        self.paginator = Paginator(embed_colour=embed_colour)
        self.no_category = collections.namedtuple(
            "NoCategory", ["qualified_name", "emoji"]
        )
        self.command_indent = "  "

    async def send_bot_help(self, mapping):
        """
        Sends help message when the help command is called without arguments

        Parameters
        ----------
        mapping: OrderedDict{Cog/None: List[commands.Command]}
            dictionary of cogs -> list of commands
            commands not associated with a cog (if any) will be in mapping[None]
            Both cogs and commands are ordered by name (None 'cog' is at the end)
        """
        self.format_opening_note()
        self.paginator.add_line("__**Commands**__:", empty=True)

        if None in mapping:
            mapping[self.no_category("No Category", "🤷")] = mapping[None]
            del mapping[None]

        for cog, _commands in mapping.items():
            if len(_commands) > 0:
                self.format_cog_commands(cog, _commands)

        self.format_ending_note()

        await self.send_pages()

    async def send_cog_help(self, cog):
        """
        Sends help message when the help command is called with a Cog as argument

        Parameters
        ----------
        cog: commands.Cog
        """
        self.paginator.add_line(f"**{cog.description}**", empty=True)
        self.format_cog_commands(cog, cog.get_commands())

        await self.send_pages()

    async def send_group_help(self, group):
        """
        Sends help message when the help command is called with a command group as argument
        (a command that has subcommands)

        Parameters
        ----------
        group: commands.Group
        """
        await self.send_command_help(group, True)

    async def send_command_help(self, command, subcommands=False):
        """
        Sends help message when the help command is called with a command as argument

        Parameters
        ----------
        command: commands.Command
        subcommands: bool
            if command has subcommands
        """
        command_signature = self.get_command_signature(command)
        self.paginator.add_line(f"**{command_signature}**", empty=True)
        self.format_command_help_message(command.help)

        if subcommands:
            self.paginator.add_line("__**Subcommands**__:")
            self.paginator.add_line("```")
            self.format_command_and_subcommands(
                command, len(command.qualified_name), False
            )
            self.paginator.add_line("```")

        await self.send_pages()

    async def command_callback(self, ctx, *, command=None):
        """
        Log help command calls
        """
        command_logging.log_command_call(ctx, self.logger, "help")
        await super().command_callback(ctx, command=command)

    async def prepare_help_command(self, ctx, command=None):
        """
        Prepares the help command before it does anything

        Parameters
        ----------
        ctx: commands.Context
        command: str
            argument passed to the help command
        """
        self.paginator.clear()
        await super().prepare_help_command(ctx, command)

    async def send_pages(self):
        """
        Sends the page output from the paginator to the destination
        """
        for page in self.paginator.pages:
            await self.get_destination().send(embed=page)

    async def on_help_command_error(self, ctx, error):
        command_logging.log_command_exception(self.logger, "help")

    def command_not_found(self, command_name):
        """
        Called when help is called for a non-existent command

        Parameters
        ----------
        command_name : str
            invalid command name

        Returns
        -------
        str
            info message to be sent
        """
        return f"Command `{command_name}` not found"

    def subcommand_not_found(self, command, command_name):
        """
        Called when help is called for a subcommand non-existent subcommand

        Parameters
        ----------
        command : commands.Command
            The command that did not have the requested subcommand
        command_name : str
            invalid subcommand name

        Returns
        -------
        str
            info message to be sent
        """
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return (
                f"Command `{command.qualified_name}` has no subcommand `{command_name}`"
            )
        return f"Command `{command.qualified_name}` has no subcommands"

    def get_bot_mapping(self):
        """
        Retrieves bot mapping, which is passed to send_bot_help

        Returns
        -------
        OrderedDict{commands.Cog/None: List[commands.Command]}
        """
        bot = self.context.bot

        mapping = collections.OrderedDict()
        ordered_cogs = sorted(bot.cogs.values(), key=lambda c: c.qualified_name)
        for cog in ordered_cogs:
            mapping[cog] = sorted(cog.get_commands(), key=lambda c: c.name)

        mapping[None] = [c for c in bot.all_commands.values() if c.cog is None]
        return mapping

    def get_command_signature(self, command):
        """
        Retrieves the signature portion of the help page

        Parameters
        ----------
        command : commands.Command
            The command to get the signature of

        Returns
        -------
        str
            Formatted command signature
        """
        parent = command.full_parent_name + " " if command.full_parent_name else ""
        alias = f"{parent}{command.name}"
        if len(command.aliases) > 0:
            aliases = " | ".join(command.aliases)
            alias = f"{parent}[{command.name} | {aliases}]"

        return f"{self.context.clean_prefix}{alias} {command.signature}"

    def format_opening_note(self):
        """
        Formats help message opening note
        """
        prefix_simple = self.context.bot.prefix_simple
        prefix_mention = self.context.bot.user.display_name
        opening_note = (
            f"Commands can be called with the prefix `{prefix_simple}` "
            "or by mentioning the bot. Ex:\n"
            f"> `{prefix_simple}`info\n"
            f"> `@{prefix_mention}` info"
        )

        self.paginator.add_line(opening_note, empty=True)

    def format_ending_note(self):
        """
        Formats help message ending note
        """
        help_command_name = self.invoked_with
        prefix_simple = self.context.bot.prefix_simple
        ending_note = (
            f"For more info on a command use `{prefix_simple}{help_command_name} "
            "[command] [subcommand]`\n"
            f"You can also use `{prefix_simple}{help_command_name} [category]` "
            "for more info on a category"
        )
        self.paginator.add_line(ending_note, empty=True)

    def format_command_help_message(self, command_help):
        """
        Formats command help message

        Parameters
        ----------
        command_help : str or None
            original command help message (command docstring)
        """
        if command_help is not None:
            command_help = command_help.replace("<prefix>", self.context.clean_prefix)
            self.paginator.add_line(command_help, empty=True)

    def format_cog_commands(self, cog, cog_commands):
        """
        Formats a category, its commands and subcommands

        Parameters
        ----------
        cog : discord_bot.base_cog.Cog or self.no_category
        cog_commands: List[commands.Command]
        """
        if cog_commands:
            self.format_cog_header(cog)
            self.paginator.add_line("```")

            max_size = self.get_max_size(cog_commands)
            for command in cog_commands:
                self.format_command_and_subcommands(command, max_size)

            self.paginator.add_line("```")

    def format_cog_header(self, cog):
        """
        Formats the cog name header for a category section of the help output

        Parameters
        ----------
        cog : discord_bot.base_cog.Cog
        """
        self.paginator.add_line(f"{cog.emoji} __**{cog.qualified_name}**__")

    def format_command_and_subcommands(
        self, command, max_size, show_main=True, prefix_spacer_size=0
    ):
        """
        Formats a command and all its subcommands, recursively

        Parameters
        ----------
        command: commands.Command or commands.Group
        max_size: int
            size of biggest command in the group (for indenting purposes)
        show_main: bool
            if main command name and description should be shown or not
        prefix_spacer_size: int
            size of spacer before command/subcommand name
        """
        if show_main:
            prefix = self.command_indent * prefix_spacer_size
            self.format_single_command(command, max_size, prefix)
        else:
            prefix_spacer_size -= 1

        if isinstance(command, commands.Group):
            ordered_subcommands = sorted(
                command.commands, key=lambda c: c.qualified_name
            )
            for subcommand in ordered_subcommands:
                max_size = self.get_max_size(command.commands)
                self.format_command_and_subcommands(
                    subcommand, max_size, True, prefix_spacer_size + 1
                )

    def format_single_command(
        self, command, max_size=None, starting_spacer="", spacer=None
    ):
        """
        Formats a single command.
        Name and description

        Parameters
        ----------
        command: commands.Command
        max_size: int
            size of biggest command in the group
        starting_spacer: str
            spacer command name
        spacer: str
            space between command name and description
        """
        max_size = max_size if max_size is not None else len(command.name)
        spacer = spacer if spacer is not None else self.command_indent
        indent = " " * (max_size - len(command.name)) + spacer
        line = self.handle_line_size(
            f"{starting_spacer}{command.name}{indent}{command.short_doc}",
            " " * max_size + spacer,
        )
        self.paginator.add_line(line)

    @staticmethod
    def handle_line_size(line, spacer, char_number=61):
        """
        Divides a line in multiple lines given the number of characters per line

        Parameters
        ----------
        line: str
            line to be divided
        spacer: str
            space prefix added to the beginning of each additional line
        char_number: int
            number of characters per line

        Returns
        -------
        str
            line divided in multiple lines
        """
        if len(line) <= char_number:
            return line

        new_line = line[:char_number] + "\n"
        line = line[char_number:]

        still_line = True
        while still_line:
            if len(line) > char_number:
                new_line += spacer + line[: char_number - len(spacer)] + "\n"
                line = line[char_number - len(spacer) :]
            else:
                new_line += spacer + line[: char_number - len(spacer)]
                still_line = False

        return new_line
