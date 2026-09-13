import sys
import discord


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
