# Work with Python 3.6
import discord
import player as p
import random as r
import asyncio
import operator
#from discord.ext import commands
#from discord.ext.commands import Bot

TOKEN = 'YOUR TOKEN'
splitter = lambda l: l[3:].split(",")
players = []
prettyPrinting = lambda x: [str(x) for x in players]
# Initialization of the players with a randomized start
def fillPlayers(m,players):
    for x in splitter(m):
        players = players + [p.Player(x.strip())]
    r.shuffle(players)
    if len(players) % 2 != 0: players = players + [p.Player("PASS")]
    return players

# It sets the first round, so it does not have to check if players fought against others
def firstTime(players, msg, i=0):
    if i < len(players):
        p1,p2 = players[i],players[i+1]
        msg = msg + str(p1.name + " ~ " + p2.name + "\t")
        p1.addFight(p2)
        players[i] = p1
        p2.addFight(p1)
        players[i+1] = p2
        return firstTime(players, msg, i + 2)
    return (players,msg)

def new_round(players):
    fights = []
    tmpPlayers = players.copy() # so the real players remain untouched
    for i in range(len(players)):
        tmp1 = tmpPlayers[i]
        tmpPlayers[i] = None
        #finding an opponent
        for j in range(len(tmpPlayers)):
            tmp2 = tmpPlayers[j]
            if tmp1 != None and tmp2 != None and tmp1.name != tmp2.name and tmp1.name not in tmp2.fights and tmp2.name not in tmp1.fights and tmp1.name not in fights and tmp2.name not in fights:
                fights = fights + [tmp1.name,tmp2.name]
                tmp1.addFight(tmp2)
                tmp2.addFight(tmp1)
                tmpPlayers[i] = None
                tmpPlayers[j] = None
    return fights

client = discord.Client()
#client = commands.Bot(command_prefix = "!")
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    global players
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    # starting a tournament: players get shuffled and the score initialized to 0
    elif message.content.startswith('!t'):
        #global players
        players = fillPlayers(message.content,players)
        [print(x.name) for x in players]
        msg = 'Turn 1:\t'
        players, msg = firstTime(players, msg)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!s'):
        str = splitter(message.content)
        for x in str:
            tmp_name,score = x.split(":")[0], int(x.split(":")[1].strip())
            for i in range(len(players)): #assigning the score
                if players[i].name.strip() == tmp_name.strip():
                    players[i].addPoints(score)
        players = sorted(players, key= lambda x: x.points, reverse=True)
        print(new_round(players))
        await client.send_message(message.channel, prettyPrinting(''))

    elif message.content.startswith('!r'):
        await client.send_message(message.channel, prettyPrinting(''))
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
