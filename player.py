import random
import operator

class Player:

    def __init__(self, name):
        self.name = name.strip()
        self.points = 0
        self.fights = []
        self.magic_pass = False
        self.pass_string = ""

    def add_points(self, x):
        self.points += x

    def set_pass(self):
        self.magic_pass = True
        self.pass_string = "+2p*"

    def get_points(self):
        return self.points

    def has_pass(self):
        return self.magic_pass

    def add_fight(self, player):
        self.fights.append(player.name)

    def __str__(self):
        return str(self.name) + " with score " + str(self.points) + self.pass_string

    def get_name(self):
        return self.name

    def __repr__(self):
        return str(self.name) + " with score " + str(self.points) + self.pass_string

    def __lt__(self, other):
        RANDOM = [-1,1]
        if self.points < other.points: return -1
        if self.points > other.points: return 1
        elif self.points == other.points:
            if self.has_pass and not other.has_pass: return -1
            if self.has_pass and other.has_pass: return 1
        else:
            return RANDOM[random.randint(0,1)]


def global_sorting(REAL_PLAYERS, value):
    """ Sorting according to the value"""
    ZIPPED_PLAYERS = list()
    for pl in REAL_PLAYERS:
        POINTS = pl.get_points()
        if pl.has_pass():
            POINTS += value
        ZIPPED_PLAYERS.append((pl,POINTS))
    ZIPPED_PLAYERS.sort(key=lambda tup: tup[1], reverse=True)
    return list(map(lambda a: a[0], ZIPPED_PLAYERS))

def sorted_players_for_ranking(REAL_PLAYERS):
    """ Here the PASS boolean will be considered as 1.5 """
    return global_sorting(REAL_PLAYERS, 1.5)

def sorted_players_for_playing(REAL_PLAYERS):
    """ Here the PASS boolean will be considered as 2.5 """
    return global_sorting(REAL_PLAYERS, 2.5)

if __name__ == '__main__':
    x = Player("Matteo")
    x.add_points(5)
    y = Player("Michaela")
    y.add_points(7)
    z = Player("Ivan")
    z.add_points(6)
    z.set_pass()
    w = Player("Stergios")
    w.add_points(6)
    L = [x,y,z,w]
    print(sorted_players_for_ranking(L))
    #print(L)
