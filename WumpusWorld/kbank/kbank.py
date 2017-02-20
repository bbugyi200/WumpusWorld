""" kbank.py

Agent's Knowledge Bank.
"""

from ..environment import getIndexes
from .. import constants as C
from .death import Death
import math
import abc


class BaseBank:
    """ Agent's Knowledge Bank

        Primary objective of this class is to establish accurate probabilities
        of each square in the environment being either a pit or a wumpus by
        using sensory data retrieved from each square that the agent has
        visited """
    def __init__(self, stimArr):
        self.Probs = [[0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.],
                      [0., 0., 0., 0.]]

        __metaclass__ = abc.ABCMeta
        self.Indexes = getIndexes()
        self.stimArr = stimArr
        self.Known = False

    def markSafe(self, index):
        """ Sets pitProb at index to 0 """
        x, y = index
        self.Probs[x][y] = 0.0

    def Inv(self, prob):
        if (1 - prob) >= 0:
            return (1 - prob)
        else:
            return 0.0

    @abc.abstractmethod
    def calcProbs(self):
        pass

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
            if (D not in self.Indexes) or \
               (self.Probs[x][y] == 0.0) or \
               (self.Probs[x][y] == 1.0):
                    directions.remove(D)

        return directions

    def update(self, index):
        if not (index in self.Indexes):
            return

        self.Indexes.remove(index)

        x, y = index

        senses = self.stimArr[x][y]
        if C.Wumpus in senses:
            raise Death(C.Wumpus)
        if C.Pit in senses:
            raise Death(C.Pit)
        else:
            self.markSafe(index)

        self.calcProbs()


class Uniform(BaseBank):
    def __init__(self, stimArr):
        BaseBank.__init__(self, stimArr)
        self.Kbase = [[list(), list(), list(), list()],
                      [list(), list(), list(), list()],
                      [list(), list(), list(), list()],
                      [list(), list(), list(), list()]]

        self.listOfPercepts = []

        self.uniformDistribution()
        self.update((0, 0))

    def markSafe(self, index):
        BaseBank.markSafe(self, index)
        x, y = index
        self.Kbase[x][y][0][0] -= 1
        self.Kbase[x][y] = [[0]]

    def uniformDistribution(self):
        self.listOfPercepts.append([16])
        PerceptIndex = len(self.listOfPercepts) - 1
        for index in self.Indexes:
            x, y = index
            self.Kbase[x][y].append(self.listOfPercepts[PerceptIndex])
            self.Probs[x][y] = math.ceil(1 / 15 * 1000) / 1000

    def calcProbs(self):
        """ Uses percepts to calculate the pitProb of each square """
        for index in self.Indexes:
            x, y = index
            percepts = self.Kbase[x][y]

            Prob = 0.0
            if self.Probs[x][y]:
                P = percepts[0][0]

                try:
                    Prob = 1 / P
                except:
                    print('x:{0}\ny:{1}\nP:{2}'.format(x, y, P))
                Prob = math.ceil((Prob * 1000)) / 1000

                self.Probs[x][y] = Prob
                if Prob == 1.0:
                    self.Known = True


class WBank(Uniform):
    def __init__(self, stimArr):
        Uniform.__init__(self, stimArr)

    def update(self, index):
        Uniform.update(self, index)

        x, y = index
        senses = self.stimArr[x][y]
        directions = self.getDirections(index)

        if C.Stench in senses:
            for index in self.Indexes:
                x, y = index
                if (index not in directions) and (self.Probs[x][y] != 1.0):
                    self.markSafe(index)
        else:
            for D in directions:
                self.markSafe(D)

        self.calcProbs()


class GBank(Uniform):
    def update(self, index):
        Uniform.update(self, index)

        x, y = index
        senses = self.stimArr[x][y]

        if C.Gold in senses:
            self.Probs[x][y] = 1.0
            for I in self.Indexes:
                self.markSafe(I)
        else:
            self.markSafe(index)


class PBank(BaseBank):
    def __init__(self, stimArr):
        BaseBank.__init__(self, stimArr)

    def update(self, index):
        BaseBank.update(self, index)

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


class KBank:
    def __init__(self, stimArr):
        self.PBank = PBank(stimArr)
        self.WBank = WBank(stimArr)
        self.GBank = GBank(stimArr)

        self.BankList = [self.PBank, self.WBank, self.GBank]
