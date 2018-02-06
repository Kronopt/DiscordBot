#!python3
# coding: utf-8

"""
Types to which to convert the arguments of a command (or functions that convert strings) can be found here.
"""


class Dice:
    dices = ('d4', 'd6', 'd8', 'd10', 'd12', 'd20')

    def __init__(self, value):
        if hasattr(value, "lower") and value.lower() in self.dices:
            self.dice = value
        else:
            raise ValueError(str(value) + ' is not a valid dice')

    def __repr__(self):
        return self.dice


def number(cls, value):
    try:
        value = float(value)
    except ValueError:
        raise ValueError(str(value) + ' is not a valid number')

    # ex: for 7.0 return 7
    # ex: for 3.4 return 3.4
    return int(value) if int(value) == value else value
