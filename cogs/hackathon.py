import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup


class Hackathon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mlh(self, ctx):
        description = ''
        try:
            page = requests.get('https://mlh.io/seasons/na-2020/events')
        except requests.exceptions.RequestException as error:
            return await ctx.send(error)
        soup = BeautifulSoup(page.content, 'html.parser')
        current = soup.find_all('div', class_='row')[1]
        hacks = [h.get_text() for h in current.find_all('h3', class_='event-name')]
        date = [d.get_text() for d in current.find_all('p', class_='event-date')]
        location = [l.get_text() for l in current.find_all('div', class_='event-location')]
        url = [u['href'] for u in current.find_all('a', href=True)]
        for i in range(len(hacks)):
            description += str(i + 1) + '. ' + hacks[i] + '\n' + date[i] + '\n' + \
                           (location[i].replace(' ', '')).replace('\n', '') + '\n' + url[i] + '\n\n'
        embed = discord.Embed(
            title='MLH',
            color=discord.Color.orange(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            description +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        embed.set_footer(text='The information is based on MLH', icon_url='https://pbs.twimg.com/profile_images/1184141979493568515/NMa0vlIb_200x200.jpg')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Hackathon(bot))
