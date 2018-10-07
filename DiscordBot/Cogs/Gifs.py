#!python3
# coding: utf-8


"""
Gif Commands.
"""


import discord
from discord.ext import commands
from DiscordBot.BaseCog import Cog


class Gifs(Cog):
    """Gifs"""

    def __init__(self, bot):
        super().__init__(bot)

    def embed_gif(self, gif_url, footer_message=discord.Embed.Empty, colour=None):
        """
        Creates the embed object to be sent by the bot.

        Parameters
        ----------
        gif_url: str
            url of the gif
        footer_message: str
            message to show at the bottom of the gif (optional)
        colour: int
            an int or hex representing a valid colour (optional)

        Returns
        -------
        discord.Embed
        """
        if colour is None:
            colour = self.embed_colour
        gif = discord.Embed(colour=colour)
        gif.set_image(url=gif_url)
        gif.set_footer(text=footer_message)
        return gif

    ##########
    # COMMANDS
    ##########

    # RICKROLL
    @commands.command(name='rickroll', ignore_extra=False, aliases=['rr'], pass_context=True)
    async def command_rickroll(self, context):
        """Never gonna give you up."""
        gif = self.embed_gif('https://media.giphy.com/media/LXONhtCmN32YU/giphy.gif',
                             footer_message='You\'ve been rick rolled')
        await self.bot.say(embed=gif)

    # OHGODNO
    @commands.command(name='ohgodno', ignore_extra=False, aliases=['godno'], pass_context=True)
    async def command_ohgodno(self, context):
        """Oh god no (The Office)."""
        gif = self.embed_gif('https://media.giphy.com/media/12XMGIWtrHBl5e/giphy.gif',
                             footer_message='Noooooooooooooooooooooooooo')
        await self.bot.say(embed=gif)

    # REKT
    @commands.command(name='rekt', ignore_extra=False, pass_context=True)
    async def command_rekt(self, context):
        """Rekt."""
        gif = self.embed_gif('https://media.giphy.com/media/11yKQ9fN3c06fC/giphy.gif',
                             footer_message='rekt')
        await self.bot.say(embed=gif)

    ################
    # ERROR HANDLING
    ################

    @command_rickroll.error
    @command_ohgodno.error
    @command_rekt.error
    async def rickroll_ohgodno_rekt_on_error(self, error, context):
        bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.invoked_with)
        await self.generic_error_handler(error, context,
                                         (commands.MissingRequiredArgument, commands.CommandOnCooldown,
                                          commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))


# TODO maybe use Giphy API if this gets rate limited
# TODO more gifs
