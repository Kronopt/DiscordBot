#!python3
# coding: utf-8


"""
Funny Commands
"""


import aiohttp
import collections
import random
from discord.ext import commands
from DiscordBot.BaseCog import Cog
from DiscordBot.Services import (
    Converters, ExternalAPIHandler, ICanHazDadJoke, OfficialJokeAPI, JokeApi)


class NoJokeError(Exception):
    """
    Could not retrieve a joke from any API
    """
    def __init__(self, apis):
        super().__init__()
        self.apis = [str(api) for api in apis]

    def __str__(self):
        return 'Could not retrieve a joke from any of the following APIs: ' \
               ', '.join(self.apis)


class Funny(Cog):
    """
    Funny commands (debatable)
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.emoji = '😂'
        self.eightball_emojis = ['✅', '🔅', '❌']
        self.eightball_answers = [
            'It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely',
            'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes',
            'Signs point to yes', 'Reply hazy, try again', 'Ask again later',
            'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
            'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
            'Very doubtful']
        self.dick = r'(\_\_)_)##{}D'

        headers = {'Accept': 'application/json',
                   'User-Agent': 'DiscordBot (https://github.com/Kronopt/DiscordBot)'}
        icanhazdadjoke_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='ICanHazDadJoke (icanhazdadjoke.com)',
            url='https://icanhazdadjoke.com/',
            headers=headers,
            json_parser=ICanHazDadJoke.DadJoke)
        officialjoke_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='OfficialJokeAPI (github.com/15Dkatz/official_joke_api)',
            url='https://official-joke-api.appspot.com/random_joke',
            headers=headers,
            json_parser=OfficialJokeAPI.OfficialJoke)
        joke_api = ExternalAPIHandler.APICommunicationHandler(
            api_name='JokeAPI (sv443.net/jokeapi/v2)',
            url='https://sv443.net/jokeapi/v2/joke/Any',
            headers=headers,
            json_parser=JokeApi.JokeApiJoke)
        self.apis = [icanhazdadjoke_api, officialjoke_api, joke_api]

    async def get_joke(self):
        """
        joke command implementation

        Returns
        -------
        str
            joke text

        Raises
        ------
        NoJokeError
            if none of the joke APIs is reachable
        """
        # shuffle APIs and then try to get a joke from a single API sequentially
        random.shuffle(self.apis)
        for jokeapi in self.apis:
            try:
                self.logger.info(f'Trying to fetch joke from {jokeapi}')
                joke = await jokeapi.call_api()
                joke_text = joke.text()

            except ExternalAPIHandler.HttpError as error:
                self.logger.error(f'Invalid HTTP status code on command joke: {error.status_code}')

            except (aiohttp.ClientResponseError, aiohttp.ClientConnectionError) as error:
                self.logger.error(f'Can\'t reach {jokeapi}: {error}')

            else:
                self.logger.info(f'Fetched joke from {jokeapi}')
                return joke_text

        # couldn't retrieve a joke from any joke API
        raise NoJokeError(self.apis)

    ##########
    # COMMANDS
    ##########

    # 8BALL
    @commands.command(name='8ball', ignore_extra=False, aliases=['eightball', '8b'])
    async def command_eightball(self, context, *phrase):
        """
        Predicts the outcome of a question

        Bot uses its fortune-telling powers to answer your question.
        Ask a question and get one of the classic magic 8 ball answers.

        ex:
        `<prefix>8ball` is it going to be sunny today?
        `<prefix>8b` are you going to answer correctly?
        """
        if len(phrase) == 0:  # at least one argument
            param = collections.namedtuple('param', 'name')
            raise commands.MissingRequiredArgument(param('phrase'))

        answer = random.randint(0, len(self.eightball_answers) - 1)
        if answer <= 9:  # Affirmative answer
            emoji = self.eightball_emojis[0]
        elif answer <= 14:  # Meh answer
            emoji = self.eightball_emojis[1]
        else:  # Negative answer
            emoji = self.eightball_emojis[2]

        message_without_command = context.message.clean_content.split(maxsplit=1)[1]
        await context.send(
            f'`{message_without_command}`: {self.eightball_answers[answer]} {emoji}')

    # DICK
    @commands.command(name='dick', ignore_extra=False, aliases=['penis'])
    async def command_dick(self, context):
        """
        Reveals user's dick size

        Bot peaks into your pants and reveals your dick size to everyone on the channel.
        You can't change your dick size (talking code here, not real life).

        ex:
        `<prefix>dick`
        `<prefix>penis`
        """
        random.seed(context.author.id)
        dick = self.dick.format('#' * random.randrange(12))
        await context.send(f'{context.author.display_name}\'s dick: {dick}')

    # POOP
    @commands.command(name='poop', ignore_extra=False)
    async def command_poop(self, context, *n: Converters.positive_int):
        """
        Sends poops

        Sends n number of poops (up to the maximum number of characters allowed by discord).

        ex:
        `<prefix>poop`
        `<prefix>poop` 10
        """
        if len(n) > 1:    # At most one argument
            raise commands.TooManyArguments
        if len(n) == 0:
            n = 1  # default
        else:
            n = n[0] if n[0] <= 198 else 198  # character limit
        await context.send('💩' * n)

    # JOKE
    @commands.group(name='joke', ignore_extra=False, aliases=['jk'], invoke_without_command=True)
    async def command_joke(self, context):
        """
        Tells a random (bad) joke

        Jokes are randomly sourced from one of these APIs:
        - http://icanhazdadjoke.com
        - official_joke_api @ http://github.com/15Dkatz/official_joke_api
        - JokeAPI @ http://sv443.net/jokeapi/v2

        ex:
        `<prefix>joke`
        `<prefix>jk`
        """
        joke = await self.get_joke()
        await context.send(joke)

    # JOKE TTS
    @command_joke.command(name='tts', ignore_extra=False, aliases=['-tts', '-t'])
    async def command_joke_tts(self, context):
        """
        Reads joke using tts

        ex:
        `<prefix>joke tts`
        `<prefix>joke -t`
        """
        joke = await self.get_joke()
        await context.send(joke, tts=True)

    ################
    # ERROR HANDLING
    ################

    @command_eightball.error
    async def eightball_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.invoked_with}` ' \
                      'needs a phrase on which to apply its fortune-telling powers'
        await self.generic_error_handler(
            context, error,
            (commands.TooManyArguments, commands.CommandOnCooldown,
             commands.NoPrivateMessage, commands.CheckFailure),
            (commands.MissingRequiredArgument, bot_message),
            (commands.BadArgument, bot_message))

    @command_dick.error
    async def joke_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.invoked_with}` takes no arguments'
        await self.generic_error_handler(
            context, error,
            (commands.MissingRequiredArgument, commands.CommandOnCooldown,
             commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message))

    @command_poop.error
    async def poop_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.invoked_with}` ' \
                      'takes no arguments or 1 positive number'
        await self.generic_error_handler(
            context, error,
            (commands.CommandOnCooldown, commands.NoPrivateMessage,
             commands.CheckFailure, commands.MissingRequiredArgument),
            (commands.BadArgument, bot_message),
            (commands.TooManyArguments, bot_message))

    @command_joke.error
    @command_joke_tts.error
    async def joke_on_error(self, context, error):
        bot_message = f'`{context.prefix}{context.invoked_with}` takes no arguments'
        bot_message_api_error = 'Can\'t retrieve a joke from the server at the moment'
        await self.generic_error_handler(
            context, error,
            (commands.MissingRequiredArgument, commands.CommandOnCooldown,
             commands.NoPrivateMessage, commands.CheckFailure),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (NoJokeError, bot_message_api_error),
            (JokeApi.JokeApiError, bot_message_api_error))
