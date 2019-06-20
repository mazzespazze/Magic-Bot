# Work with Python 3.6
import random


import discord
from discord.ext import commands
import random as r
import player as p
from sets import *

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''
REAL_PLAYERS, TURNS = list(),1
bot = commands.Bot(command_prefix='!', description=description)

""" Starting my functions """

def splitter(l): return [x.strip().lower() for x in l.split(",")]

def fillPlayers(m,players):
    """ Given a string it fill is the player and the last one gets
        a pass in case of odd number of players """
    for x in splitter(m):
        players = players + [p.Player(x)]
    r.shuffle(players)
    if len(players) % 2 != 0: players = players + [p.Player("PASS")]
    return players

def firstTime(players, msg, i=0):
    """ It """
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
    """ It starts a new game! """
    global players,turns
    players = fillPlayers(ctx,players)
    print(players)
    players, msg = firstTime(players,"Turn " + str(turns) + "\t")
    print(players)
    await bot.say(msg)

@bot.command()
async def first(ctx):
    """global players,turns
    for x in splitter(ctx):
        tmp_name,score = x.split(":")[0].strip(), int(x.split(":")[1].strip())
        for i in range(len(players)): #assigning the score
            if players[i].name == tmp_name:
                players[i].addPoints(score)
    players = sorted(players, key= lambda x: x.points, reverse=True)
    turns += 1
    print(turns,players,len(players))
    if (turns+1) == len(players)/2:
        await bot.say("WINNER:\t" + str(prettyPrinting()))
    else:
        players,msg = new_round(players)
        await bot.say("Turn "+ str(turns)+"\t"+msg)"""
    players = ctx.strip().split(",")
    global REAL_PLAYERS, TURNS
    for pl in players:
        REAL_PLAYERS.append(p.Player(pl))
    random.shuffle(REAL_PLAYERS)
    MATCH, GAME = "TURN: " + str(TURNS) + "\n", 1
    for x in range(0,len(REAL_PLAYERS),2):
        if x + 1 >= len(REAL_PLAYERS):
            MATCH += REAL_PLAYERS[x].get_name() + " gets the PASS"
            REAL_PLAYERS[x].set_pass()
        else:
            MATCH += "GAME " + str(GAME) + ":\t"
            GAME+=1
            MATCH += REAL_PLAYERS[x].get_name() + " vs " + REAL_PLAYERS[x+1].get_name() + "\n"
    await bot.say(MATCH)

@bot.command()
async def reset():
    global players
    players = [p.Player(x.name) for x in players]
    await bot.say(prettyPrinting())

@bot.command()
async def roll(ctx):
    n = int(ctx.strip())
    if n <= 0: n = 1
    await bot.say(r.randint(1,n))



@bot.command()
async def rank():
    """ Printing the ranking of the current players"""
    global REAL_PLAYERS
    SHOW, RANK = "", 1
    SORTED = p.sorted_players_for_ranking(REAL_PLAYERS)
    for pl in SORTED:
        SHOW += str(RANK) + ")\t" + str(pl) + "\n"
        RANK += 1
    await bot.say(SHOW)

""" Some fun utilities / functions """
@bot.command()
async def sets(ctx):
    await bot.say(get_sets(int(ctx.strip())))

@bot.command()
async def duel_deck(ctx):
    await bot.say(get_duel_decks(ctx.strip()))

bot.run(TOKEN)
