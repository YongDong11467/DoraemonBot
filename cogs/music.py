import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send('You are not connected to a voice channel.')
            return
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.send(f'Joined {channel}')


def setup(bot):
    bot.add_cog(Music(bot))