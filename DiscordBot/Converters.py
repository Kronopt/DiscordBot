#!python3
# coding: utf-8

"""
Converters convert the arguments of a command.
"""

DICES = ('d4', 'd6', 'd8', 'd10', 'd12', 'd20')


def dice(argument):
    if hasattr(argument, "lower") and argument.lower() in DICES:
        return argument
    else:
        raise ValueError(str(argument) + ' is not a valid dice')


def number(argument):
    try:
        value = float(argument)
    except ValueError:
        raise ValueError(str(argument) + ' is not a valid number')
    else:
        # ex: for 7.0 return 7
        # ex: for 3.4 return 3.4
        return int(value) if int(value) == value else value
