#!python3
# coding: utf-8


"""
Awesomenauts related Commands.
"""

import asyncio
import logging
import discord
import regex
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from DiscordBot.BaseCog import Cog


logger = logging.getLogger('discord')

_wiki_url = 'https://awesomenauts.gamepedia.com/Awesomenauts_Wiki'
_awesomenauts_wiki_unreachable = False  # if html is unreachable or has changed, this will be True

# retrieve list of available awesomenauts (as long as the wiki is updated)
# assumes the bot is restarted periodically (as heroku does) to refresh list
try:
    _awesomenaut_list_html = requests.get(_wiki_url)
except requests.exceptions.RequestException:
    _awesomenauts_wiki_unreachable = True
    logger.warning('Awesomenauts Wiki (%s) is unreachable' % _wiki_url)
else:
    _awesomenaut_list_soup = BeautifulSoup(_awesomenaut_list_html.text, 'html.parser')

    try:
        # list of pairs (awesomenaut_name, awesomenaut_url_ready_name)
        AWESOMENAUTS = [(awesomenaut.text, awesomenaut.a['href'][1:])
                        for awesomenaut in
                        _awesomenaut_list_soup.find(id='p-.27Nauts').find_all('li')]
    except (AttributeError, KeyError):
        # html was altered and, therefore, the code is now broken...
        _awesomenauts_wiki_unreachable = True
        logger.warning('Awesomenauts Wiki\'s html (%s) has changed' % _wiki_url)


def existing_awesomenaut(name):
    """
    Converter that finds whether the given name matches a known awesomenaut.
    Returns the url ready name of the matched awesomenaut, raises ValueError otherwise.

    Parameters
    ----------
    name: str
        Part or complete name of the awesomenaut

    Returns
    -------
    url ready awesomenaut name, raises ValueError if no matching awesomenaut is found
    """
    _name = name.lower().strip()

    # for smaller words will look at the start of the awesomenaut's name instead of it's whole
    if len(_name) <= 2:
        regex_operation = 'match'
        re = regex.escape(_name)
    else:
        regex_operation = 'search'
        re = '(%s){e<=1}' % regex.escape(_name)  # search for the given name with at most 1 mistake

    regex_result = {}
    best_match = (None, 2)  # (regex_result key, fuzzy_counts)
    for awesomenaut_name, awesomenaut_url_name in AWESOMENAUTS:
        result = getattr(regex, regex_operation)(re, awesomenaut_name.lower(), regex.BESTMATCH)
        if result:
            regex_result[result] = awesomenaut_url_name
            fuzzy_counts = sum(result.fuzzy_counts)
            # first match will always overwrite the best_match variable
            if fuzzy_counts < best_match[1]:
                best_match = (result, fuzzy_counts)

    if regex_result:
        return regex_result[best_match[0]]
    raise ValueError(name + ' does not match an existing awesomenaut')


