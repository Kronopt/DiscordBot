#!python3
# coding: utf-8


"""
HelpFormatter override.
Changes the way the 'help' command works
"""


import inspect
import itertools
import logging
from discord.ext import commands


class HelpFormat(commands.HelpFormatter):
    """The code is mostly the same as in the original except for a few details:
    - 'No Category' category is now just the 'Help' category.
    - Add subcommands recursively to each command that has them.
    - The ending note is altered"""

    def get_ending_note(self):
        command_name = self.context.invoked_with
        return "Type {0}{1} <command> for more info on a command.\n" \
               "Type {0}{1} <category> for more info on a category.".format(self.clean_prefix, command_name)

    def _add_subcommands_to_page(self, max_width, _commands, recursive_level=1):
        for name, command in _commands:
            if name in command.aliases:
                # skip aliases
                continue

            entry = '{0}{1:<{width}} {2}'.format('   '*recursive_level, name, command.short_doc, width=max_width)
            shortened = self.shorten(entry)
            self._paginator.add_line(shortened)

            if isinstance(command, commands.core.Group) and len(command.commands) != 0:  # add subcommands recursively
                self._add_subcommands_to_page(max_width, command.commands.items(), recursive_level+1)

    def format(self):
        logging.info('command called: help')

        self._paginator = commands.Paginator()

        description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

        if description:  # Description portion
            self._paginator.add_line(description, empty=True)

        if isinstance(self.command, commands.core.Command):
            # Signature portion
            signature = self.get_command_signature()
            self._paginator.add_line(signature, empty=True)

            # Long doc section
            if self.command.help:
                self._paginator.add_line(self.command.help, empty=True)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._paginator.close_page()
                return self._paginator.pages

        max_width = self.max_name_size

        def category(tup):
            cog = tup[1].cog_name
            # zero width space to give it approximate last place sorting position
            return cog + ':' if cog is not None else '\u200bHelp:'

        if self.is_bot():
            data = sorted(self.filter_command_list(), key=category)
            for category, _commands in itertools.groupby(data, key=category):
                _commands = list(_commands)
                if len(_commands) > 0:
                    self._paginator.add_line(category)

                self._add_subcommands_to_page(max_width, _commands)
        else:
            self._paginator.add_line('Commands:')
            self._add_subcommands_to_page(max_width, self.filter_command_list())

        # add ending note
        self._paginator.add_line()
        ending_note = self.get_ending_note()
        self._paginator.add_line(ending_note)
        return self._paginator.pages
