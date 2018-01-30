#!python2
# coding: utf-8

import random
from disco.bot import Plugin


class RandomNumberGenerators(Plugin):

    def load(self, ctx):
        super(RandomNumberGenerators, self).load(ctx)
        self.dices = ("d4", "d6", "d8", "d10", "d12", "d20")

    def unload(self, ctx):
        super(RandomNumberGenerators, self).unload(ctx)

    @Plugin.command('dice', '<content:str...>')
    def on_dice_command(self, event, content):
        if content.lower() in self.dices:
            dice_number = int(content[1:])
            dice_roll = str(random.randint(1, dice_number))
            event.msg.reply("Rolled a **" + dice_roll + "** with a " + content)
        else:
            event.msg.reply("Can't throw " + content + ". \nThrow one of the following dices: " + ", ".join(self.dices))

    @Plugin.command('random')
    def on_random_command(self, event):
        random_number = random.random()
        event.msg.reply("Result: **" + str(random_number) + "**")

    @Plugin.command('random_between', '<a:int> <b:int>')
    def on_random_between_command(self, event, a, b):
        values = [a, b]
        values.sort()  # Either value can be the smallest one
        random_number = random.randint(values[0], values[1])
        event.msg.reply("Result: **" + str(random_number) + "**")

    @Plugin.command('random_from', '<content:str...>')
    def on_random_from_command(self, event, content):
        result = random.choice(content.split())
        event.msg.reply("Result: **" + result + "**")
