# Work with Python 3.6
import random, math
TOKEN = 'YOUR_TOKEN'

import discord
from discord.ext import commands
import random as r
import player as p
from sets import *

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''
REAL_PLAYERS, TURNS = list(),1
bot = commands.Bot(command_prefix='!', description=description)


def winner():
    """ Stating the winner!"""
    global REAL_PLAYERS
    STRING, winner = "", REAL_PLAYERS[0].get_name()
    STRING = "\t\tWinner is " + winner + "!! with "+ str(REAL_PLAYERS[0].get_points()) +" points\n\t\tFollowed by:\n"
    for x in range(1,len(REAL_PLAYERS)):
        STRING += str(x+1) + ") " + REAL_PLAYERS[x].get_name() + " with " + str(REAL_PLAYERS[x].get_points())+ " points\n"
    return STRING

def pretty_printing(turn):
    """ Given a list of players, we create the string that discord bot will then
        print: a list of matches split into their rooms with two players fighting
        each other. Plus the PASS if odd number of players occurs """
    global REAL_PLAYERS
    MATCH, ROOM = "TURN: " + str(turn) + "\n", 1
    for x in range(0,len(REAL_PLAYERS),2):
        if x + 1 >= len(REAL_PLAYERS):
            MATCH += REAL_PLAYERS[x].get_name() + " gets the PASS"
            REAL_PLAYERS[x].set_pass()
        else:
            MATCH += "ROOM " + str(ROOM) + ":\t"
            ROOM+=1
            P1, P2 = REAL_PLAYERS[x], REAL_PLAYERS[x+1]
            MATCH += P1.get_name() + " vs " + P2.get_name() + "\n"
            #adding fights to each player
            P1.add_fight(P2)
            P2.add_fight(P1)
    return MATCH

""" Starting bot interactions """
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

""" Starting commands written by @Matteo Ghetti (matteo.ghetti@nonorank.com)"""
@bot.command()
async def names(ctx):
    """ This has to be the first interaction with the bot:
        creating the players objects and setting the scores to 0, and eventually
        even the pass if it occurs (odd number of players).
        @ctx has to be a string in the form: A,B,C,D ~> !first A,B,C,D,E
        """
    players = ctx.strip().split(",")
    global REAL_PLAYERS, TURNS
    for pl in players:
        REAL_PLAYERS.append(p.Player(pl)) #creating players
    random.shuffle(REAL_PLAYERS) #random shuffle since is the first time
    await bot.say(pretty_printing(TURNS))

@bot.command()
async def set_scores(ctx):
    """ @ctx has to be a valid string in the form: (A,B)=2-0;(C,D)=2-1;(E,F)=0-2 ...
        Furthermore it is able to find a player from a name """
    global REAL_PLAYERS, TURNS
    TURNS += 1
    scores = ctx.strip().split(";")
    for match in scores:
        M = match.split("=")
        P1_P2, ACTUAL_SCORE = M[0].replace("(","").replace(")","").split("-"), M[1].strip()
        #pp = p.find_players(REAL_PLAYERS, P1_P2)
        P1 = p.find_player(REAL_PLAYERS, P1_P2[0])
        P2 = p.find_player(REAL_PLAYERS, P1_P2[1])
        if ACTUAL_SCORE == '2-0':
            P1.add_points(3)
        elif ACTUAL_SCORE == '2-1':
            P1.add_points(2)
            P2.add_points(1)
        elif ACTUAL_SCORE == '0-2':
            P2.add_points(3)
        elif ACTUAL_SCORE == '1-2':
            P1.add_points(1)
            P2.add_points(2)
    """ Now the scores are done """
    if TURNS > math.ceil(math.log(len(REAL_PLAYERS))/math.log(2)):
        REAL_PLAYERS = p.sorted_players_for_ranking(REAL_PLAYERS)
        await bot.say(winner())
    else:
        PLAYING = p.sorted_players_for_playing(REAL_PLAYERS)
        flatten_list = list()
        """ we transform the list of tuples into a list """
        for pl in PLAYING:
            if type(pl) is tuple:
                flatten_list += [pl[0], pl[1]]
            else:
                flatten_list.append(pl)
        print("Flatten List:\t",flatten_list)
        REAL_PLAYERS = flatten_list
        STRING = pretty_printing(TURNS)
        await bot.say(STRING)


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
