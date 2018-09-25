# Work with Python 3.6

TOKEN = 'NDkzNzA5NDAxMzgzNzYzOTY5.Doo7fw.n0VDx3djJKFq6Cer8Kh0x5mutzs'

"""
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
#import chalk

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Yo")

@bot.event(pass_context=True)
async def ping(ctx):
    await bot.say("pong")
bot.run(TOKEN)
"""

import discord
from discord.ext import commands
import random as r
import player as p

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''
players = []
bot = commands.Bot(command_prefix='!', description=description)

""" Starting my functions """

splitter = lambda l: [x.strip() for x in l.split(",")]

def fillPlayers(m,players):
    for x in splitter(m): players = players + [p.Player(x.strip())]
    r.shuffle(players)
    if len(players) % 2 != 0: players = players + [p.Player("PASS")]
    return players

def firstTime(players, msg, i=0):
    if i < len(players):
        p1,p2 = players[i],players[i+1]
        msg = msg + str(p1.name + " ~ " + p2.name + "\t")
        p1.addFight(p2), p2.addFight(p1)
        players[i], players[i+1] = p1,p2
        return firstTime(players, msg, i + 2)
    return (players,msg)


""" Starting bot interactions """
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def t(ctx):
    global players
    players = fillPlayers(ctx,players)
    players, msg = firstTime(players,'Turn 1\t')
    await bot.say(msg)

#@bot.command()
#async def s(ctx):


bot.run(TOKEN)
