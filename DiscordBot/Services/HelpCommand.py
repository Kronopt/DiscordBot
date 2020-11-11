#!python3
# coding: utf-8


"""
Help Command
"""


import collections
import discord
from discord.ext import commands


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
        self._current_page = discord.Embed(colour=self.embed_colour,
                                           description='')
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
        return self._current_page.description

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
        if self.current_page != '':
            self.close_page()
        return self._pages

    def clear(self):
        """
        Clears the paginator of all pages
        """
        self.current_page = ''
        self._pages = []

    def add_line(self, line='', *, empty=False):
        """
        Adds a line to the current page (appends a \n at the end)
        If the line exceeds the max_size limit, an exception is raised

        Parameters
        -----------
        line: str
            The line to add
        empty: bool
            Indicates if another empty line should be added

        Raises
        ------
        RuntimeError
            The line was too big for the current max_size
        """
        if len(line) + 1 > self.max_size:
            raise RuntimeError(f'Line exceeds maximum page size of {self.max_size}')

        if len(line) + 1 + len(self.current_page) > self.max_size:
            self.close_page()

        self.current_page += line + '\n'

        if empty and len(self.current_page) + 1 <= self.max_size:
            self.current_page += '\n'

    def close_page(self):
        """
        Terminate a page
        """
        self._pages.append(self._current_page)
        self._current_page = discord.Embed(colour=self.embed_colour,
                                           description='')

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
        self.paginator = Paginator(embed_colour=embed_colour)
        self.no_category = collections.namedtuple('NoCategory', ['qualified_name', 'emoji'])

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
        if opening_note := self.opening_note():
            self.paginator.add_line(opening_note, empty=True)

        self.paginator.add_line('__**Commands**__:', empty=True)

        if None in mapping:
            mapping[self.no_category('No Category', '🤷')] = mapping[None]
            del mapping[None]

        for cog, _commands in mapping.items():
            if len(_commands) > 0:
                self.add_bot_commands_formatting(cog, _commands)

        await self.send_pages()

    def command_not_found(self, command_name):
        """
        Called when help is called for a non-existent command
        (overridden)

        Parameters
        ----------
        command_name : str
            invalid command

        Returns
        -------
        str
            info message to be sent
        """
        return f'Command `{command_name}` not found'

    def subcommand_not_found(self, command, command_name):
        """
        Called when help is called for a subcommand non-existent subcommand

        Parameters
        ----------
        command : commands.Command
            The command that did not have the requested subcommand
        command_name : str
            invalid subcommand

        Returns
        -------
        str
            info message to be sent
        """
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f'Command `{command.qualified_name}` has no subcommand `{command_name}`'
        return f'Command `{command.qualified_name}` has no subcommands'

    async def prepare_help_command(self, ctx, command=None):
        """
        Prepares the help command before it does anything
        Parameters
        """
        self.paginator.clear()
        await super().prepare_help_command(ctx, command)

    def get_bot_mapping(self):
        """
        Retrieves bot mapping, which is passed to send_bot_help
        """
        bot = self.context.bot

        mapping = collections.OrderedDict()
        ordered_cogs = sorted(bot.cogs.values(), key=lambda c: c.qualified_name)
        for cog in ordered_cogs:
            mapping[cog] = sorted(cog.get_commands(), key=lambda c: c.name)

        mapping[None] = [c for c in bot.all_commands.values() if c.cog is None]
        return mapping

    async def send_pages(self):
        """
        Sends the page output from the paginator to the destination
        """
        for page in self.paginator.pages:
            await self.get_destination().send(embed=page)

    def opening_note(self):
        """
        Opening note

        Returns
        -------
        str
            The help command opening note
        """
        help_command_name = self.invoked_with
        prefix_simple = self.context.bot.prefix_simple
        prefix_mention = self.context.bot.user.display_name
        return f'Commands can be called with the prefix `{prefix_simple}` ' \
               f'or by mentioning the bot. Ex:\n' \
               f'`{prefix_simple}`info\n' \
               f'`@{prefix_mention}` info\n\n' \
               f'For more info on a command use `{prefix_simple}{help_command_name} ' \
               '[command] [subcommand]`\n' \
               f'You can also use `{prefix_simple}{help_command_name} [category]`' \
               ' for more info on a category'

    def add_bot_commands_formatting(self, cog, _commands):
        """
        Formats categories, commands and subcommands
        """
        if _commands:
            max_size = self.get_max_size(_commands)
            space = '   '
            self.paginator.add_line(f'{cog.emoji} __**{cog.qualified_name}**__')

            self.paginator.add_line('```')
            for command in _commands:
                indent = ' ' * (max_size - len(command.name)) + space
                line = self.handle_line_size(f'{command.name}{indent}{command.short_doc}',
                                             ' ' * max_size + space)
                self.paginator.add_line(line)

                if isinstance(command, commands.Group):
                    max_size_sub = self.get_max_size(command.commands)
                    for subcommand in command.commands:
                        indent = ' ' * (max_size_sub - len(subcommand.name)) + space
                        line = self.handle_line_size(
                            f'{space}{subcommand.name}{indent}{subcommand.short_doc}',
                            ' ' * max_size_sub + space * 2)
                        self.paginator.add_line(line)

            self.paginator.add_line('```')

    @staticmethod
    def handle_line_size(line, prefix_char, char_number=61):
        """
        Divides a line in multiple lines given the number of characters per line

        Parameters
        ----------
        line: str
            line to be divided
        prefix_char: str
            prefix added to the beginning of each new line
        char_number: int
            number of characters per line

        Returns
        -------
        str
            line divided in multiple lines
        """
        if len(line) <= char_number:
            return line

        new_line = line[:char_number] + '\n'
        line = line[char_number:]

        still_line = True
        while still_line:
            if len(line) > char_number:
                new_line += prefix_char + line[:char_number - len(prefix_char)] + '\n'
                line = line[char_number - len(prefix_char):]
            else:
                new_line += prefix_char + line[:char_number - len(prefix_char)]
                still_line = False

        return new_line
