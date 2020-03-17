from deuces.deck import Deck
from deuces.card import Card
from discord.ext import commands
from player import Player


class Poker(commands.Cog):

    # deck = Deck()

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poker(self, ctx):
        deck = Deck()
        board = deck.draw(3)
        Card.print_pretty_cards(board)
        players = ctx.guild.members
        activePlayers = []
        i = 0
        for player in players:
            print(player.status)
            if player.status.value == "online" and (not player.bot):
                print(player)
                await player.send("Your are part of a poker game!")
                activePlayers.append(Player(player.display_name, deck.draw(2), player))
                await player.send(Card.print_pretty_cards(activePlayers[i].hand))
                i += 1

        if activePlayers.__len__() < 2:
            await ctx.send("You need at least two players to start a poker game")

        i = 0
        while activePlayers.__len__() > 1:
            i %= activePlayers.__len__()
            await ctx.send("It is {0}'s turn".format(activePlayers[i].name))

            def check(m):
                # Could display name and actual name be diff?
                return (m.content == 'fold' or m.content == 'raise') and m.author == activePlayers[i].name

            decision = await ctx.bot.wait_for('message', check=check)
            print(decision)
            i += 1


def setup(bot):
    bot.add_cog(Poker(bot))
