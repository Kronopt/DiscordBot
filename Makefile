.PHONY: help install-dependencies install-dev-dependencies install-extra-dependencies lint test-bot bot

help:
	@echo "install-dependencies         installs python dependencies"
	@echo "install-dev-dependencies     installs python dev dependencies"
	@echo "install-extra-dependencies   install extra dependencies"
	@echo ""
	@echo "lint                         runs linter"
	@echo ""
	@echo "test-bot                     runs bot on test bot account, for testing"
	@echo "bot                          runs bot on main bot account, in production"

install-dependencies:
	python -m pip install -r requirements.txt

install-dev-dependencies:
	python -m pip install -r requirements-dev.txt

install-extra-dependencies:
	pyppeteer-install

lint:
	python -m pylint DiscordBot DiscordBot.py
	python -m black --check .

test-bot:
	python DiscordBot.py ${DISCORD_BOT_TEST_TOKEN} -isthereanydeal_token=${ISTHEREANYDEAL_TOKEN}

bot:
	python DiscordBot.py ${DISCORD_BOT_TOKEN} -chromium_args=--no-sandbox -isthereanydeal_token=${ISTHEREANYDEAL_TOKEN}