class Awesomenauts(Cog):
    """Awesomenauts related commands"""

    def __init__(self, bot):
        super().__init__(bot)
        self.help_order = 6

        if _awesomenauts_wiki_unreachable:
            self.command_awesomenauts.enabled = False
            self.command_awesomenauts_rank.enabled = False
        else:
            self.awesomenauts_url = 'https://awesomenauts.gamepedia.com/%s#Stats'
            self.rankings_url = 'https://nautsrankings.com/index.php?search=%s'

    ##########
    # COMMANDS
    ##########

    # AWESOMENAUT
    @commands.group(name='awesomenauts', ignore_extra=False, aliases=['awesomenaut'],
                    invoke_without_command=True,)
    async def command_awesomenauts(self, context, awesomenaut: existing_awesomenaut):
        """Displays information of the specified awesomenaut.

        Any text that matches at least part of an awesomenaut's name will work.
        Matches are performed in alphabetical order ('Coco' matches first than
        'Commander Rocket' for text 'co').
        Info retrieved from https://awesomenauts.gamepedia.com"""
        # parameter is the URL READY NAME
        # (raises ValueError if it does not match an existing awesomenaut)
        current_awesomenaut_url = self.awesomenauts_url % awesomenaut

        awesomenaut_url = requests.get(current_awesomenaut_url)
        awesomenaut_soup = BeautifulSoup(awesomenaut_url.text, 'html.parser')

        rows = awesomenaut_soup.table.find_all('tr')
        name_difficulty = rows[10].text.split()

        awesomenaut_info = dict()
        awesomenaut_info['image'] = awesomenaut_soup.table.img['src']
        awesomenaut_info['name'] = ' '.join(name_difficulty[:name_difficulty.index('[edit]')])
        awesomenaut_info['difficulty'] = name_difficulty[name_difficulty.index('Difficulty:') + 1]
        awesomenaut_info['health'] = ' '.join(rows[1].text.split()[1:])
        awesomenaut_info['movement_speed'] = ' '.join(rows[2].text.split()[2:])
        awesomenaut_info['attack_type'] = ' '.join(rows[3].text.split()[2:])
        awesomenaut_info['role'] = ' '.join(rows[4].text.split()[1:])
        awesomenaut_info['mobility'] = ' '.join(rows[5].text.split()[1:])

        # build embed
        awesomenaut_embed = discord.Embed(colour=self.embed_colour)
        awesomenaut_embed.set_thumbnail(url=awesomenaut_info['image'])
        awesomenaut_embed.set_author(name=awesomenaut_info['name'],
                                     url=current_awesomenaut_url,
                                     icon_url='https://d1u5p3l4wpay3k.cloudfront.net/'
                                              'awesomenauts_gamepedia/0/04/Overdrivesign.png')
        awesomenaut_embed.add_field(name=':chart_with_upwards_trend: DIFFICULTY',
                                    value=awesomenaut_info['difficulty'] + '\n\u200b')
        awesomenaut_embed.add_field(name=':spy: ROLE', value=awesomenaut_info['role'] + '\n\u200b')
        awesomenaut_embed.add_field(name=':heart: HEALTH', value=awesomenaut_info['health'] +
                                                                 '\n\u200b')
        awesomenaut_embed.add_field(name=':boot: MOVEMENT SPEED',
                                    value=awesomenaut_info['movement_speed'] + '\n\u200b')
        awesomenaut_embed.add_field(name=':crossed_swords: ATTACK TYPE',
                                    value=awesomenaut_info['attack_type'] + '\n\u200b')
        awesomenaut_embed.add_field(name=':runner: MOBILITY', value=awesomenaut_info['mobility'] +
                                                                    '\n\u200b')

        await context.send(embed=awesomenaut_embed)

    # AWESOMENAUT LIST
    @command_awesomenauts.command(name='list', ignore_extra=False, aliases=['l', '-l'])
    async def command_awesomenauts_list(self, context):
        """Displays all currently existing Awesomenauts characters alphabetically."""
        list_embed = discord.Embed(colour=self.embed_colour)

        current_letter = ''
        name = ''
        value = ''
        first = True
        for awesomenaut, _ in AWESOMENAUTS:  # assumes awesomenauts are alphabetically ordered
            if awesomenaut[0] != current_letter:
                if not first:
                    value += '\n\u200b'
                    list_embed.add_field(name=name, value=value)
                else:
                    first = False

                current_letter = awesomenaut[0]
                name = '- %s -' % current_letter.upper()
                value = awesomenaut
            else:
                value += '\n' + awesomenaut
        list_embed.add_field(name=name, value=value)
        list_embed.set_footer(text='There currently are %s Awesomenauts' % len(AWESOMENAUTS))
        await context.send(embed=list_embed)

    # AWESOMENAUT RANK
    @command_awesomenauts.command(name='rank', ignore_extra=False, aliases=['r', '-r'])
    async def command_awesomenauts_rank(self, context, player: str):
        """Displays rank information of an Awesomenaut's player.

        Matches highest ranked player, alphabetically.
        Retrieves first result obtained from https://nautsrankings.com"""
        _rankings_url = self.rankings_url % player.replace(' ', '+')
        rankings_url = requests.get(_rankings_url)
        rankings_soup = BeautifulSoup(rankings_url.text, 'html.parser')

        # player doesn't exist
        if rankings_soup.find('div', {'class': 'entries'}).text.startswith('0'):
            await context.send('No player whose name starts with `%s` was found.\n'
                               'Only players that played during the current awesomenauts season are'
                               ' available.' % player)
            return

        row = rankings_soup.find('div', {'id': 'rankings'}).find('img')
        player_info = row.find('div', {'class': 'name'})
        games_played = row.find_all('div', {'class': 'played'})
        favourite_naut = row.find('div', {'class': 'favorite'}).find('img')

        ranking_info = dict()
        ranking_info['league'] = 'https://nautsrankings.com/%s' % row['src']
        ranking_info['rank'] = row.a.text
        ranking_info['player_steam_url'] = player_info.a['href']
        ranking_info['player_img'] = player_info.a.img['src']
        ranking_info['player_name'] = player_info.a['title']
        ranking_info['win_percent_this_season'] = row.find('div', {'class': 'win'}).text
        ranking_info['games_played_this_season'] = games_played[0].text
        ranking_info['games_played_this_season_wins'] = games_played[0]['title'].split()[1].rstrip(',')
        ranking_info['games_played_this_season_losses'] = games_played[0]['title'].split()[3]
        ranking_info['win_percent_total'] = games_played[1]['title'].split()[5]
        ranking_info['games_played_total'] = games_played[1].text
        ranking_info['games_played_total_wins'] = games_played[1]['title'].split()[1].rstrip(',')
        ranking_info['games_played_total_losses'] = games_played[1]['title'].split()[3].rstrip(',')
        ranking_info['favourite_naut_name'] = favourite_naut['title']
        ranking_info['favourite_naut_img'] = 'https://nautsrankings.com/%s' % favourite_naut['src']
        ranking_info['rating'] = row.find('div', {'class': 'rating'}).text

        # build embed
        ranking_embed = discord.Embed(colour=self.embed_colour)
        ranking_embed.set_thumbnail(url=ranking_info['league'])
        ranking_embed.set_author(name=ranking_info['player_name'],
                                 url=ranking_info['player_steam_url'],
                                 icon_url=ranking_info['player_img'])
        ranking_embed.add_field(name=':first_place: RANK', value=ranking_info['rank'] + '\n\u200b')
        ranking_embed.add_field(name=':star2: RATING', value=ranking_info['rating'] + '\n\u200b')
        ranking_embed.add_field(name=':chart_with_upwards_trend: THIS SEASON',
                                value='Games Played:   ' +
                                      ranking_info['games_played_this_season'] + '\n'
                                      'Games Won:      ' +
                                      ranking_info['games_played_this_season_wins'] + '\n'
                                      'Games Lost:       ' +
                                      ranking_info['games_played_this_season_losses']
                                      + '\n'
                                      'Win%:                 ' +
                                      ranking_info['win_percent_this_season'] +
                                      '\n\u200b')
        ranking_embed.add_field(name=':mortar_board: TOTAL',
                                value='Games Played:   ' +
                                      ranking_info['games_played_total'] + '\n'
                                      'Games Won:      ' +
                                      ranking_info['games_played_total_wins'] + '\n'
                                      'Games Lost:       ' +
                                      ranking_info['games_played_total_losses'] + '\n'
                                      'Win%:                 ' + ranking_info['win_percent_total'] +
                                      '\n\u200b')
        ranking_embed.set_footer(text=ranking_info['favourite_naut_name'] + ' (favourite naut)',
                                 icon_url=ranking_info['favourite_naut_img'])

        await context.send(embed=ranking_embed)

    ################
    # ERROR HANDLING
    ################

    @command_awesomenauts.error
    @command_awesomenauts_list.error
    @command_awesomenauts_rank.error
    async def awesomenaut_awesomenaut_rank_on_error(self, error, context):
        bot_message_url_unreachable = 'Can\'t access Awesomenauts information right now. ' \
                                      'Command will sleep for a few minutes'
        bot_message_html_changed = 'Can\'t access Awesomenauts information right now. Command will ' \
                                   'sleep until issue is fixed'
        if context.command.callback is self.command_awesomenauts.callback:
            bot_message = '`%s%s` takes a name of an awesomenaut (or part of it) as ' \
                          'argument (use quotation marks to enclose space ' \
                          'separated names).' % (context.prefix, context.invoked_with)
            url_fetch_error_message = 'Awesomenauts Wiki (%s) is ' \
                                      'unreachable' % self.awesomenauts_url
            html_changed_error = 'Awesomenauts Wiki\'s html (%s) ' \
                                 'has changed' % self.awesomenauts_url
        elif context.command.callback is self.command_awesomenauts_rank.callback:
            bot_message = '`%s%s` takes a player name as argument (use quotation marks ' \
                          'to enclose space separated ' \
                          'names).' % (context.prefix, context.command.qualified_name)
            url_fetch_error_message = 'nautsrankings.com (%s) is unreachable' % self.rankings_url
            html_changed_error = 'nautsrankings.com html (%s) has changed' % self.rankings_url
        else:  # awesomenauts list
            bot_message = '`%s%s` takes no arguments.' % (context.prefix,
                                                          context.command.qualified_name)
            url_fetch_error_message = ''
            html_changed_error = ''
        await self.generic_error_handler(error, context,
                                         (commands.CommandOnCooldown, commands.NoPrivateMessage,
                                          commands.CheckFailure),
                                         (commands.MissingRequiredArgument, bot_message),
                                         (commands.TooManyArguments, bot_message),
                                         (commands.BadArgument, bot_message))
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, requests.exceptions.RequestException):
                self.logger.warning(url_fetch_error_message)
                await context.send(bot_message_url_unreachable)
                context.command.enabled = False
                await asyncio.sleep(60 * 5)  # disable command for 5 minutes
                context.command.enabled = True
            elif isinstance(error.original, (AttributeError, KeyError, IndexError)):
                # html was altered and, therefore, the code is now broken...
                self.logger.warning(html_changed_error)
                await context.send(bot_message_html_changed)
                context.command.enabled = False
