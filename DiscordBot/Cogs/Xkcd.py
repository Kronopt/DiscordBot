#!python3
# coding: utf-8


"""
XKCD comic Commands.
"""


import random
import beckett.exceptions
import discord
from discord.ext import commands
from beckett.clients import BaseClient
from beckett.resources import BaseResource
from .BaseCog import Cog
from DiscordBot import Converters


class Xkcd(Cog):
    """xkcd comic commands"""

    def __init__(self, bot):
        super().__init__(bot)
        self.xkcd_api_client = XkcdClient()

    def embed_comic(self, xkcd_comic, colour=None):
        """
        Creates the embed object to be sent by the bot.

        Parameters
        ----------
        Creates the embed object to be sent by the bot.

        xkcd_comic: XkcdComic
            XkcdComic object
        colour: int
            an int or hex representing a valid colour (optional)

        Returns
        -------
        discord.Embed
        """
        if colour is None:
            colour = self.embed_colour
        comic = discord.Embed(colour=colour)
        comic.set_author(name='xkcd #%s: %s' % (xkcd_comic.num, xkcd_comic.safe_title),
                         url='https://xkcd.com/%s' % xkcd_comic.num)
        comic.set_image(url=xkcd_comic.img)
        comic.set_footer(text=xkcd_comic.alt)
        return comic

    ##########
    # COMMANDS
    ##########

    # XKCD
    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True, pass_context=True)
    async def command_xkcd(self, context):
        """Retrieves a random xkcd comic from xkcd.com."""

        # get the latest comic number and generate a number between 1 and that number
        latest_comic_number = self.xkcd_api_client.get_comic(uid=-1)[0].num
        random_comic_number = random.randint(1, latest_comic_number)

        # retrieve the random comic
        random_comic = self.xkcd_api_client.get_comic(uid=random_comic_number)[0]

        embed_comic = self.embed_comic(random_comic)
        await self.bot.say(embed=embed_comic)

    # XKCD LATEST
    @command_xkcd.command(name='latest', ignore_extra=False, aliases=['l', '-l', 'last'], pass_context=True)
    async def command_xkcd_latest(self, context):
        """Retrieves the latest xkcd comic from xkcd.com."""

        comic = self.xkcd_api_client.get_comic(uid=-1)[0]
        embed_comic = self.embed_comic(comic)
        await self.bot.say(embed=embed_comic)

    # XKCD ID
    @command_xkcd.command(name='id', ignore_extra=False, aliases=['n', '-n', 'number'], pass_context=True)
    async def command_xkcd_id(self, context, comic_id: Converters.positive_int):
        """Retrieves the selected xkcd comic from xkcd.com."""

        comic = self.xkcd_api_client.get_comic(uid=comic_id)[0]
        embed_comic = self.embed_comic(comic)
        await self.bot.say(embed=embed_comic)

    ################
    # ERROR HANDLING
    ################

    @command_xkcd.error
    @command_xkcd_latest.error
    @command_xkcd_id.error
    async def xkcd_xkcd_latest_xkcd_id_on_error(self, error, context):
        if context.command.callback is self.command_xkcd.callback:
            bot_message = '`{0}{1}` takes no arguments or one of the predefined ones (use `{0}help {1}` for more ' \
                          'information).'.format(context.prefix, context.invoked_with)
        elif context.command.callback is self.command_xkcd_latest.callback:
            bot_message = '`%s%s` takes no arguments.' % (context.prefix, context.command.qualified_name)
        else:
            bot_message = '`%s%s` takes exactly 1 positive number.' % (context.prefix, context.command.qualified_name)
        bot_message_id_not_found = 'xkcd comic with the given id was not found.'
        bot_message_xkcd_unavailable = 'Can\'t reach xkcd.com at the moment.'
        await self.generic_error_handler(error, context,
                                         (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message),
                                         (commands.MissingRequiredArgument, bot_message))
        if (isinstance(error, commands.CommandInvokeError) and
                isinstance(error.original, beckett.exceptions.InvalidStatusCodeError)):
            self.logger.info('%s exception in command %s: %s',
                             error.original.__class__.__name__, context.command.qualified_name, context.message.content)
            if error.original.status_code == 404:
                await self.bot.say(bot_message_id_not_found)
            else:
                await self.bot.say(bot_message_xkcd_unavailable)


########################
# XKCD API COMMUNICATION
########################


class XkcdComic(BaseResource):
    """XKCD Comic Resource"""
    class Meta(BaseResource.Meta):
        name = 'Comic'
        resource_name = 'info.0.json'
        identifier = 'num'
        attributes = (
            'month',
            'num',  # comic id
            'year',
            'safe_title',
            'transcript',
            'alt',  # descrition
            'img',  # actual image link
            'day'
        )

    @classmethod
    def get_resource_url(cls, resource, base_url):
        """Overwrite to allow base_url/id/resource_name as per xkcd api"""
        url = base_url + '/{}' + resource.Meta.resource_name  # will be formatted in get_url
        return cls._parse_url_and_validate(url)

    @classmethod
    def get_url(cls, url, uid, **kwargs):
        """Overwrite to allow base_url/id/resource_name as per xkcd api"""
        if uid == -1:  # latest comic
            url = url.format('')
        else:  # specific comic
            url = url.format(str(uid) + '/')
        return cls._parse_url_and_validate(url)


class XkcdClient(BaseClient):
    class Meta(BaseClient.Meta):
        name = 'XKCD Comic API'
        base_url = 'https://xkcd.com'
        resources = (
            XkcdComic,
        )
