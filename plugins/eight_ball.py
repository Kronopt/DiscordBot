#!python2
# coding: utf-8

import random
from disco.bot import Plugin


class EightBall(Plugin):

    def load(self, ctx):
        super(EightBall, self).load(ctx)
        self.answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes",
                        "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                        "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no",
                        "My sources say no", "Outlook not so good", "Very doubtful"]
        self.emojis = [":white_check_mark:", ":low_brightness:", ":x:"]

    def unload(self, ctx):
        super(EightBall, self).unload(ctx)

    @Plugin.command('8ball', '<content:str...>')
    def on_8ball_command(self, event, content):
        answer = random.randint(0, len(self.answers) - 1)

        if answer <= 9:  # Affirmative answer
            emoji = self.emojis[0]
        elif answer <= 14:  # Meh answer
            emoji = self.emojis[1]
        else:  # Negative answer
            emoji = self.emojis[2]
        event.msg.reply("`" + content + "`: " + self.answers[answer] + " " + emoji)
