import sys
import discord


def when_mentioned(bot, message):
    """Mirrors discord.ext.commands.when_mentioned's shape; bot.py only
    passes it as command_prefix, never calls it in tests."""
    return [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]


class Bot:
    def __init__(self, command_prefix="!", intents=None):
        self.command_prefix = command_prefix
        self.intents = intents
        self.tree = discord.app_commands.CommandTree(self)
        self.user = discord.User(id=999999999999999999)

    async def setup_hook(self):
        pass

    async def close(self):
        pass

    def run(self, token):
        raise RuntimeError("fake bot: run() should not be called in tests")

    def event(self, fn):
        setattr(self, fn.__name__, fn)
        return fn
