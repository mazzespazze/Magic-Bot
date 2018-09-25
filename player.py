class Player:

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.fights = []

    def addPoints(self, x):
        self.points = self.points+x

    def addFight(self, player):
        self.fights = self.fights + [player.name]

    def __str__(self):
        return str(self.name) + " : " + str(self.points) + " "

def compare(p1,p2):
    if p1.points > p2.points: return 1
    elif p1.points == p2.points: return 0
    else: return -1

if __name__ == '__main__':
    x = Player("Matteo")
    print(x.points)
