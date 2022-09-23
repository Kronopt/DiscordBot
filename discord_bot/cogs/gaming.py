#!python3
# coding: utf-8


"""
Gaming related Commands
"""


from typing import TYPE_CHECKING
import asyncio
import urllib
import discord
import pyppeteer
import pyppeteer.errors
from discord import app_commands, Interaction
from discord_bot.base_cog import Cog
from discord_bot.services import (
    awesomenauts_rank,
    external_api_handler,
    is_there_any_deal_api,
)

if TYPE_CHECKING:
    from discord_bot.bot import Bot


class NoBrowserError(Exception):
    """
    Browser is not available
    """

    def __str__(self):
        return "Browser is not available"


class Gaming(Cog):
    """
    Commands that deal with games/gaming (player rank, high scores, characters, etc)
    """

    awesomenauts_group = app_commands.Group(
        name="awesomenauts", description="Awesomenauts-related commands"
    )

    def __init__(self, bot: "Bot"):
        super().__init__(bot)
        self.emoji = "🎮"
        self.browser = None
        self.awesomenauts_rank_url = "https://orikaru.net/nautsrankings#//rank/asc/{}//"
        self.isthereanydeal_base_url = "https://api.isthereanydeal.com"

        headers = {
            "Accept": "application/json",
            "User-Agent": "DiscordBot (https://github.com/Kronopt/DiscordBot)",
        }
        self.isthereanydeal_identifier_api = (
            external_api_handler.APICommunicationHandler(
                api_name="IsThereAnyDeal API, Identifier endpoint",
                base_url=f"{self.isthereanydeal_base_url}/v02/game/plain/?key="
                f'{self.bot.cog_args["isthereanydeal_token"]}',
                headers=headers,
                json_parser=is_there_any_deal_api.IdentifierEndpoint,
                error_parser=is_there_any_deal_api.IsThereAnyDealErrorResponse,
            )
        )
        self.isthereanydeal_game_info_api = (
            external_api_handler.APICommunicationHandler(
                api_name="IsThereAnyDeal API, Get Info About Game endpoint",
                base_url=f"{self.isthereanydeal_base_url}/v01/game/info/?key="
                f'{self.bot.cog_args["isthereanydeal_token"]}',
                headers=headers,
                json_parser=is_there_any_deal_api.GetInfoAboutGameEndpoint,
                error_parser=is_there_any_deal_api.IsThereAnyDealErrorResponse,
            )
        )
        self.isthereanydeal_game_prices_api = (
            external_api_handler.APICommunicationHandler(
                api_name="IsThereAnyDeal API, Get Current Game Prices endpoint",
                base_url=f"{self.isthereanydeal_base_url}/v01/game/prices/?key="
                f'{self.bot.cog_args["isthereanydeal_token"]}&region=eu2&country=PT',
                headers=headers,
                json_parser=is_there_any_deal_api.GetCurrentPricesEndpoint,
                error_parser=is_there_any_deal_api.IsThereAnyDealErrorResponse,
            )
        )
        self.isthereanydeal_historical_price_api = (
            external_api_handler.APICommunicationHandler(
                api_name="IsThereAnyDeal API, Get Historical Price endpoint",
                base_url=f"{self.isthereanydeal_base_url}/v01/game/lowest/?key="
                f'{self.bot.cog_args["isthereanydeal_token"]}&region=eu2&country=PT',
                headers=headers,
                json_parser=is_there_any_deal_api.GetHistoricalLowEndpoint,
                error_parser=is_there_any_deal_api.IsThereAnyDealErrorResponse,
            )
        )

    async def cog_load(self):
        # init browser
        chromium_args = self.bot.cog_args["chromium_args"]
        launcher = pyppeteer.launcher.Launcher({"args": chromium_args})

        # for testing:
        # import os
        # os.system(' '.join(launcher.cmd))

        self.browser = await launcher.launch()

    async def cog_unload(self):
        await self.browser.close()

    async def create_gamedeal_embed(
        self,
        game_info: is_there_any_deal_api.GetInfoAboutGameEndpoint,
        game_prices: is_there_any_deal_api.GetCurrentPricesEndpoint,
        game_historical_low_price: is_there_any_deal_api.GetHistoricalLowEndpoint,
    ) -> discord.Embed:
        """gamedeal embed"""
        embed = discord.Embed(colour=self.embed_colour)

        # game title
        dlc = " (DLC)" if game_info.is_dlc else ""
        embed.set_author(name=game_info.title + dlc, url=game_info.game_itad_url)

        # game prices per store
        embed_value = ""

        if game_prices.shops:
            for shop in game_prices.shops:
                price_current = f"{shop.price_full}{game_prices.currency}"
                if shop.price_percent_discount != 0:
                    price_current = f"~~{price_current}~~"
                    price_cut = (
                        f"{shop.price_discounted}{game_prices.currency} "
                        f"(-{shop.price_percent_discount}%) "
                    )
                else:
                    price_cut = ""

                shop_price_info = (
                    f"{price_current} {price_cut}[{shop.name}]({shop.game_url})\n"
                )

                if (
                    len(embed_value) + len(shop_price_info) < 1024
                ):  # embed.field.value size limit
                    embed_value += shop_price_info
                else:
                    embed.add_field(name="\u200b", value=embed_value, inline=False)
                    embed_value = shop_price_info

            embed.add_field(name="\u200b", value=embed_value, inline=False)

        else:
            embed.description = (
                f"{game_info.title} is currently not available for purchase"
            )

        # historical low price, if any
        if game_historical_low_price.price is not None:
            embed.add_field(
                name="\u200b\nHistorical Low",
                value=f"{game_historical_low_price.store}: "
                f"**{game_historical_low_price.price}{game_prices.currency}**\n"
                f"on {game_historical_low_price.date}",
                inline=True,
            )

        # steam review, if any
        if game_info.steam_review:
            embed.add_field(
                name="\u200b\nSteam Review",
                value=f"**{game_info.steam_review.text}**\n"
                f"({game_info.steam_review.positive_reviews_percent}% of "
                f"{game_info.steam_review.total_reviews} users)",
                inline=True,
            )

        # game image
        if game_info.image_url:
            embed.set_image(url=game_info.image_url)

        # footer info
        embed.set_footer(
            text="source: IsThereAnyDeal.com ❤",
            icon_url="https://d2uym1p5obf9p8.cloudfront.net/images/favicon.png",
        )

        return embed

    ##########
    # COMMANDS
    ##########

    # AWESOMENAUTS RANK
    @awesomenauts_group.command(name="rank")
    @app_commands.describe(player_name="awesomenauts player name")
    @app_commands.rename(player_name="player")
    async def command_awesomenauts_rank(
        self, interaction: Interaction, player_name: str
    ):
        """
        Displays rank information of an Awesomenaut's player

        Matches highest ranked player out of a list of closely named players found
        (ie, retrieves first result obtained from https://orikaru.net/nautsrankings)

        ex:
        `<prefix>awesomenauts rank` niki
        """
        if self.browser is None:
            raise NoBrowserError()

        await interaction.response.send_message(
            f"looking for player `{player_name}` ...", ephemeral=True
        )

        page = await self.browser.newPage()
        await page.goto(
            self.awesomenauts_rank_url.format(urllib.parse.quote(player_name)),
            options={"timeout": 5000},
        )

        # either the list of players is populated or the "no results" message is shown,
        # whatever happens first. forced timeout after 5 seconds
        rank_selector = page.waitForSelector("#leaderboard tbody tr")
        no_result_selector = page.waitForSelector(
            "#content-container #no-result:not(.hidden)"
        )
        _, pending_futures = await asyncio.wait(
            [rank_selector, no_result_selector],
            return_when=asyncio.FIRST_COMPLETED,
            timeout=5,
        )
        for future in pending_futures:
            future.cancel()

        players = await page.querySelectorAll("#leaderboard tbody tr")
        if players:
            player = players[1]  # zeroth element is the header
            text_fields = await player.querySelectorAllEval(
                "td", "(nodes => nodes.map(n => n.innerText))"
            )
            steam_profile = await player.querySelectorEval("td a", "node => node.href")
            img_urls = await player.querySelectorAllEval(
                "td img", "(nodes => nodes.map(n => n.src))"
            )
            img_titles = await player.querySelectorAllEval(
                "td img", "(nodes => nodes.map(n => n.title))"
            )

            awesomenaut_rank = awesomenauts_rank.AwesomenautsRank(
                self.embed_colour,
                {
                    "player_name": text_fields[1].rstrip(),
                    "rank": text_fields[0].rstrip(),
                    "games_played_current_season": text_fields[3].rstrip(),
                    "games_played_all_time": text_fields[4].rstrip(),
                    "win_percentage": text_fields[2].rstrip()[:-1],
                    "rating": text_fields[6].rstrip(),
                    "league": img_titles[0],
                    "league_img_url": img_urls[0],
                    "favourite_naut": img_titles[1],
                    "favourite_naut_img_url": img_urls[1],
                    "country": img_titles[2] if len(img_titles) == 3 else "",
                    "steam_profile_url": steam_profile,
                },
            )

            await interaction.followup.send(embed=awesomenaut_rank.embed)

        else:
            message = await interaction.original_response()
            await message.edit(
                content=f"Can't retrieve player `{player_name}`, "
                + "because he's not on the leaderboard"
            )

        await page.close()

    # GAMEDEAL
    @app_commands.command(name="gamedeal")
    @app_commands.describe(game_name="name of game to search for deals")
    @app_commands.rename(game_name="name")
    async def command_gamedeal(self, interaction: Interaction, game_name: str):
        """
        Displays game pricing info

        Info pertains to all stores in which the game is available for purchase

        ex:
        `<prefix>gamedeal` "Assassin's Creed Odyssey"
        """
        game_name_quoted = urllib.parse.quote(game_name)

        game = await self.isthereanydeal_identifier_api.call_api(
            f"&title={game_name_quoted}"
        )

        if game.plain:
            game_info = await self.isthereanydeal_game_info_api.call_api(
                f"&plains={game.plain}"
            )
            game_prices = await self.isthereanydeal_game_prices_api.call_api(
                f"&plains={game.plain}"
            )
            game_historical_low_price = (
                await self.isthereanydeal_historical_price_api.call_api(
                    f"&plains={game.plain}"
                )
            )

            embed = await self.create_gamedeal_embed(
                game_info, game_prices, game_historical_low_price
            )
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(
                f"Could not find game `{game_name}`", ephemeral=True
            )

    ################
    # ERROR HANDLING
    ################

    @command_awesomenauts_rank.error
    async def awesomenauts_rank_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        "command_awesomenauts_rank error handling"
        timeout_message = "Can't retrieve Awesomenauts rankings at the moment"

        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
            (NoBrowserError, timeout_message),
            (pyppeteer.errors.TimeoutError, timeout_message),
        )

    @command_gamedeal.error
    async def gamedeal_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        "command_gamedeal error handling"
        http_error_message = "couldn't reach IsThereAnyDeal.com"
        itad_message = "got an error from IsThereAnyDeal.com"

        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
            (external_api_handler.HttpError, http_error_message),
            (is_there_any_deal_api.IsThereAnyDealError, itad_message),
        )
