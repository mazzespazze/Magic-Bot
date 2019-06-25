""" Player is a class that will take care of all the information of a magic player: score, matches, and
    if he/she got already the pass """
import random, operator, itertools

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
        """ Returning the points of current player """
        return self.points

    def has_pass(self):
        """ It returns if this player got a pass """
        return self.magic_pass

    def add_fight(self, player):
        """ Adding @player's name to the list of the fights """
        self.fights.append(player.name)

    def get_fights(self):
        return self.fights

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

""" Useful global functions that manage list of players based on ranking and matching """

def global_sorting(REAL_PLAYERS, value):
    """ Sorting according to the value and checking if a player won against a second
        one boosting in case of victory """
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

def check_pass(PLAYERS_SORTED):
    INDEX = 0
    for pl in PLAYERS_SORTED[::-1]:
        if not pl.has_pass():
            break
        INDEX += 1
    return len(PLAYERS_SORTED) - INDEX - 1
    #returning the index of the pass

def sorted_players_for_playing(REAL_PLAYERS):
    """ Here the PASS boolean will be considered as 2.5
        NOTE: the simple sorting does not suffice. We need to check if two players
        did already a match against each other! And the last one cannot have a PASS if
        it already got it """
        #TODO function that checks the matches before calling the new game
    PLAYERS_SORTED = global_sorting(REAL_PLAYERS, 2.5)
    """ Solving the first contraint: going from the bottom of the list taking the first
        that does not have a pass """
    PASS = len(PLAYERS_SORTED) % 2 == 1 #if even is False, True otherwise
    INDEX_PASS = -1 #assuming is the last position
    PASS_PLAYER = None
    if PASS:
        INDEX_PASS = check_pass(PLAYERS_SORTED)
        pass_player = PLAYERS_SORTED[INDEX_PASS] #saving pass player
        del PLAYERS_SORTED[INDEX_PASS] #deleting the pass player from its original position
        PASS_PLAYER = pass_player
    """ Now the PASS is decided, and we will just do permutations to find the next rounds
        minimizing the fairness (sum of all the differences between points on match) and ensuring
        the legality of it (never play again the same match, never the same pass) """
    assert len(PLAYERS_SORTED) % 2 == 0
    PLAYERS_SORTED = min_fairness(check_legality(build_combinations(PLAYERS_SORTED)))
    PLAYERS_SORTED.append(PASS_PLAYER)
    return PLAYERS_SORTED

def find_player(REAL_PLAYERS, NAME):
    """ Assuming the names in @NAMES are only two """
    PLAYERS = list()
    for pl in REAL_PLAYERS:
        if pl.get_name() == NAME:
            return pl

def check_legality(LIST):
    """ @LIST is a list of lists and it filters out all the non legal combinations:
        players that already played against other ones should not be legal """
    LEGAL_MATCHES, INDEX, LEGAL = [[]], 0, False
    for game in LIST:
        for match in game:
            if not (match[0].get_name() in match[1].get_fights()) and not (match[1].get_name() in match[0].get_fights()):
                LEGAL = True
        if LEGAL:
            LEGAL_MATCHES.append(list())
            LEGAL_MATCHES[INDEX] = game
            INDEX += 1
            LEGAL = False
    return list(filter(lambda x: len(x) > 0, LEGAL_MATCHES))

def min_fairness(LIST):
    """ Given a LIST of combinations of possible matches, we select the combination with
        the minimum fairness or tight for it. FAIRNESS = the sum of the difference of points in absolute
        value of all matches within a combination """
    FAIRNESS, FAIRNESS_INDEX = 100000, -1
    for combination in range(len(LIST)):
        TMP_FAIR =  0
        for match in LIST[combination]:
            PASS_1, PASS_2 = 0, 0
            if match[0].has_pass():
                PASS_1 = 2.5
            if match[1].has_pass():
                PASS_2 = 2.5
            TMP_FAIR += abs(match[0].get_points() + PASS_1 - match[1].get_points() - PASS_2)
        if TMP_FAIR < FAIRNESS:
            FAIRNESS = TMP_FAIR
            FAIRNESS_INDEX = combination
    return LIST[FAIRNESS_INDEX]

