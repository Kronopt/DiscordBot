#!python2
# coding: utf-8

from disco.bot import Plugin


class Ping(Plugin):

    def load(self, ctx):
        super(Ping, self).load(ctx)

    def unload(self, ctx):
        super(Ping, self).unload(ctx)

    @Plugin.command('ping')
    def on_ping_command(self, event):
        event.msg.reply('pong')
