import os
import config

from discord.ext import commands

bot = commands.Bot(command_prefix=config.prefix)


@bot.event
async def on_ready():
    print("ready")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(config.token_secret)
