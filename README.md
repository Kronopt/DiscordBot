# DiscordBot
[![build status](https://github.com/Kronopt/DiscordBot/workflows/CI/badge.svg "build status")](https://github.com/Kronopt/DiscordBot/actions?query=workflow%3ACI)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/Kronopt/DiscordBot)](https://github.com/Kronopt/DiscordBot/blob/master/LICENSE)
[![known vulnerabilities](https://snyk.io/test/github/Kronopt/DiscordBot/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/Kronopt/DiscordBot?targetFile=requirements.txt)

A Discord Bot

#### Install Dependencies
* Python 3.9
* `pip install -r requirements.txt`
* `pyppeteer-install` (command becomes available after installing python dependencies)

#### How to run
* Download this repo
* Install dependencies
* Create a `bot` [here](https://discordapp.com/developers/applications/me) and then create an `app bot user`
(on the same page)
* Use the `BOT_TOKEN` provided there
* Run `python discord_bot.py <BOT_TOKEN>` on the root of the repo
* Add the bot to a server using discord

note: on linux you might need to pass an extra parameter to discord_bot.py: `-gaming_cog=--no-sandbox`

## Commands

### Funny

| command | descripion |
| ------- | ---------- |
| `!8ball <str phrase>` | "Predicts" the outcome of a question |
| `!dick` | Reveals user's dick size |
| `!joke` | Tells a random (bad) joke |
| `!joke tts` | Reads joke using tts |
| `!poop [int n]` | Sends n poops |

### Gaming

| command | descripion |
| ------- | ---------- |
| `!awesomenaut rank <str player_name>` | Displays rank information of an Awesomenaut's player |
| `!gamedeal <str game_name>` | Displays game pricing info |

### General

| command | descripion |
| ------- | ---------- |
| `!dice [str dice]` | Rolls one of the following dices: d4, d6, d8, d10, d12 and d20 |
| `!hi` | Greets user |
| `!poll` | Starts a poll|

### Info

| command | descripion |
| ------- | ---------- |
| `!info` | Shows bot author, relevant frameworks used and github page |
| `!system` | Shows bot host system information |

### XKCD Comics

| command | descripion |
| ------- | ---------- |
| `!xkcd` | Shows a random xkcd comic |
| `!xkcd id <number id>` | Shows the selected xkcd comic |
| `!xkcd latest` | Shows the latest xkcd comic |

### Help

| command | descripion |
| ------- | ---------- |
| `!help [command] [subcommand]` | Shows command help message |
