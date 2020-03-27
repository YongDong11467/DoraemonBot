import time
import discord
from discord.ext import commands
import config
import requests


class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ss'])
    async def serverStatus(self, ctx):
        try:
            data = requests.get('https://api.mcsrvstat.us/2/' + config.my_server_ip)
        except requests.exceptions.RequestException as error:
            return await ctx.send(error)
        json = data.json()
        if json['online']:
            description = 'Server Status: Online' + '\n' + 'Player: ' + str(json['players']['online']) + ' / ' + \
                          str(json['players']['max']) + '\n' + 'Last Updated: ' + \
                          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(json['debug']['cachetime']))) + '\n'
        else:
            description = 'Server Status: Offline' + '\n' + 'Last Updated: ' + \
                          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(json['debug']['cachetime']))) + '\n'


        embed = discord.Embed(
            title='Minecraft Server Status',
            color=discord.Color.green(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            description +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Pokemon(bot))