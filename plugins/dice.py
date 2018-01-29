#!python2
# coding: utf-8

import random
from disco.bot import Plugin


class Dice(Plugin):

    def load(self, ctx):
        super(Dice, self).load(ctx)
        self.dices = ("d4", "d6", "d8", "d10", "d12", "d20")

    def unload(self, ctx):
        super(Dice, self).unload(ctx)

    @Plugin.command('dice', '<content:str...>')
    def on_dice_command(self, event, content):
        if content.lower() in self.dices:
            dice_number = int(content[1:])
            dice_roll = str(random.randint(1, dice_number))
            event.msg.reply("Rolled a **" + dice_roll + "** with a " + content)
        else:
            event.msg.reply("Can't throw " + content + ". \nThrow one of the following dices: " + ", ".join(self.dices))
