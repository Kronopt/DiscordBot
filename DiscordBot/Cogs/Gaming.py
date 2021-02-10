#!python3
# coding: utf-8


"""
Gaming related Commands
"""


import asyncio
import collections
import urllib
import discord
import pyppeteer
from discord.ext import commands
from DiscordBot.BaseCog import Cog
from DiscordBot.Services import AwesomenautsRank, ExternalAPIHandler, IsThereAnyDealAPI


class NoBrowserError(Exception):
    """
    Browser is not available
    """
    def __str__(self):
        return 'Browser is not available'


class Gaming(Cog):
    """
    Commands that deal with games/gaming (player rank, high scores, characters, etc)
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = '🎮'
        self.browser = None
        self.awesomenauts_rank_url = 'https://orikaru.net/nautsrankings#//rank/asc/{}//'
        self.isthereanydeal_base_url = 'https://api.isthereanydeal.com'

        headers = {'Accept': 'application/json',
                   'User-Agent': 'DiscordBot (https://github.com/Kronopt/DiscordBot)'}
        self.isthereanydeal_identifier_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='IsThereAnyDeal API, Identifier endpoint',
            base_url=f'{self.isthereanydeal_base_url}/v02/game/plain/?key='
                     f'{self.bot.cog_args["isthereanydeal_token"]}',
            headers=headers,
            json_parser=IsThereAnyDealAPI.IdentifierEndpoint)
        self.isthereanydeal_game_info_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='IsThereAnyDeal API, Get Info About Game endpoint',
            base_url=f'{self.isthereanydeal_base_url}/v01/game/info/?key='
                     f'{self.bot.cog_args["isthereanydeal_token"]}',
            headers=headers,
            json_parser=IsThereAnyDealAPI.GetInfoAboutGameEndpoint)
        self.isthereanydeal_game_prices_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='IsThereAnyDeal API, Get Current Game Prices endpoint',
            base_url=f'{self.isthereanydeal_base_url}/v01/game/prices/?key='
                     f'{self.bot.cog_args["isthereanydeal_token"]}&region=eu2&country=PT',
            headers=headers,
            json_parser=IsThereAnyDealAPI.GetCurrentPricesEndpoint)
        self.isthereanydeal_historical_price_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='IsThereAnyDeal API, Get Historical Price endpoint',
            base_url=f'{self.isthereanydeal_base_url}/v01/game/lowest/?key='
                     f'{self.bot.cog_args["isthereanydeal_token"]}&region=eu2&country=PT',
            headers=headers,
            json_parser=IsThereAnyDealAPI.GetHistoricalLowEndpoint)

    async def setup_cog(self):
        # init browser
        chromium_args = self.bot.cog_args['chromium_args']
        launcher = pyppeteer.launcher.Launcher({'args': chromium_args})

        # for testing:
        # import os
        # os.system(' '.join(launcher.cmd))

        self.browser = await launcher.launch()

    async def create_gamedeal_embed(self, game_info, game_prices, game_historical_low_price):
        embed = discord.Embed(colour=self.embed_colour)

        # game title
        dlc = ' (DLC)' if game_info.is_dlc else ''
        embed.set_author(name=game_info.title + dlc)

        # game prices per store
        embed_value = ''
        for shop in game_prices.shops:
            price_current = f'{shop.price_full}{game_prices.currency}'
            if shop.price_percent_discount != 0:
                price_current = f'~~{price_current}~~'
                price_cut = f'{shop.price_discounted}{game_prices.currency} ' \
                            f'(-{shop.price_percent_discount}%) '
            else:
                price_cut = ''

            shop_price_info = f'{price_current} {price_cut}[{shop.name}]({shop.game_url})\n'

            if len(embed_value) + len(shop_price_info) < 1024:  # embed.field.value size limit
                embed_value += shop_price_info
            else:
                embed.add_field(name='\u200b', value=embed_value, inline=False)
                embed_value = shop_price_info

        embed.add_field(name='\u200b', value=embed_value, inline=False)

        # historical low price and store
        embed.add_field(name='\u200b\nHistorical Low',
                        value=f'__{game_historical_low_price.price}{game_prices.currency}__ '
                              f'on {game_historical_low_price.store}',
                        inline=True)

        # steam review, if any
        if game_info.steam_review:
            embed.add_field(name='\u200b\nSteam Review',
                            value=f'**{game_info.steam_review.text}**\n'
                                  f'({game_info.steam_review.positive_reviews_percent}% of '
                                  f'{game_info.steam_review.total_reviews} users)',
                            inline=True)

        # game image
        if game_info.image_url:
            embed.set_image(url=game_info.image_url)

        # footer info
        embed.set_footer(text='source: IsThereAnyDeal.com ❤',
                         icon_url='https://d2uym1p5obf9p8.cloudfront.net/images/favicon.png')

        return embed

    ##########
    # COMMANDS
    ##########

    # AWESOMENAUTS
    @commands.group(name='awesomenauts', ignore_extra=False, invoke_without_command=True)
    async def command_awesomenauts(self, context, *subcommand):
        await context.send('Please specify a known subcommand')
        await context.send_help(self.command_awesomenauts)

    # AWESOMENAUTS RANK
    @command_awesomenauts.command(name='rank', ignore_extra=False, aliases=['r', '-r'])
    async def command_awesomenauts_rank(self, context, *player_name):
        """
        Displays rank of an Awesomenaut's player

        Matches highest ranked player out of a list of closely named players found
        (ie, retrieves first result obtained from https://orikaru.net/nautsrankings)

        ex:
        `<prefix>awesomenauts rank` niki
        `<prefix>awesomenauts r` game is broken
        """
        if len(player_name) == 0:  # at least one argument
            param = collections.namedtuple('param', 'name')
            raise commands.MissingRequiredArgument(param('player_name'))

        player_name = ' '.join(player_name)
        player_name_quoted = urllib.parse.quote(player_name)

        if self.browser is None:
            raise NoBrowserError()

        page = await self.browser.newPage()
        await page.goto(self.awesomenauts_rank_url.format(player_name_quoted),
                        options={"timeout": 5000})

        # either the list of players is populated or the "no results" message is shown,
        # whatever happens first. forced timeout after 5 seconds
        rank_selector = page.waitForSelector('#leaderboard tbody tr')
        no_result_selector = page.waitForSelector('#content-container #no-result:not(.hidden)')
        _, pending = await asyncio.wait(
            [rank_selector, no_result_selector],
            return_when=asyncio.FIRST_COMPLETED,
            timeout=5)
        for c in pending:
            c.cancel()

        players = await page.querySelectorAll('#leaderboard tbody tr')

        if players:
            player = players[1]  # zeroth element is the header
            text_fields = await player.querySelectorAllEval(
                'td',
                '(nodes => nodes.map(n => n.innerText))')
            steam_profile = await player.querySelectorEval(
                'td a',
                'node => node.href')
            img_urls = await player.querySelectorAllEval(
                'td img',
                '(nodes => nodes.map(n => n.src))')
            img_titles = await player.querySelectorAllEval(
                'td img',
                '(nodes => nodes.map(n => n.title))')

            awesomenaut_rank = AwesomenautsRank.AwesomenautsRank(
                self.embed_colour,
                {'player_name': text_fields[1].rstrip(),
                 'rank': text_fields[0].rstrip(),
                 'games_played_current_season': text_fields[3].rstrip(),
                 'games_played_all_time': text_fields[4].rstrip(),
                 'win_percentage': text_fields[2].rstrip()[:-1],
                 'rating': text_fields[6].rstrip(),
                 'league': img_titles[0],
                 'league_img_url': img_urls[0],
                 'favourite_naut': img_titles[1],
                 'favourite_naut_img_url': img_urls[1],
                 'country': img_titles[2] if len(img_titles) == 3 else '',
                 'steam_profile_url': steam_profile})

            await context.send(embed=awesomenaut_rank.embed)

        else:
            await context.send(f'Can\'t retrieve player `{player_name}`')

        await page.close()

    # GAMEDEAL
    @commands.command(name='gamedeal', ignore_extra=False, aliases=['gameprice'])
    async def command_gamedeal(self, context, *game_name):
        """
        Displays game pricing info

        Info pertains to all stores in which the game is available for purchase

        ex:
        `<prefix>gamedeal` Assassin's Creed Odyssey
        `<prefix>gameprice` Cyberpunk 2077
        """
        if len(game_name) == 0:  # at least one argument
            param = collections.namedtuple('param', 'name')
            raise commands.MissingRequiredArgument(param('game_name'))

        game_name = ' '.join(game_name)
        game_name_quoted = urllib.parse.quote(game_name)

        game = await self.isthereanydeal_identifier_api.call_api(f'&title={game_name_quoted}')

        if game.plain:
            game_info = await self.isthereanydeal_game_info_api.call_api(
                f'&plains={game.plain}')
            game_prices = await self.isthereanydeal_game_prices_api.call_api(
                f'&plains={game.plain}')
            game_historical_low_price = await self.isthereanydeal_historical_price_api.call_api(
                f'&plains={game.plain}')

            embed = await self.create_gamedeal_embed(
                game_info, game_prices, game_historical_low_price)
            await context.send(embed=embed)

        else:
            await context.send(f'Could not find game `{game_name}`')

    ################
    # ERROR HANDLING
    ################

    @command_awesomenauts.error
    async def awesomenauts_on_error(self, context, error):
        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure))

    @command_awesomenauts_rank.error
    async def awesomenauts_rank_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.command.qualified_name}` expects an ' \
                      'Awesomenauts player name as argument'
        timeout_message = 'Can\'t retrieve Awesomenauts rankings at the moment'

        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (commands.MissingRequiredArgument, bot_message),
            (NoBrowserError, timeout_message),
            (pyppeteer.errors.TimeoutError, timeout_message))

    # TODO error handling
    @command_gamedeal.error
    async def gamedeal_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.command.qualified_name}` error'

        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (commands.MissingRequiredArgument, bot_message))
