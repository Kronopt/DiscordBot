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


class Number:
    def __init__(self, value):
        if type(value) is Number:
            self.value = value.value
        else:
            try:
                value = float(value)
            except ValueError:
                raise ValueError(str(value) + ' is not a valid number')

            # ex: for 7.0 return 7
            # ex: for 3.4 return 3.4
            self.value = int(value) if int(value) == value else value

    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __truediv__(self, other):
        return Number(self.value / other.value)

    def __repr__(self):
        return str(self.value)
