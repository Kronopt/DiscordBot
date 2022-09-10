#!python3
# coding: utf-8


"""
General Commands
"""


import random
import discord
from discord.ext import commands
from discord_bot.base_cog import Cog
from discord_bot.services import converters


class General(Cog):
    """
    General commands that don't fit in other, more specific, categories
    """

    def __init__(self, bot):
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

    def create_poll_embed(self, name, options):
        """poll embed"""
        embed = discord.Embed(colour=self.embed_colour, description=f"📊 **{name}**\n\n")
        for i, option in enumerate(options):
            embed.description += f"{self.poll_options[i]} {option}\n"

        return embed

    async def react_with_options(self, message, options):
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
    @commands.hybrid_command(
        name="hi",
        ignore_extra=False,
        aliases=["hello", "hey", "sup", "greetings", "howdy"],
    )
    async def command_hi(self, context):
        """
        Greets user

        ex:
        `<prefix>hi`
        `<prefix>hey`
        """
        greeting = random.choice(self.greetings)
        emoji = random.choice(self.greeting_emojis)
        await context.send(f"{greeting}, {context.author.display_name}! {emoji}")

    # DICE
    @commands.hybrid_command(name="dice", ignore_extra=False)
    async def command_dice(self, context, dice: converters.dice):
        """
        Rolls a die

        Possible dices: `d4`, `d6`, `d8`, `d10`, `d12` and `d20`

        ex:
        `<prefix>dice`
        `<prefix>dice` d20
        """
        dice_number = int(dice[1:])
        dice_roll = random.randint(1, dice_number)
        await context.send("Rolled a **" + str(dice_roll) + "** with a " + dice)

    # POLL
    @commands.hybrid_command(name="poll")
    async def command_poll(self, context, name, options):
        """
        Starts a poll

        Use quotation marks if you want whole phrases as name/options.
        If just the poll name is given, options will be yes/no/maybe, otherwise
        each option will have a letter associated.

        ex:
        `<prefix>poll` "Is this a cool poll command?"
        `<prefix>poll` "Favourite icecream?" "chocolate strawberry banana concrete"
        """
        options = options.split()
        if len(options) <= 20:
            message = await context.send(embed=self.create_poll_embed(name, options))
            await self.react_with_options(message, options)
        else:
            raise commands.TooManyArguments("Maximum number of options is 20")

    ################
    # ERROR HANDLING
    ################

    @command_hi.error
    async def hi_on_error(self, context, error):
        """command_hi error handling"""
        bot_message = f"`{context.prefix}{context.invoked_with}` takes no arguments"
        await self.generic_error_handler(
            context,
            error,
            (
                commands.MissingRequiredArgument,
                commands.CommandOnCooldown,
                commands.NoPrivateMessage,
                commands.CheckFailure,
            ),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
        )

    @command_dice.error
    async def dice_on_error(self, context, error):
        """command_dice error handling"""
        bot_message = (
            f"`{context.prefix}{context.invoked_with}` either takes no arguments or"
            " one of the following: %s" % (", ".join(converters.DICES))
        )
        await self.generic_error_handler(
            context,
            error,
            (
                commands.MissingRequiredArgument,
                commands.CommandOnCooldown,
                commands.NoPrivateMessage,
                commands.CheckFailure,
            ),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
        )

    @command_poll.error
    async def poll_on_error(self, context, error):
        """command_poll error handling"""
        missing_argument = (
            f"`{context.prefix}{context.invoked_with}` "
            f"requires a poll name/description"
        )
        bot_message = (
            f"`{context.prefix}{context.invoked_with}` takes a maximum of 20 options"
        )
        await self.generic_error_handler(
            context,
            error,
            (
                commands.CommandOnCooldown,
                commands.NoPrivateMessage,
                commands.CheckFailure,
            ),
            (commands.TooManyArguments, bot_message),
            (commands.BadArgument, bot_message),
            (commands.MissingRequiredArgument, missing_argument),
        )
