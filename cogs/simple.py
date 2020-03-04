from discord.ext import commands


class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Your ping is {round(self.bot.latency * 1000)} ms")


def setup(bot):
    bot.add_cog(Simple(bot))
