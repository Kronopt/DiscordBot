#!python3
# coding: utf-8

"""
Bot main .py file.
A small command line utility is available so that the bot's token is not hardcoded in the script.
"""

import argparse
from DiscordBot.Commands_re import BOT


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description='Run Discord Bot')
    cli_parser.add_argument('token', help='Bot token')
    cli_parser = cli_parser.parse_args()

    BOT.run(cli_parser.token)


# TODO setup logging (log command calls, etc)
