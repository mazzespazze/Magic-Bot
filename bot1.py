# Work with Python 3.6

TOKEN = None

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
from sets import get_sets

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''
players,turns = [],1
bot = commands.Bot(command_prefix='!', description=description)

""" Starting my functions """

def splitter(l): return [x.strip().lower() for x in l.split(",")]

def prettyPrinting(): return [str(x) for x in players]

def fillPlayers(m,players):
    #for x in list(filter(lambda x: x!='stern' and x!='jack',splitter(m))):
    for x in splitter(m):
        players = players + [p.Player(x)]
    r.shuffle(players)
    if len(players) % 2 != 0: players = players + [p.Player("PASS")]
    #return [p.Player("stern"),p.Player("jack")]+players
    return players

def firstTime(players, msg, i=0):
    if i < len(players):
        p1,p2 = players[i],players[i+1]
        msg = msg + str("\nRoom " + str(int(i/2)+1) + "\t" + p1.name + " ~ " + p2.name)
        p1.addFight(p2), p2.addFight(p1)
        players[i], players[i+1] = p1,p2
        return firstTime(players, msg, i + 2)
    return (players,msg)

def new_round(players,tmp=[]):
    msg,i = '',1
    for x in players:
        if x in tmp: continue
        for y in players:
            if y in tmp: continue
            if y.name!=x.name and y.name not in x.fights:
                msg = msg + str("\nRoom " + str(i) + "\t"+ x.name + " ~ " + y.name + "\t")
                x.addFight(y),y.addFight(x)
                i = i + 1
                tmp.append(x),tmp.append(y)
                break
    return(players,msg)


""" Starting bot interactions """
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def t(ctx):
    global players,turns
    players = fillPlayers(ctx,players)
    players, msg = firstTime(players,"Turn " + str(turns) + "\t")
    await bot.say(msg)

@bot.command()
async def s(ctx):
    global players,turns
    for x in splitter(ctx):
        tmp_name,score = x.split(":")[0].strip(), int(x.split(":")[1].strip())
        for i in range(len(players)): #assigning the score
            if players[i].name == tmp_name:
                players[i].addPoints(score)
    players = sorted(players, key= lambda x: x.points, reverse=True)
    turns += 1
    print(turns,players,len(players))
    if turns == len(players)/2:
        await bot.say("WINNER:\t" + str(prettyPrinting()))
    else:
        players,msg = new_round(players)
        await bot.say("Turn "+ str(turns)+"\t"+msg)

@bot.command()
async def reset():
    #for x in players: x = p.Player(x.name)
    global players
    players = [p.Player(x.name) for x in players]
    await bot.say(prettyPrinting())

@bot.command()
async def roll(ctx):
    n = int(ctx.strip())
    if n <= 0: n = 1
    await bot.say(r.randint(1,n))

@bot.command()
async def sets(ctx):
    await bot.say(get_sets(int(ctx.strip())))

@bot.command()
async def show():
    global players
    await bot.say(prettyPrinting())

bot.run(TOKEN)
