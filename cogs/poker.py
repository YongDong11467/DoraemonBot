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
                activePlayers.append(Player(player.name, deck.draw(2), player))
                await player.send(Card.print_pretty_cards(activePlayers[i].hand))
                i += 1

        if activePlayers.__len__() < 2:
            await ctx.send("You need at least two players to start a poker game")

        while activePlayers.__len__() > 1:
            #TODO track players in current round
            #TODO player specified raise
            #TODO track pot size

            roundPlayers = activePlayers.copy()
            i = 0
            pot = 0

            # Start of new round

            # track money in round to update at end
            gainLost = []
            for x in range(activePlayers.__len__()):
                gainLost.append(0)

            for x in range(3):

                curBid = 1000

                for roundPlayer in roundPlayers:
                    i %= roundPlayers.__len__()
                    await ctx.send("It is {0}'s turn".format(roundPlayer.name))

                    def check(m):
                        return (m.content == 'fold' or m.content == 'raise' or m.content == 'check') and m.author.name == roundPlayer.name

                    decision = await ctx.bot.wait_for('message', check=check)
                    print(decision.content)
                    if decision.content == 'fold':
                        roundPlayers.remove(roundPlayer)
                        if roundPlayers.__len__() == 1:
                            await ctx.send("{0} wins {1} this round".format(roundPlayers[0].name, pot))
                            break
                    elif decision.content == 'raise':
                        print('s')
                    elif decision.content == 'check':
                        gainLost[i] -= curBid
                        pot += curBid
                    else:
                        print('There a bug')
                    i += 1

                if roundPlayers.__len__() == 1:
                    break

            # Update money for the round
            for x in range(activePlayers.__len__()):
                activePlayers[x].chipSum += gainLost[x]

            # Check again for player that are out of the game
            for player in activePlayers:
                if player.chipSum <= 0:
                    activePlayers.remove(player)

def setup(bot):
    bot.add_cog(Poker(bot))
