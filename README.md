# DiscordBot
[![build status](https://github.com/Kronopt/DiscordBot/workflows/CI/badge.svg "build status")](https://github.com/Kronopt/DiscordBot/actions?query=workflow%3ACI)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/Kronopt/DiscordBot)](https://github.com/Kronopt/DiscordBot/blob/master/LICENSE)
[![known vulnerabilities](https://snyk.io/test/github/Kronopt/DiscordBot/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/Kronopt/DiscordBot?targetFile=requirements.txt)

A Discord Bot

#### Install Dependencies
* Python 3.10
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
| `/8ball <str question>` | "Predicts" the outcome of a question |
| `/dick` | Reveals user's dick size |
| `/poop [int n]` | Sends n poops |
| `/joke [bool tts]` | Tells a random (bad) joke |

### Gaming

| command | descripion |
| ------- | ---------- |
| `/awesomenaut rank <str player>` | Displays rank information of an Awesomenaut's player |
| `/gamedeal <str name>` | Displays game pricing info |

### General

| command | descripion |
| ------- | ---------- |
| `/hi` | Greets user |
| `/dice [str die]` | Rolls a die |
| `/poll <str name> [str options]` | Starts a poll |

### Info

| command | descripion |
| ------- | ---------- |
| `/info` | Shows author, github page and framework |
| `/system` | Shows bot host system information |

### XKCD Comics

| command | descripion |
| ------- | ---------- |
| `/xkcd random` | Shows a random xkcd comic |
| `/xkcd latest` | Shows the latest xkcd comic |
| `/xkcd id <int id>` | Shows the selected xkcd comic |
