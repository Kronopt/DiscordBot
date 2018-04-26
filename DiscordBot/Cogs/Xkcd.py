#!python3
# coding: utf-8


"""
XKCD comic Commands.
"""


import random
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

    # XKCD
    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True)
    async def command_xkcd(self):
        """Retrieves a random xkcd comic from xkcd.com."""
        self.log_command_call('xkcd')

        # get the latest comic number and generate a number between 1 and that number
        latest_comic_number = self.xkcd_api_client.get_comic(uid=-1)[0].num
        random_comic_number = random.randint(1, latest_comic_number)

        # retrieve the random comic
        random_comic = self.xkcd_api_client.get_comic(uid=random_comic_number)[0]

        embed_comic = self.embed_comic(random_comic)
        await self.bot.say(embed=embed_comic)

    # XKCD LATEST
    @command_xkcd.command(name='latest', ignore_extra=False, aliases=['l', '-l', 'last'])
    async def command_xkcd_latest(self):
        """Retrieves the latest xkcd comic from xkcd.com."""
        self.log_command_call('xkcd latest')

        comic = self.xkcd_api_client.get_comic(uid=-1)[0]
        embed_comic = self.embed_comic(comic)
        await self.bot.say(embed=embed_comic)

    # XKCD ID
    @command_xkcd.command(name='id', ignore_extra=False, aliases=['n', '-n', 'number'])
    async def command_xkcd_id(self, comic_id: Converters.positive_int):
        """Retrieves the selected xkcd comic from xkcd.com."""
        self.log_command_call('xkcd id')

        comic = self.xkcd_api_client.get_comic(uid=comic_id)[0]
        embed_comic = self.embed_comic(comic)
        await self.bot.say(embed=embed_comic)


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
