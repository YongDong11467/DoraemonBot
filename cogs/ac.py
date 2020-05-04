import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class AnimalCrossing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def villager(self, ctx, arg):
        info = []
        try:
            page = requests.get('https://animalcrossing.fandom.com/wiki/' + arg)
        except requests.exceptions.RequestException as error:
            return await ctx.send(error)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            img = soup.find('img', class_='pi-image-thumbnail').get('src')
        except AttributeError:
            return await ctx.send('Enter a valid villager.')
        img = soup.find('img', class_='pi-image-thumbnail').get('src')
        for i in range(4):
            info.append(soup.find_all('div', class_='pi-data-value pi-font')[i].get_text())
        embed = discord.Embed(
            title=arg.capitalize(),
            color=discord.Color.green(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            'Gender: ' + info[0] + '\n' +
            'Personality: ' + info[1] + '\n' +
            'Species: ' + info[2] + '\n' +
            'Birthday: ' + info[3] + '\n' +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        embed.set_image(url= img)
        embed.set_footer(text='The information is based on Animal Crossing Wiki')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimalCrossing(bot))