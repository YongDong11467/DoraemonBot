import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('Njg0NDkzNzc1NzkxNDU2Mjgy.Xl66lg.PQQmow4HY_1zlaJQyLUrsFlxM8Y')

