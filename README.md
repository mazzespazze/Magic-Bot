## Synopsis

Magic-Bot is a discord bot for Magic the Gathering. It is able to manage turns, scores and rankings in a friendly discord environment. It is meant for personal use.

## Code Example

### Start

First round you should give the names to the bot (no spaces!) on discord:

```
!names NamePlayer1,NamePlayer2,NamePlayer3,NamePlayer4
```

NOTE: if the number of player is odd, then one will get a pass, the first time will be completely random, but from the second time it picks the last one.

### Setting the points

After a round you should set the matches scores in this way:

```
!set (NamePlayer1,NamePlayer2)=2-0;(NamePlayer3,NamePlayer4)=1-2
```

NOTE: there is no draw in this bot, the scores has to be: 2-0, 2-1, 1-2, 0-2!

The bot will automatically calculate the next matches. Be always sure that you gave the bot the correct scores. If you forgot something you can always !reset and set again from the start.

```
!reset
I have resetted all players as from the start :)
```

### End

The bot will terminate automatically after "N" turns. The number of turns is calculated following the formula:
<img src="https://latex.codecogs.com/svg.latex?\Large&space;Turns=\log_2{|Players|}" title="\Large Turns=\log_2{|Players|}" />

You can check all the commands in the wiki of this project!

## Motivation

My friends and I play usually on Cockatrice or Magic Arena and we wanted a BOT to make the interactions more funny and easier. And as well to decide who plays against who.

I will maintain it as long as we play Magic and as long as we want to keep using Cockatrice.

## Installation

You should check to have python3 on your system. After that you just execute \$python3 MagicBot.py

NOTE: you should install discord module for python3: \$python3 -m pip install discord
Complete commands (assuming python3 is installed):

```
$git clone https://github.com/mazzespazze/Magic-Bot.git
$python3 -m pip install discord
```

## Tests

TODO There will be soon a collection of tests to make sure the python version you get is the one that is working actually.

## Contributors

GIT nicknames: mazzespazze, mikaelamch.

If you want to join or improve this project you can always email me matteo.ghetti@nonorank.com (Matteo Ghetti).

## License

GNU Licence: https://www.gnu.org/licenses/gpl-3.0.en.html
