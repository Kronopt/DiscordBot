# DiscordBot  (Work in Progress)
A Discord Bot

#### Install Dependencies
* Python 3.6
* `pip install -r requirements.txt`

#### How to run
* Download this repo
* Install dependencies
* Create a bot [here](https://discordapp.com/developers/applications/me) and then create an app bot user
(on the same page)
* Use the BOT_TOKEN provided there
* Run `python DiscordBot.py <BOT_TOKEN>` on the root of the repo
* Add the bot to a server using discord

## Commands

### General

| command | descripion |
| ------- | ---------- |
| `!ping` | Answers with `pong` |
| `!hi` | Greets user |
| `!dice <str dice>` | Rolls one of the specified d4, d6, d8, d10, d12 and d20 dices |
| `!random` | Generates a number between 0 and 1 (inclusive) |
| `!random between <int a> <int b>` | Generates a number between a and b (inclusive) |
| `!random from <str a> <str b> ...` | Randomly selects one of the space separated arguments |

### Math

| command | descripion |
| ------- | ---------- |
| `!sum <number a> <number b> ...` | Sums all given numbers |
| `!subtract <number a> <number b> ...` | Subtracts all given numbers |
| `!divide <number a> <number b> ...` | Divides all given numbers |
| `!multiply <number a> <number b> ...` | Multiplies all given numbers |

### Funny

| command | descripion |
| ------- | ---------- |
| `!8ball <str> ...` | Uses its fortune-telling powers to answer your question |
| `!joke` | Tells a (bad) joke |

### Gifs

| command | descripion |
| ------- | ---------- |
| `!rickroll` | Shows a Rick Roll gif |
| `!ohgodno` | Shows "Oh God No" gif from 'The Office' |
| `!rekt` | Shows a rekt themed giff |

### Ascii Emojis

| command | descripion |
| ------- | ---------- |
| `!tableflip` | (╯°□°）╯︵ ┻━┻ |
| `!tableunflip` | ┬─┬ ノ(゜-゜ノ) |
| `!shrug` | ¯\\\_(ツ)_/¯ |

### XKCD Comics

| command | descripion |
| ------- | ---------- |
| `!xkcd` | Shows a random xkcd comic |
| `!xkcd latest` | Shows the latest xkcd comic |
| `!xkcd <number id>` | Shows the requested xkcd comic, if it exists |

### Info

| command | descripion |
| ------- | ---------- |
| `!help <command>` | Shows all available commands, detailed info on a given command or info on a given command group |
| `!info` | Shows bot author, relevant frameworks used and github page |