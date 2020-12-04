#!python3
# coding: utf-8


"""
Gaming related Commands
"""


import asyncio
import collections
import urllib
from discord.ext import commands
import pyppeteer
from DiscordBot.BaseCog import Cog
from DiscordBot.Services import AwesomenautsRank



#     """
#
#
#
#
#
class Gaming(Cog):
    """
    Commands that deal with games/gaming (player rank, high scores, characters, etc)
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = '🎮'
        self.browser = None
        self.awesomenauts_rank_url = 'https://orikaru.net/nautsrankings#//rank/asc/{}//'

        # if _awesomenauts_wiki_unreachable:
        #     self.command_awesomenauts.enabled = False
        #     self.command_awesomenauts_rank.enabled = False
        # else:
        #     self.awesomenauts_url = 'https://awesomenauts.gamepedia.com/%s#Stats'
        # self.rankings_url = 'https://nautsrankings.com/index.php?search=%s'

    async def setup_cog(self):
        launcher = pyppeteer.launcher.Launcher({'args': ['--no-sandbox']})

        # for testing
        # chromium_cmd = ' '.join(launcher.cmd)
        # import os
        # os.system(chromium_cmd)

        self.browser = await launcher.launch()

    ##########
    # COMMANDS
    ##########

    # AWESOMENAUTS
    @commands.group(name='awesomenauts', ignore_extra=False, invoke_without_command=True)
    async def command_awesomenauts(self, context, *subcommand):
        await context.send('Please specify a known subcommand\n'
                           f'Type `{context.prefix}help {context.invoked_with}` to know more')

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

    ################
    # ERROR HANDLING
    ################

    # @command_awesomenauts.error
    # @command_awesomenauts_rank.error

    @command_awesomenauts.error
    async def awesomenauts_on_error(self, context, error):
        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure))

    @command_awesomenauts_rank.error
    async def awesomenauts_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.command.qualified_name}` expects an ' \
                      'Awesomenauts player name as argument'
        timeout_message = 'can\'t retrieve Awesomenauts rankings at the moment'

        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (commands.MissingRequiredArgument, bot_message),
            (pyppeteer.errors.TimeoutError, timeout_message))
