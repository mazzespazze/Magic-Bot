# Work with Python 3.6
import random
TOKEN = 'NDkzNzA5NDAxMzgzNzYzOTY5.Doo7fw.n0VDx3djJKFq6Cer8Kh0x5mutzs'

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
        if x in tmp:
            continue
        for y in players:
            if y in tmp:
                continue
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

""" Starting commands written by @Matteo Ghetti (matteo.ghetti@nonorank.com)"""
@bot.command()
async def first(ctx):
    """ This has to be the first interaction with the bot:
        creating the players objects and setting the scores to 0, and eventually
        even the pass if it occurs (odd number of players).
        @ctx has to be a string in the form: A,B,C,D ~> !first A,B,C,D,E
        """
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
            P1, P2 = REAL_PLAYERS[x], REAL_PLAYERS[x+1]
            MATCH += P1.get_name() + " vs " + P2.get_name() + "\n"
            #adding fights to each player
            P1.add_fight(P2)
            P2.add_fight(P1)
    await bot.say(MATCH)

@bot.command()
async def set_scores(ctx):
    """ @ctx has to be a valid string in the form: (A,B)=2-0;(C,D)=2-1;(E,F)=0-2 ...
        Furthermore it is able to find a player from a name """
    global REAL_PLAYERS
    scores = ctx.strip().split(";")
    for match in scores:
        M = match.split("=")
        P1_P2, ACTUAL_SCORE = M[0].replace("(","").replace(")","").split(","), M[1].strip()
        pp = p.find_players(REAL_PLAYERS, P1_P2)
        if ACTUAL_SCORE == '2-0':   pp[0].add_points(3)
        elif ACTUAL_SCORE == '2-1':
            pp[0].add_points(2)
            pp[1].add_points(1)
        elif ACTUAL_SCORE == '0-2': pp[1].add_points(3)
        elif ACTUAL_SCORE == '1-2':
            pp[0].add_points(1)
            pp[1].add_points(2)

@bot.command()
async def next(ctx):
    """ It decides which player goes against in the next round:
        @CONSTRAINT 1: the pass should not given twice to the same player
        @CONSTRAINT 2: two players should not match twice """
    global REAL_PLAYERS



@bot.command()
async def reset():
    """ It resets whatever it happened"""
    global REAL_PLAYERS
    for x in REAL_PLAYERS:
        x = Player(x.get_name())
    await bot.say("I have resetted all players as from the start :) ")

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

""" Some fun utilities / functions that just add flavour but do not add anything
    for a tournament """
@bot.command()
async def sets(ctx):
    """ It prints to discord a random choice of sets """
    await bot.say(get_sets(int(ctx.strip())))

@bot.command()
async def duel_deck(ctx):
    """ It gives a random set of duel_decks assigning the players to it"""
    await bot.say(get_duel_decks(ctx.strip()))

@bot.command()
async def roll(ctx):
    """ It rolls a dice within a given integer"""
    n = int(ctx.strip())
    if n <= 0: n = 1
    await bot.say(r.randint(1,n))

bot.run(TOKEN)
