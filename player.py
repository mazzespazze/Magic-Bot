""" Player is a class that will take care of all the information of a magic player: score, matches, and
    if he/she got already the pass """
import random, operator

class Player:

    def __init__(self, name):
        self.name = name.strip()
        self.points = 0
        self.fights = []
        self.magic_pass = False
        self.pass_string = ""
        self.won = [] #won fights against other players

    def add_points(self, x):
        """ Adding @x points to the current score """
        self.points += x

    def set_pass(self):
        self.magic_pass = True
        self.pass_string = "+2p*"

    def get_points(self):
        """ Returning the points of a player """
        return self.points

    def has_pass(self):
        """ It returns if this player got a pass """
        return self.magic_pass

    def add_fight(self, player):
        """ Adding @player's name to the list of the fights """
        self.fights.append(player.name)

    def __str__(self):
        return str(self.name) + " with score " + str(self.points) + self.pass_string

    def get_name(self):
        """ Returning the name of this player """
        return self.name

    def add_won(self, player):
        """ Adding @player to the list of won matches: it means this player (@self) won
        against @player  """
        self.won.append(player.name)

    def did_player_win_against(self,other):
        """ It returns whether or not @other' name is in the list won matches """
        return other.get_name() in self.won

    def __repr__(self):
        return str(self.name) + " with score " + str(self.points) + self.pass_string


def global_sorting(REAL_PLAYERS, value):
    """ Sorting according to the value """
    ZIPPED_PLAYERS = list()
    for pl in REAL_PLAYERS:
        POINTS = pl.get_points()
        if pl.has_pass():
            POINTS += value
        ZIPPED_PLAYERS.append((pl,POINTS))
    ZIPPED_PLAYERS.sort(key=lambda tup: tup[1], reverse=True)
    """ Now we have a list according to their points:
        NOTE: we will now use a second sorting method to check if two
        players have the same points """
    PLAYERS_SORTED = list(map(lambda a: a[0], ZIPPED_PLAYERS))
    last = PLAYERS_SORTED[0].get_points()
    for pl in range(len(PLAYERS_SORTED)):
        if pl == 0: continue
        if PLAYERS_SORTED[pl].get_points() == last: #if the last checked has the same points...
            if PLAYERS_SORTED[pl].did_player_win_against(PLAYERS_SORTED[pl-1]):
                """ this means that player in position pl won against the previous one,
                    therefore we swap! """
                loser = PLAYERS_SORTED[pl-1]
                PLAYERS_SORTED[pl-1] = PLAYERS_SORTED[pl]
                PLAYERS_SORTED[pl] = loser
                pl = pl - 1
        else:
            #means the two players DO NOT have the same points, therefore
            last = PLAYERS_SORTED[pl].get_points()
    return PLAYERS_SORTED

def sorted_players_for_ranking(REAL_PLAYERS):
    """ Here the PASS boolean will be considered as 1.5 """
    return global_sorting(REAL_PLAYERS, 1.5)

def sorted_players_for_playing(REAL_PLAYERS):
    """ Here the PASS boolean will be considered as 2.5 """
    return global_sorting(REAL_PLAYERS, 2.5)

def find_players(REAL_PLAYERS, NAMES):
    """ Assuming the names are only two """
    PLAYERS = list()
    for pl in REAL_PLAYERS:
        if pl.get_name() in NAMES:
            PLAYERS.append(pl)
    return PLAYERS

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
    """ Testing won list """
    for x in range(100):
        A, B, C = Player("Matteo1"), Player("Matteo2"), Player("Matteo3")
        A.add_points(2)
        B.add_points(2)
        C.add_points(2)
        B.add_won(A)
        B.add_won(C)
        L = sorted_players_for_ranking([A,B,C])
        assert "Matteo2" == L[0].get_name()
