#!python3
# coding: utf-8


"""
XKCD webcomic Commands
"""


import aiohttp
import discord
import xkcd_wrapper
from discord.ext import commands
from DiscordBot.Services import Converters
from DiscordBot.BaseCog import Cog


class Xkcd(Cog):
    """
    Commands that deal with XKCD webcomics
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = '🗨️'
        self.xkcd_api_client = xkcd_wrapper.AsyncClient()

    def embed_comic(self, xkcd_comic, colour=None):
        """
        Creates the embed object to be sent by the bot

        Parameters
        ----------
        xkcd_comic: xkcd_wrapper.Comic
        colour: int
            an int or hex representing a valid colour (optional)

        Returns
        -------
        discord.Embed
        """
        if colour is None:
            colour = self.embed_colour
        comic = discord.Embed(colour=colour)
        comic.set_author(name=f'xkcd #{xkcd_comic.id}: {xkcd_comic.title}',
                         url=f'https://xkcd.com/{xkcd_comic.id}',
                         icon_url='https://xkcd.com/s/0b7742.png')
        comic.set_image(url=xkcd_comic.image_url)
        comic.set_footer(text=xkcd_comic.description)
        return comic

    ##########
    # COMMANDS
    ##########

    # XKCD
    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True)
    async def command_xkcd(self, context):
        """
        Retrieves a random xkcd comic from xkcd.com
        """
        random_comic = await self.xkcd_api_client.random(raw_comic_image=False)
        embed_comic = self.embed_comic(random_comic)
        await context.send(embed=embed_comic)

    # XKCD LATEST
    @command_xkcd.command(name='latest', ignore_extra=False, aliases=['l', '-l', 'last'])
    async def command_xkcd_latest(self, context):
        """
        Retrieves the latest xkcd comic from xkcd.com
        """
        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)

    # XKCD ID
    @command_xkcd.command(name='id', ignore_extra=False, aliases=['n', '-n', 'number'])
    async def command_xkcd_id(self, context, comic_id: Converters.positive_int):
        """
        Retrieves the selected xkcd comic from xkcd.com
        """
        comic = await self.xkcd_api_client.get(comic_id, raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)

    ################
    # ERROR HANDLING
    ################

    @command_xkcd.error
    @command_xkcd_latest.error
    @command_xkcd_id.error
    async def xkcd_xkcd_latest_xkcd_id_on_error(self, context, error):
        """
        Handles errors for all xkcd commands

        Parameters
        ----------
        context: commands.Context
        error: commands.CommandError
        """
        bot_message_id_not_found = 'An xkcd comic with the given `id` was not found'
        bot_message_xkcd_unavailable = 'Can\'t reach xkcd.com right now'
        bot_message_bad_xkcd_response = 'Got a bad response from xkcd.com'

        if context.command.callback is self.command_xkcd.callback:
            bot_message = '`{0}{1}` either takes no arguments or takes one subcommand ' \
                          '(use `{0}help {1}` for more information)'.format(context.prefix,
                                                                            context.invoked_with)
        elif context.command.callback is self.command_xkcd_latest.callback:
            bot_message = f'`{context.prefix}{context.command.qualified_name}` takes no arguments'
        else:
            bot_message = f'`{context.prefix}{context.command.qualified_name}` takes exactly 1 ' \
                          'positive number as argument'

        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (commands.MissingRequiredArgument, bot_message))

        if isinstance(error, commands.CommandInvokeError):
            self.logger.info(f'{error.original.__class__.__name__} exception in command '
                             f'{context.command.qualified_name}: {context.message.content}')

            if isinstance(error.original, xkcd_wrapper.exceptions.HttpError):
                if error.original.status_code == 404:
                    await context.send(bot_message_id_not_found)
                else:
                    await context.send(bot_message_xkcd_unavailable)

            elif isinstance(error.original, xkcd_wrapper.exceptions.BadResponseField):
                await context.send(bot_message_bad_xkcd_response)

            elif isinstance(
                    error.original,
                    (aiohttp.ClientResponseError, aiohttp.ClientConnectionError)):
                await context.send(bot_message_xkcd_unavailable)
