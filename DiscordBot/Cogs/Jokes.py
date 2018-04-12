#!python3
# coding: utf-8


"""
Joke Commands.
Each bot command is decorated with a @command decorator.
"""


import random
import sys
from discord.ext import commands
from beckett.clients import BaseClient
from beckett.exceptions import InvalidStatusCodeError
from beckett.resources import BaseResource
from .BaseCog import Cog


class Jokes(Cog):
    """Joke commands"""

    def __init__(self, bot):
        super().__init__(bot)
        self.api_list = [ICanHazDadJokeClient(), OfficialJokeApiClient()]


    # JOKE
    @commands.command(name='joke', ignore_extra=False, invoke_without_command=True)
    async def command_joke(self):
        """Tells a random (bad) joke
        from one of the available apis: icanhazdadjoke.com and official_joke_api @ github)"""
        # I don't really know if the InvalidStatusCodeErrors are caught correctly.
        # These errors are all caught on DiscordBot.py on_command_error, but I wanted to be able to catch a first error
        # here so that I could switch apis on the fly in case one of them stops working.
        # As it stands now, a first error should be caught here, then the api is switched and if another error occurs,
        # it should be caught in DiscordBot.py.
        # I still haven't tested this correctly though...

        # randomly choose one api
        api = random.choice(self.api_list)

        self.log_command_call('joke, with %s' % api.Meta.name)

        # retrieve random joke from the selected api
        try:
            joke = api.get_random_joke(uid=-1)[0]

        except InvalidStatusCodeError as error:
            self.logger.error('Invalid HTTP status code on command joke: %s' % error.status_code)

            # try the other api
            api_alternate = self.api_list[0] if api is not self.api_list[0] else self.api_list[1]

            joke = api_alternate.get_random_joke(uid=-1)[0]
            await self.send_joke(api, joke)
        else:
            await self.send_joke(api, joke)

    async def send_joke(self, api, joke):
        if api is self.api_list[0]:  # ICanHazDadJokeClient
            full_joke = joke.joke
        else:
            full_joke = '%s %s' % (joke.setup, joke.punchline)
        await self.bot.say(full_joke)


######################################
# icanhazdadjoke.com API COMMUNICATION
######################################


class ICanHazDadJokeResource(BaseResource):
    """icanhazdadjoke Resource"""
    class Meta(BaseResource.Meta):
        name = 'random_joke'
        resource_name = 'j'
        identifier = 'id'
        attributes = (
            'id',
            'joke',
            'status'
        )

    @classmethod
    def get_url(cls, url, uid, **kwargs):
        """Overwrite to allow the random joke endpoint when uid == -1, as per icanhazdadjoke api"""
        if uid == -1:  # random joke
            url = url[:-1]  # remove 'j'
        else:  # specific joke
            url = '{}/{}'.format(url, uid)
        return cls._parse_url_and_validate(url)


class ICanHazDadJokeClient(BaseClient):
    class Meta(BaseClient.Meta):
        name = 'icanhazdadjoke.com API'
        base_url = 'https://icanhazdadjoke.com'
        resources = (
            ICanHazDadJokeResource,
        )

    def get_http_headers(self, client_name, method_name, **kwargs):
        """Overwrite to add Accept and User-Agent headers"""
        headers = super().get_http_headers(client_name, method_name, **kwargs)
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = 'Python %s.%s.%s, Discord.py library. bot: https://github.com/Kronopt/DiscordBot'\
                                % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

        return headers


########################################################
# github.com/15Dkatz/official_joke_api API COMMUNICATION
########################################################


class OfficialJokeApiResource(BaseResource):
    """official_joke_api Resource"""
    class Meta(BaseResource.Meta):
        name = 'random_joke'
        resource_name = 'random_joke'
        identifier = 'id'
        attributes = (
            'id',
            'type',
            'setup',
            'punchline'
        )

    @classmethod
    def get_url(cls, url, uid, **kwargs):
        """Overwrite to ignore uid"""
        return cls._parse_url_and_validate(url)


class OfficialJokeApiClient(BaseClient):
    class Meta(BaseClient.Meta):
        name = 'github.com/15Dkatz/official_joke_api API'
        base_url = 'https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev'
        resources = (
            OfficialJokeApiResource,
        )
