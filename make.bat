@echo off

if "%1" == "" goto help
goto %~1

:help
echo install-dependencies           installs dependencies
echo testbot                        runs bot on test bot account
echo bot                            runs bot on main bot account
goto:eof

:install-dependencies
python -m pip install -r requirements.txt
goto:eof

:testbot
python DiscordBot.py %TEST_TOKEN% --setup-extra
goto:eof

:testbot
python DiscordBot.py %BOT_TOKEN% --setup-extra
goto:eof
