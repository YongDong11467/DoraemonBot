import discord


class Player:

    name = ""
    hand = []
    chipSum = 0
    ref = discord.Member

    def __init__(self, name, hand, ref):
        self.name = name
        self.hand = hand
        self.ref = ref
        self.chipSum = 10000