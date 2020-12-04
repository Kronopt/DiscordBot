.PHONY: help install-dependencies install-extra-dependencies testbot bot

help:
	@echo "install-dependencies         installs python dependencies"
	@echo "install-extra-dependencies   install extra dependencies"
	@echo "testbot                      runs bot on test bot account, for testing"
	@echo "bot                          runs bot on main bot account, in production"

install-dependencies:
	python -m pip install -r requirements.txt

install-extra-dependencies:
	pyppeteer-install

testbot:
	python DiscordBot.py ${TEST_TOKEN}

bot:
	python DiscordBot.py ${BOT_TOKEN} -gaming_cog=--no-sandbox
