import asyncio
import time
import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
        embed.set_image(url=img)
        embed.set_footer(text='The information is based on Animal Crossing Wiki')
        return await ctx.send(embed=embed)

    # German villager
    @commands.command()
    async def gvillager(self, ctx, arg):
        info = []
        try:
            page = requests.get('https://animalcrossing.fandom.com/de/wiki/' + arg)
        except requests.exceptions.RequestException as error:
            return await ctx.send(error)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            img = soup.find('img', class_='pi-image-thumbnail').get('src')
        except AttributeError:
            return await ctx.send('Enter a valid villager.')
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
        embed.set_image(url=img)
        embed.set_footer(text='The information is based on Animal Crossing Wiki')
        return await ctx.send(embed=embed)

    @commands.command()
    async def nook(self, ctx, arg):
        browser = webdriver.Chrome(executable_path='C:/Users/Tina/Documents/chromedriver_win32/chromedriver.exe')
        items = []
        id = []
        listing = []
        seller = []
        price = []
        description = ''
        browser.get('https://nookazon.com/products?search=' + arg)
        try:
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'item-img-container'))
            )
            html = browser.page_source
        except TimeoutException:
            return await ctx.send("Timed out waiting for page to load")
        finally:
            browser.quit()

        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find_all('div', class_='sc-fzoXzr eyWNWx')
        productURL = soup.find_all('a', class_='sc-AxjAm kCLLqI item-img')
        if len(name) > 0:
            for i in range(len(name)):
                items.append(name[i].get_text())
                id.append(productURL[i].get('href'))
        else:
            return await ctx.send('No result.')
        for i in range(len(name)):
            description += str(i + 1) + '. ' + items[i] + '\n'
        embed = discord.Embed(
            title='Nookazon',
            color=discord.Color.green(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            description +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        embed.set_footer(text='The information is based on Nookazon')
        await ctx.send(embed=embed)
        await ctx.send('Enter the number of the item.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        try:
            answer = await self.bot.wait_for('message', check=is_correct, timeout=10)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, timed out')

        if 0 < int(answer.content) <= len(name):
            browser = webdriver.Chrome(executable_path='C:/Users/Tina/Documents/chromedriver_win32/chromedriver.exe')
            itemName = items[int(answer.content) - 1]
            browser.get('https://nookazon.com' + id[int(answer.content) - 1])
        else:
            return await ctx.send('Error: Please restart and enter a valid number')

        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'listing-product-info'))
            )
            html = browser.page_source
        except TimeoutException:
            return await ctx.send("Timed out waiting for page to load")
        finally:
            browser.quit()

        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find('div', class_='product-img').img['src']
        listingProduct = soup.find_all('div', class_='listing-product-info')
        if len(listingProduct) > 0:
            # item name
            for i in soup.select(".listing-product-info > :nth-child(1) > :nth-child(1)"):
                listing.append(i.get_text())
            # discord username
            for i in soup.select(
                    ".listing-product-info > :nth-child(1) > :nth-child(2) > :nth-child(1)"):
                seller.append(i.get_text())
            # price
            for i in soup.select(
                    ".listing-product-info > :nth-child(1) > :nth-child(3) > :nth-child(1) > "
                    ":nth-child(1) > :nth-child(1)"):
                price.append(i.get_text())
        else:
            return await ctx.send('No Listing Currently.')

        description = ''
        if len(listingProduct) > 10:
            num = 10
        else:
            num = len(listingProduct)
        for i in range(num):
            description += str(i+1) + '. ' + listing[i] + '- ' + (seller[i])[:-1] + ': ' + \
                           price[i].replace('\n', ' ') + '\n'

        embed = discord.Embed(
            title=itemName,
            color=discord.Color.green(),
            description=
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n' +
            description +
            '**▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**\n'
        )
        embed.set_thumbnail(url=img)
        embed.set_footer(text='The information is based on Nookazon')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimalCrossing(bot))
