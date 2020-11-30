#!python3
# coding: utf-8


"""
Bot main .py file
A small command line utility is available so that the bot's token is not hardcoded in the script
"""


import argparse
import logging
import os
from DiscordBot.Bot import Bot


if __name__ == '__main__':
    # command line handling
    cli = argparse.ArgumentParser(description='Run Discord Bot')
    cli.add_argument('token', help='Bot token')
    cli.add_argument('--setup-extra', action='store_true',
                     help='Whether to setup/download external bot dependencies or not')
    cli = cli.parse_args()

    # logging handling
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    logger = logging.getLogger('DiscordBot.main')

    # extra dependencies
    if cli.setup_extra:
        logger.info('Downloading and setting up external dependencies...')
        os.system('pyppeteer-install')

    # run bot
    logger.info('Starting bot')
    Bot(prefix='!', intents=None).run(cli.token)
    logger.info('Shutting down bot complete')