def build_combinations(LIST):
    """ It builds all combinations possible given a list of players without mirroring """
    A = list(itertools.combinations(LIST, 2))
    GLOBAL_LIST = [[]]
    GLOBAL_INDEX = 0
    MIN_SIZE = len(LIST)/2
    for INDEX in range(len(A)):
        _tuple_1 = A[INDEX]
        GLOBAL_NAMES = [_tuple_1[0].get_name(), _tuple_1[1].get_name()]
        GLOBAL_LIST.append(list())
        for NEW_INDEX in range(INDEX+1, len(A)):
            _tuple_2 = A[NEW_INDEX]
            if not (_tuple_2[0].get_name() in GLOBAL_NAMES) and not (_tuple_2[1].get_name() in GLOBAL_NAMES):
                GLOBAL_LIST[GLOBAL_INDEX].append(_tuple_2)
                GLOBAL_NAMES += [_tuple_2[0].get_name(), _tuple_2[1].get_name()]
        GLOBAL_LIST[GLOBAL_INDEX] = [_tuple_1] + GLOBAL_LIST[GLOBAL_INDEX]
        GLOBAL_INDEX += 1
    GLOBAL_LIST = list(filter(lambda l: len(l) >= MIN_SIZE, GLOBAL_LIST))
    return GLOBAL_LIST

if __name__ == '__main__':
    #test legality
    En, Pi, Iv, Ma, Be, Da, It = Player("Enrico"),Player("Pietro"),Player("Ivan"),Player("Matteo"),Player("Beppe"),Player("Davide"),Player("Itachi")
    En.add_fight(It)
    En.add_points(3)
    It.add_fight(En)

    Iv.add_fight(Ma)
    Iv.add_points(2)
    Ma.add_fight(Iv)
    Ma.add_points(1)

    Be.add_fight(Da)
    Be.add_points(2)
    Da.add_fight(Be)
    Da.add_points(1)

    Pi.set_pass()

    PL = [En, Pi, Iv, Ma, Be, Da, It]
    A1 = sorted_players_for_playing(PL)
    print("TURN 2", A1)

    En.add_fight(Pi)
    En.add_points(3)
    Pi.add_fight(En)

    Iv.add_fight(Be)
    Iv.add_points(2)
    Be.add_fight(Iv)
    Be.add_points(1)

    Ma.add_fight(Da)
    Ma.add_points(2)
    Da.add_fight(Ma)
    Da.add_points(1)

    It.set_pass()

    PL = [En, Pi, Iv, Ma, Be, Da, It]
    A2 = sorted_players_for_playing(PL)
    print("TURN 3", A2)





    #A2 = check_legality(A1)
    #print(len(A1), len(A2), print(A2))
    #print(sorted_players_for_playing(PL))
    """x = Player("Matteo")
    x.add_points(5)
    x.set_pass()
    y = Player("Michaela")
    y.add_points(7)
    z = Player("Ivan")
    z.add_points(6)
    z.set_pass()
    w = Player("Stergios")
    w.add_points(6)
    L = [x,y,z,w]
    print(sorted_players_for_ranking(L), "\n\n",sorted_players_for_playing(L),"\n\n")
    A,B,C = Player("Matteo1"), Player("Matteo2"), Player("Matteo3")
    A.add_points(2.5)
    C.add_points(2.5)
    B.set_pass() #everyone has 2.5
    C.set_pass()
    print(sorted_players_for_playing([A,B,C])) #A has to be last, since the only one without a pass!
    for x in range(100):
        A, B, C = Player("Matteo1"), Player("Matteo2"), Player("Matteo3")
        A.add_points(2)
        B.add_points(2)
        C.add_points(2)
        B.add_won(A)
        B.add_won(C)
        L = sorted_players_for_ranking([A,B,C])
        assert "Matteo2" == L[0].get_name()"""
