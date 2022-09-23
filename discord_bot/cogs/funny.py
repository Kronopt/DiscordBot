#!python3
# coding: utf-8


"""
Funny Commands
"""


from typing import TYPE_CHECKING, Optional
import random
import aiohttp
from discord import app_commands, Interaction
from discord_bot.base_cog import Cog
from discord_bot.services import (
    external_api_handler,
    i_can_haz_dad_joke_api,
    joke_api,
    official_joke_api,
    transformers,
)

if TYPE_CHECKING:
    from discord_bot.bot import Bot


class NoJokeError(Exception):
    """
    Could not retrieve a joke from any API
    """

    def __init__(self, apis: list[external_api_handler.APICommunicationHandler]):
        super().__init__()
        self.apis = [str(api) for api in apis]

    def __str__(self):
        return "Could not retrieve a joke from any of the following APIs: " ", ".join(
            self.apis
        )


class Funny(Cog):
    """
    Funny commands (debatable)
    """

    def __init__(self, bot: "Bot"):
        super().__init__(bot)
        self.emoji = "😂"
        self.eightball_emojis = ["✅", "🔅", "❌"]
        self.eightball_answers = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]
        self.dick = r"(\_\_)_)##{}D"

        headers = {
            "Accept": "application/json",
            "User-Agent": "DiscordBot (https://github.com/Kronopt/DiscordBot)",
        }
        icanhazdadjoke_api = external_api_handler.APICommunicationHandler(
            api_name="ICanHazDadJoke (icanhazdadjoke.com)",
            base_url="https://icanhazdadjoke.com",
            headers=headers,
            json_parser=i_can_haz_dad_joke_api.DadJoke,
        )
        officialjoke_api = external_api_handler.APICommunicationHandler(
            api_name="OfficialJokeAPI (github.com/15Dkatz/official_joke_api)",
            base_url="https://official-joke-api.appspot.com/random_joke",
            headers=headers,
            json_parser=official_joke_api.OfficialJoke,
        )
        jokeapi_api = external_api_handler.APICommunicationHandler(
            api_name="JokeAPI (sv443.net/jokeapi/v2)",
            base_url="https://sv443.net/jokeapi/v2/joke/Any",
            headers=headers,
            json_parser=joke_api.JokeApiJoke,
        )
        self.apis = [icanhazdadjoke_api, officialjoke_api, jokeapi_api]

    async def get_joke(self) -> str:
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
                self.logger.info(f"Trying to fetch joke from {jokeapi}")
                joke = await jokeapi.call_api()
                joke_text = joke.text()

            except external_api_handler.HttpError as error:
                self.logger.error(
                    f"Invalid HTTP status code on command joke: {error.status_code}"
                )

            except (
                aiohttp.ClientResponseError,
                aiohttp.ClientConnectionError,
            ) as error:
                self.logger.error(f"Can't reach {jokeapi}: {error}")

            else:
                self.logger.info(f"Fetched joke from {jokeapi}")
                return joke_text

        # couldn't retrieve a joke from any joke API
        raise NoJokeError(self.apis)

    ##########
    # COMMANDS
    ##########

    # 8BALL
    @app_commands.command(name="8ball")
    @app_commands.describe(question="question for bot")
    async def command_eightball(self, interaction: Interaction, question: str):
        """
        Predicts the outcome of a question

        Bot uses its fortune-telling powers to predict the outcome of your question.
        Ask a question and get one of the classic magic 8 ball answers.

        ex:
        `<prefix>8ball` is it going to be sunny today?
        """
        answer = random.randint(0, len(self.eightball_answers) - 1)
        if answer <= 9:  # Affirmative answer
            emoji = self.eightball_emojis[0]
        elif answer <= 14:  # Meh answer
            emoji = self.eightball_emojis[1]
        else:  # Negative answer
            emoji = self.eightball_emojis[2]

        await interaction.response.send_message(
            f"`{question}`: {self.eightball_answers[answer]} {emoji}"
        )

    # DICK
    @app_commands.command(name="dick")
    async def command_dick(self, interaction: Interaction):
        """
        Reveals user's dick size

        Bot peaks into your pants and reveals your dick size to everyone on the channel.
        You can't change your dick size (talking code here, not real life).

        ex:
        `<prefix>dick`
        """
        random.seed(interaction.user.id)
        dick = self.dick.format("#" * random.randrange(12))
        await interaction.response.send_message(
            f"{interaction.user.display_name}'s dick: {dick}"
        )

    # POOP
    @app_commands.command(name="poop")
    @app_commands.describe(n="number of poops")
    async def command_poop(
        self,
        interaction: Interaction,
        n: Optional[app_commands.Transform[int, transformers.PositiveInteger]] = 1,
    ):
        """
        Sends poops

        Sends n number of poops (up to the maximum number of characters allowed by discord).

        ex:
        `<prefix>poop`
        `<prefix>poop` 10
        """
        n = n if n <= 198 else 198  # character limit
        await interaction.response.send_message("💩" * n)

    # JOKE
    @app_commands.command(name="joke")
    @app_commands.describe(tts="if the joke should be read by tts")
    async def command_joke(self, interaction: Interaction, tts: Optional[bool] = False):
        """
        Tells a random (bad) joke

        Jokes are randomly sourced from one of these APIs:
        - http://icanhazdadjoke.com
        - official_joke_api @ http://github.com/15Dkatz/official_joke_api
        - JokeAPI @ http://sv443.net/jokeapi/v2

        ex:
        `<prefix>joke`
        `<prefix>joke` tts=True
        """
        joke = await self.get_joke()
        await interaction.response.send_message(joke, tts=tts)

    ################
    # ERROR HANDLING
    ################

    @command_eightball.error
    @command_dick.error
    async def eightball_dick_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """
        command_eightball and command_dick error handling
        """
        await self.generic_error_handler(interaction, error, tuple())

    @command_poop.error
    async def eightball_dick_poop_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """
        command_poop error handling
        """
        bot_message_error = "argument is not a positive integer"
        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
            (app_commands.errors.TransformerError, bot_message_error),
        )

    @command_joke.error
    async def joke_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """
        command_joke error handling
        """
        bot_message_api_error = "Can't retrieve a joke from the server at the moment"
        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
            (NoJokeError, bot_message_api_error),
            (joke_api.JokeApiError, bot_message_api_error),
        )
