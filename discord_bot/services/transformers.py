#!python3
# coding: utf-8

"""
Converters convert the arguments of a command
"""


import discord
from discord import app_commands


class PositiveInteger(app_commands.Transformer):
    """verifies if an argument is a positive int"""

    async def transform(self, interaction: discord.Interaction, value: str) -> int:
        if value.isdecimal() and int(value) > 0:
            return int(value)
        raise ValueError(f"{value} is not a valid positive integer")
