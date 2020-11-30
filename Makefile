.PHONY: help install-dependencies testbot bot

help:
	@echo "install-dependencies         installs dependencies"
	@echo "testbot                      runs bot on test bot account"
	@echo "bot                          runs bot on main bot account"

install-dependencies:
	python -m pip install -r requirements.txt

testbot:
	python DiscordBot.py $TEST_TOKEN --setup-extra

bot:
	python DiscordBot.py $BOT_TOKEN --setup-extra
