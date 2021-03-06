#!python3
# coding: utf-8


"""
Bot main .py file
A small command line utility is available so that the bot's token is not hardcoded in the script
"""


import argparse
import logging
from DiscordBot.Bot import Bot


if __name__ == '__main__':
    # command line handling
    cli = argparse.ArgumentParser(description='Run Discord Bot')
    cli.add_argument('token', help='Bot token')
    cli.add_argument('-chromium_args', action='extend', nargs='*', default=[],
                     help='Chromium extra arguments')
    cli.add_argument('-isthereanydeal_token', help='IsThereAnyDeal API token')
    cli = cli.parse_args()

    # logging handling
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    logger = logging.getLogger('DiscordBot.main')

    # run bot
    logger.info('Starting bot')
    Bot(prefix='!',
        intents=None,
        chromium_args=cli.chromium_args,
        isthereanydeal_token=cli.isthereanydeal_token
        ).run(cli.token)
    logger.info('Shutting down bot complete')
