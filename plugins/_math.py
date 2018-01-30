#!python2
# coding: utf-8

from disco.bot import Plugin


class _Math(Plugin):

    def load(self, ctx):
        super(_Math, self).load(ctx)

    def unload(self, ctx):
        super(_Math, self).unload(ctx)

    @staticmethod
    def is_natural(number):
        # ex: for 7.0 return 7
        # ex: for 3.4 return 3.4
        return int(number) if int(number) == number else number

    @Plugin.command('sum', '<a:float> <b:float>')
    def on_sum_command(self, event, a, b):
        a = self.is_natural(a)
        b = self.is_natural(b)
        result = self.is_natural(a + b)

        event.msg.reply(str(a) + " + " + str(b) + " = " + "**" + str(result) + "**")

    @Plugin.command('subtract', '<a:float> <b:float>')
    def on_subtract_command(self, event, a, b):
        a = self.is_natural(a)
        b = self.is_natural(b)
        result = self.is_natural(a - b)

        event.msg.reply(str(a) + " - " + str(b) + " = " + "**" + str(result) + "**")

    @Plugin.command('divide', '<a:float> <b:float>')
    def on_divide_command(self, event, a, b):
        try:
            result = self.is_natural(a / b)
        except ZeroDivisionError:
            return event.msg.reply(":warning: Can't divide by zero :warning:")

        a = self.is_natural(a)
        b = self.is_natural(b)

        event.msg.reply(str(a) + " / " + str(b) + " = " + "**" + str(result) + "**")

    @Plugin.command('multiply', '<a:float> <b:float>')
    def on_multiply_command(self, event, a, b):
        a = self.is_natural(a)
        b = self.is_natural(b)
        result = self.is_natural(a * b)

        event.msg.reply(str(a) + " * " + str(b) + " = " + "**" + str(result) + "**")
