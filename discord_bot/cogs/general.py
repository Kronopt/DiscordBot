#!python3
# coding: utf-8


"""
General Commands
"""


from typing import TYPE_CHECKING, Optional
import random
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord_bot.base_cog import Cog

if TYPE_CHECKING:
    from discord_bot.bot import Bot


class General(Cog):
    """
    General commands that don't fit in other, more specific, categories
    """

    def __init__(self, bot: "Bot"):
        super().__init__(bot)
        self.emoji = "🎛️"
        self.greetings = [
            "Hi",
            "Hello",
            "Hey",
            "Sup",
            "What's up",
            "Greetings",
            "Howdy",
        ]
        self.greeting_emojis = ["👋", "🤙", "🖖", "🤟", "👊", "🙌"]
        self.poll_options = [
            "🇦",
            "🇧",
            "🇨",
            "🇩",
            "🇪",
            "🇫",
            "🇬",
            "🇭",
            "🇮",
            "🇯",
            "🇰",
            "🇱",
            "🇲",
            "🇳",
            "🇴",
            "🇵",
            "🇶",
            "🇷",
            "🇸",
            "🇹",
        ]

    def create_poll_embed(self, name: str, options: list[str]) -> discord.Embed:
        """poll embed"""
        embed = discord.Embed(colour=self.embed_colour, description=f"📊 **{name}**\n\n")
        for i, option in enumerate(options):
            embed.description += f"{self.poll_options[i]} {option}\n"

        return embed

    async def react_with_options(self, message: discord.Message, options: list[str]):
        "add voting options as reactions to message"
        if options:
            for i in range(len(options)):
                await message.add_reaction(self.poll_options[i])
        else:
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            await message.add_reaction("🤷")

    ##########
    # COMMANDS
    ##########

    # HI
    @app_commands.command(name="hi")
    async def command_hi(self, interaction: Interaction):
        """
        Greets user

        ex:
        `<prefix>hi`
        """
        greeting = random.choice(self.greetings)
        emoji = random.choice(self.greeting_emojis)
        await interaction.response.send_message(
            f"{greeting}, {interaction.user.display_name}! {emoji}"
        )

    # DICE
    @app_commands.command(name="dice")
    @app_commands.describe(die="die to roll")
    @app_commands.choices(
        die=[
            app_commands.Choice(name="d4", value=4),
            app_commands.Choice(name="d6", value=6),
            app_commands.Choice(name="d8", value=8),
            app_commands.Choice(name="d10", value=10),
            app_commands.Choice(name="d12", value=12),
            app_commands.Choice(name="d20", value=20),
        ]
    )
    async def command_dice(
        self, interaction: Interaction, die: app_commands.Choice[int]
    ):
        """
        Rolls a die

        Possible dices: `d4`, `d6`, `d8`, `d10`, `d12` and `d20`

        ex:
        `<prefix>dice` d20
        """
        dice_roll = random.randint(1, die.value)
        await interaction.response.send_message(
            f"Rolled a **{dice_roll}** with a {die.name}"
        )

    # POLL
    @app_commands.command(name="poll")
    @app_commands.describe(
        name="poll name", options="comma-separated options to include in the poll"
    )
    async def command_poll(
        self, interaction: Interaction, name: str, options: Optional[str]
    ):
        """
        Starts a poll

        If just the poll name is given, options will be yes/no/maybe, otherwise
        each option will have a letter associated.

        ex:
        `<prefix>poll` Is this a cool poll command?
        `<prefix>poll` Favourite icecream? options="chocolate and vanilla, strawberry, banana"
        """
        if not options:
            options = ""
        options = options.split(",")

        embed_options = []
        for option in options:
            option = option.strip()
            if len(option) > 0:
                embed_options.append(option)

        if len(embed_options) <= 20:
            await interaction.response.send_message(
                embed=self.create_poll_embed(name, embed_options)
            )
            message = await interaction.original_response()
            await self.react_with_options(message, embed_options)
        else:
            raise commands.TooManyArguments("Maximum number of options is 20")

    ################
    # ERROR HANDLING
    ################

    @command_hi.error
    @command_dice.error
    async def hi_dice_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """command_hi and command_dice error handling"""
        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
        )

    @command_poll.error
    async def poll_on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        """command_poll error handling"""
        bot_message_error = "maximum number of options is 20"
        if isinstance(error, app_commands.errors.CommandInvokeError):
            error = error.original

        await self.generic_error_handler(
            interaction,
            error,
            tuple(),
            (commands.TooManyArguments, bot_message_error),
        )
