from discord.ext import commands
from bs4 import BeautifulSoup


class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Pokemon(bot))
