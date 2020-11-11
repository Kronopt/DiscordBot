#!python3
# coding: utf-8


"""
Help Command
"""


import discord


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

