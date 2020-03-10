import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Deku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deku(self, ctx):
        NUMOFGAMES = 11;
        name = []
        oldPrice = []
        newPrice = []
        description = ''
        try:
            page = requests.get('https://www.dekudeals.com/')
        except requests.exceptions.RequestException as error:
            return await ctx.send(error)
        soup = BeautifulSoup(page.content, 'html.parser')
        for i in range(NUMOFGAMES):
            name.append(soup.find_all('div', class_='h6 name')[i].get_text())
            oldPrice.append(soup.find_all('s', class_='text-muted')[i].get_text())
            newPrice.append(soup.find_all('strong')[i].get_text())
        for i in range(NUMOFGAMES):
            description += str(i+1) + '. ' + (name[i])[1:] + '~~' + oldPrice[i] + '~~ -> ' + newPrice[i] + '\n\n'
        embed = discord.Embed(
            title='Deku Deals',
            color=discord.Color.blue(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            description +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        embed.set_footer(text='The information is based on Deku Deals', icon_url='https://www.dekudeals.com/assets/icon-400019e14b2bf320aff98e242053047b6fba48d0ed50e91ff4748fd697de4e95.png')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Deku(bot))
