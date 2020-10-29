#!python3
# coding: utf-8

"""
Converters convert the arguments of a command
"""

DICES = ('d4', 'd6', 'd8', 'd10', 'd12', 'd20')


def dice(argument):
    if hasattr(argument, "lower") and argument.lower() in DICES:
        return argument
    else:
        raise ValueError(str(argument) + ' is not a valid dice')


def positive_int(argument):
    try:
        value = int(argument)
    except ValueError:
        raise ValueError(str(argument) + ' is not a valid positive integer')
    else:
        if value < 1:
            raise ValueError(str(argument) + ' is not a valid positive integer')
        else:
            return value
