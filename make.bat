@echo off

if "%1" == "" goto help
goto %~1

:help
echo install-dependencies           installs python dependencies
echo install-extra-dependencies     install extra dependencies
echo testbot                        runs bot on test bot account, for testing
echo bot                            runs bot on main bot account, in production
goto:eof

:install-dependencies
python -m pip install -r requirements.txt
goto:eof

:install-extra-dependencies:
pyppeteer-install
goto:eof

:testbot
python DiscordBot.py %TEST_TOKEN%
goto:eof

:testbot
python DiscordBot.py %BOT_TOKEN% -gaming_cog=--no-sandbox
goto:eof
