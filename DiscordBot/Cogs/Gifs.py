#!python3
# coding: utf-8


"""
Gif Commands.
Each bot command is decorated with a @command decorator.
"""


import discord
from discord.ext import commands
from .BaseCog import Cog


# TODO maybe use Giphy API if this gets rate limited
# TODO more gifs


class Gifs(Cog):
    """Gifs"""

    def __init__(self, bot):
        super(Gifs, self).__init__(bot)

    @staticmethod
    def embed_gif(gif_url, footer_message=discord.Embed.Empty, colour=0xe74c3c):
        """
        Creates the embed object to be sent by the bot.

        :param gif_url: str
            url of the gif
        :param footer_message: str
            message to show at the bottom of the gif (optional)
        :param colour: str
            colour string
        :return: discord.Embed
        """
        gif = discord.Embed(colour=colour)
        gif.set_image(url=gif_url)
        gif.set_footer(text=footer_message)
        return gif

    # RICKROLL
    @commands.command(name='rickroll', ignore_extra=False, aliases=['rr'])
    async def command_rickroll(self):
        """Never gonna give you up."""
        self.log_command_call('rickroll')

        gif = self.embed_gif('https://media.giphy.com/media/LXONhtCmN32YU/giphy.gif',
                             footer_message='You\'ve been rick rolled')
        await self.bot.say(embed=gif)

    # OHGODNO
    @commands.command(name='ohgodno', ignore_extra=False, aliases=['godno'])
    async def command_ohgodno(self):
        """Oh god no (The Office)."""
        self.log_command_call('ohgodno')

        gif = self.embed_gif('https://media.giphy.com/media/12XMGIWtrHBl5e/giphy.gif',
                             footer_message='Noooooooooooooooooooooooooo')
        await self.bot.say(embed=gif)

    # REKT
    @commands.command(name='rekt', ignore_extra=False)
    async def command_rekt(self):
        """Rekt."""
        self.log_command_call('rekt')

        gif = self.embed_gif('https://media.giphy.com/media/11yKQ9fN3c06fC/giphy.gif',
                             footer_message='rekt')
        await self.bot.say(embed=gif)
