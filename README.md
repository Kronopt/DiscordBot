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
| `!dice [str dice]` | Rolls one of the following dices: d4, d6, d8, d10, d12 and d20 |
| `!random` | Generates a number between 0 and 1 (inclusive) |
| `!random between <int a> <int b>` | Generates a number between a and b (inclusive) |
| `!random from <str args> ...` | Randomly selects one of the space separated arguments |

### Math

| command | descripion |
| ------- | ---------- |
| `!sum <number args> ...` | Sums all given numbers |
| `!subtract <number args> ...` | Subtracts all given numbers |
| `!divide <number args> ...` | Divides all given numbers |
| `!multiply <number args> ...` | Multiplies all given numbers |

### Funny

| command | descripion |
| ------- | ---------- |
| `!8ball <str args> ...` | Uses its fortune-telling powers to answer your question |
| `!poop [number n]` | Sends n poops |
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
| `!xkcd id <number id>` | Shows the requested xkcd comic, if it exists |

### Awesomenauts

| command | descripion |
| ------- | ---------- |
| `!awesomenaut <str awesomenaut_name>` | Displays information of the specified awesomenaut. |
| `!awesomenaut rank <str player_name>` | Displays rank information of an Awesomenaut's player. |

### Info

| command | descripion |
| ------- | ---------- |
| `!help [str command]` | Shows all available commands or detailed info on a given command |
| `!info` | Shows bot author, relevant frameworks used and github page |