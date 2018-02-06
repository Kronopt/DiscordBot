# DiscordBot
A Discord Bot (**WIP**)

#### Install Dependencies
* Python 3.6
* `pip install discord.py`

#### How to run
* Download this repo
* Create a bot [here](https://discordapp.com/developers/applications/me) and then create an app bot user
(on the same page)
* Use the BOT_TOKEN provided there
* Run `python DiscordBot.py <BOT_TOKEN>` on the root of the repo
* Add the bot to a server using discord

#### Commands
* `!help`
  * Bot shows the available commands
* `!ping`
  * Bot answers with `pong`
* `!dice <str dice>`
  * Bot rolls one of the specified d4, d6, d8, d10, d12 and d20 dices
* `!random`
  * Bot generates a number between 0 and 1 (inclusive)
* `!random_between <int a> <int b>`
  * Bot generates a number between a and b (inclusive)
* `!random_from <str a> <str b> ...`
  * Bot randomly selects one of the space arguments
* `!sum <number a> <number b> ...`
  * Bot sums all numbers
* `!subtract <number a> <number b> ...`
  * Bot subtracts all numbers
* `!divide <number a> <number b> ...`
  * Bot divides all numbers
* `!multiply <number a> <number b> ...`
  * Bot multiplies all numbers
* `!8ball <str> ...`
  * Bot uses its fortune-telling powers to answer your question
