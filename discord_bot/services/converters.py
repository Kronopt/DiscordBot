#!python3
# coding: utf-8

"""
Converters convert the arguments of a command
"""

DICES = ("d4", "d6", "d8", "d10", "d12", "d20")


def dice(argument):
    """verifies if argument is a 'dice'"""
    if hasattr(argument, "lower") and argument.lower() in DICES:
        return argument
    raise ValueError(str(argument) + " is not a valid dice")


def positive_int(argument):
    """verifies if argument is a positive int"""
    if argument.isdecimal():
        return int(argument)
    raise ValueError(f"{argument} is not a valid positive integer")
