""" kbank.py

Agent's Knowledge Bank.
"""

from .environment import getIndexes
from . import constants as C
import math
import itertools
from collections import namedtuple


class Death(Exception):
    """ Exception class that will be raised in the event of the agent's
        death. """
    def __init__(self, DeathType=None):
        if DeathType == C.Pit:
            output = "The Agent has fallen down into a pit!!! SHE'S DEAD!!!"
        elif DeathType == C.Wumpus:
            output = "The Agent entered a room with the Wumpus!!! SHE HAS " \
                "BEEN EATEN!!!"
        else:
            output = "The Agent has went into a room with either a pit or a " \
                "wumpus!!! SHE IS DEAD!!!"

        Exception.__init__(self, output)


class bitStrings:
    def __init__(self, partition):
        self.length = len(partition)

        self.IMap = dict()
        for i, index in enumerate(partition):
            self.IMap[index] = i

        self.strings = [''.join(seq) for seq in itertools.product("01", repeat=self.length)]

    def get(self):
        return self.strings


class PitClass:
    def __init__(self, partition):

        BS = bitStrings(partition)
        bStrings = BS.get()

        Outcome = namedtuple('outcome', 'bitstr prob')
        self.outcomes = []



class KBank:
    """ Agent's Knowledge Bank

        Primary objective of this class is to establish accurate probabilities
        of each square in the environment being either a pit or a wumpus by
        using sensory data retrieved from each square that the agent has
        visited """
    def __init__(self, stimArr):
        self.pProb = [[0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.]]

        self.wProb = [[0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.]]

        self.gProb = [[0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.]]

        self.pKbase = [[list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()]]

        self.wKbase = [[list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()]]

        self.gKbase = [[list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()]]

        self.KBanks = {'Pit': (self.pProb, self.pKbase),
                       'Wumpus': (self.wProb, self.wKbase),
                       'Gold': (self.gProb, self.gKbase)}

        self.listOfPercepts = []
        self.KnownWumpus = False
        self.Indexes = getIndexes()
        self.setInitialProb()
        self.stimArr = stimArr

        self.update(index=(0, 0))

    def Partition(self, parity='even'):
        if parity == 'even':
            parity = True
        elif parity == 'odd':
            parity = False
        else:
            raise Exception('Parity must be Even or Odd!')

        partition = set()
        for index in self.Indexes:
            x, y = index
            even = True
            if (x + y) % 2:
                even = False

            if not (parity ^ even):  # XNOR
                partition.add(index)

        return partition

    def setInitialProb(self):
        """ Sets the initial probabilities of each square being a pit """
        self.listOfPercepts.append([16])
        GPI = len(self.listOfPercepts) - 1
        self.listOfPercepts.append([16])
        WPI = len(self.listOfPercepts) - 1
        for index in self.Indexes:
            x, y = index
            self.pKbase[x][y].append(['P'])
            self.pProb[x][y] = 0.2

            self.gKbase[x][y].append(self.listOfPercepts[GPI])
            self.gProb[x][y] = 1 / 15

            self.wKbase[x][y].append(self.listOfPercepts[WPI])
            self.wProb[x][y] = 1 / 15

    def markSafe(self, index, KBank):
        """ Sets pitProb at index to 0 """
        x, y = index
        ProbArray, Kbase = KBank
        for P in Kbase[x][y]:
            if P[0] != 'P':
                P[0] -= 1
                if P[0] < 0: P[0] = 0
        Kbase[x][y] = [[0]]
        ProbArray[x][y] = 0.0

    def calcProbs(self):
        """ Uses percepts to calculate the pitProb of each square """

        def Inv(prob):
            if (1 - prob) >= 0:
                return (1 - prob)
            else:
                return 0.0

        for KBank in (self.KBanks['Gold'], self.KBanks['Wumpus'], self.KBanks['Pit']):
            ProbArray, KBase = KBank
            for index in self.Indexes:
                x, y = index
                percepts = KBase[x][y]

                Prob = 0.0
                if ProbArray[x][y]:
                    for P in percepts:
                        P = P[0]

                        PITP = False
                        if P == 'P':
                            P = 5
                            PITP = True
                        try:
                            P = 1 / P
                        except:
                            print('x:{0}\ny:{1}\nP:{2}'.format(x, y, P))
                        if PITP:
                            P = P * Inv(Prob + self.wProb[x][y] + self.gProb[x][y])
                            Prob = Prob + P
                        else:
                            Prob = Inv(Inv(Prob) * Inv(P))
                        Prob = math.ceil((Prob * 100)) / 100

                ProbArray[x][y] = Prob
                if Prob == 1.0:
                    if KBank != self.KBanks['Gold']:
                        self.markSafe((x, y), self.KBanks['Gold'])
                    if KBank == self.KBanks['Wumpus']:
                        self.KnownWumpus = True

    def getDirections(self, index):
        """ Returns a list of indexs made up of the following set:

            {D: D is an index of a square adjacent to 'index'} """
        x, y = index
        directions = [(x + 1, y),  # right
                      (x - 1, y),  # left
                      (x, y + 1),  # down
                      (x, y - 1)]  # up

        dummyDirs = directions[:]
        for D in dummyDirs:
            x, y = D
            if (D not in self.Indexes) or (self.pProb[x][y] == 0.0):
                directions.remove(D)

        return directions

    def update(self, index):
        """ Updates the pitProb of each square based on the percepts of the
            current square and the knowledge of the percepts of previously
            visited squares """
        if not (index in self.Indexes):
            return
        else:
            self.Indexes.remove(index)

        x, y = index
        senses = self.stimArr[x][y]

        if C.Pit in senses:
            raise Death(C.Pit)
        elif C.Wumpus in senses:
            raise Death(C.Wumpus)
        elif C.Gold in senses:
            self.gProb[x][y] = 1.0
            for I in self.Indexes:
                self.markSafe(I, self.KBanks['Gold'])
        else:
            self.markSafe(index, self.KBanks['Gold'])

        self.markSafe(index, self.KBanks['Pit'])
        self.markSafe(index, self.KBanks['Wumpus'])

        self.calcProbs()

        directions = self.getDirections(index)

        # Check for adjacent square with probability of pit equal to 1.0.
        KnownPit = False
        for D in directions:
            x, y = D
            try:
                if self.pProb[x][y] == 1.0:
                    self.calcProbs()
                    KnownPit = True
            except IndexError:
                fmt = 'IndexError triggerred using (x={0}, y={1})'
                print(fmt.format(x, y))

        # If there is no wind sense in the current square, set probabilities
        # in adjacent squares to zero. (Use directions to avoid altering
        # squares that already have a zero probability)
        if not KnownPit:
            if C.Wind in senses:
                # numOfPossibleLocations
                NoPL = len(directions)

                self.listOfPercepts.append([NoPL])
                i = len(self.listOfPercepts) - 1
                for D in directions:
                    x, y = D

                    self.pKbase[x][y] = [self.listOfPercepts[i]] + self.pKbase[x][y]

            else:
                for D in directions:
                    self.markSafe(D, self.KBanks['Pit'])
                self.calcProbs()

        # Wumpus Update
        if self.KnownWumpus:
            pass
        elif C.Stench in senses:
            for index in self.Indexes:
                if index not in directions:
                    self.markSafe(index, self.KBanks['Wumpus'])
        else:
            for D in directions:
                self.markSafe(D, self.KBanks['Wumpus'])

        self.calcProbs()
