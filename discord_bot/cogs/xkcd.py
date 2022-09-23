#!python3
# coding: utf-8


"""
XKCD webcomic Commands
"""


from typing import TYPE_CHECKING
import aiohttp
import discord
import xkcd_wrapper
from discord import app_commands, Interaction
from discord_bot.services import transformers
from discord_bot.base_cog import Cog

if TYPE_CHECKING:
    from discord_bot.bot import Bot


class Xkcd(Cog):
    """
    Commands that deal with XKCD webcomics
    """

    xkcd_group = app_commands.Group(name="xkcd", description="XKCD-related commands")

    def __init__(self, bot: "Bot"):
        super().__init__(bot)
        self.emoji = "🗨️"
        self.xkcd_api_client = xkcd_wrapper.AsyncClient()

    def embed_comic(
        self, xkcd_comic: xkcd_wrapper.Comic, colour: int | discord.Colour | None = None
    ) -> discord.Embed:
        """
        Creates the embed object to be sent by the bot

        Parameters
        ----------
        xkcd_comic: xkcd_wrapper.Comic
        colour: int or discord.Colour
            an int or hex representing a valid colour (optional)

        Returns
        -------
        discord.Embed
        """
        if colour is None:
            colour = self.embed_colour
        comic = discord.Embed(colour=colour)
        comic.set_author(
            name=f"xkcd #{xkcd_comic.id}: {xkcd_comic.title}",
            url=f"https://xkcd.com/{xkcd_comic.id}",
            icon_url="https://xkcd.com/s/0b7742.png",
        )
        comic.set_image(url=xkcd_comic.image_url)
        comic.set_footer(text=xkcd_comic.description)
        return comic

    ##########
    # COMMANDS
    ##########

    # XKCD RANDOM
    @xkcd_group.command(name="random")
    async def command_xkcd_random(self, interaction: Interaction):
        """
        Shows a random xkcd comic

        Retrieves a random xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd random`
        """
        random_comic = await self.xkcd_api_client.random(raw_comic_image=False)
        embed_comic = self.embed_comic(random_comic)
        await interaction.response.send_message(embed=embed_comic)

    # XKCD LATEST
    @xkcd_group.command(name="latest")
    async def command_xkcd_latest(self, interaction: Interaction):
        """
        Shows the latest xkcd comic

        Retrieves the latest xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd latest`
        """
        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await interaction.response.send_message(embed=embed_comic)

    # XKCD ID
    @xkcd_group.command(name="id")
    @app_commands.describe(comic_id="XKCD comic ID")
    @app_commands.rename(comic_id="id")
    async def command_xkcd_id(
        self, interaction: Interaction, comic_id: transformers.PositiveInteger
    ):
        """
        Shows the selected xkcd comic

        Retrieves the xkcd webcomic with the specified ID from xkcd.com

        ex:
        `<prefix>xkcd id` 100
        """
        comic = await self.xkcd_api_client.get(comic_id, raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await interaction.response.send_message(embed=embed_comic)

    ################
    # ERROR HANDLING
    ################

    @command_xkcd_random.error
    @command_xkcd_latest.error
    @command_xkcd_id.error
    async def xkcd_xkcd_latest_xkcd_id_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """command_xkcd_random, command_xkcd_latest and command_xkcd_id error handling"""

        bot_message_id_not_found = "An xkcd comic with the given `id` was not found"
        bot_message_xkcd_unavailable = "Can't reach xkcd.com right now"
        bot_message_bad_xkcd_response = "Got a bad response from xkcd.com"

        handled_exceptions = []

        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

            if isinstance(error, xkcd_wrapper.exceptions.HttpError):
                if error.status_code == 404:
                    message = bot_message_id_not_found
                else:
                    message = bot_message_xkcd_unavailable

                handled_exceptions.append(
                    (
                        xkcd_wrapper.exceptions.HttpError,
                        message,
                    )
                )

            elif isinstance(error, xkcd_wrapper.exceptions.BadResponseField):
                handled_exceptions.append(
                    (
                        xkcd_wrapper.exceptions.BadResponseField,
                        bot_message_bad_xkcd_response,
                    )
                )

            elif isinstance(
                error,
                (aiohttp.ClientResponseError, aiohttp.ClientConnectionError),
            ):
                handled_exceptions.extend(
                    (
                        (aiohttp.ClientResponseError, bot_message_xkcd_unavailable),
                        (aiohttp.ClientConnectionError, bot_message_xkcd_unavailable),
                    ),
                )

        await self.generic_error_handler(
            interaction, error, tuple(), *handled_exceptions
        )
