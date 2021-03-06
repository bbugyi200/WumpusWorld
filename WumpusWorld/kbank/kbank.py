""" kbank.py

Agent's Knowledge Bank.
"""

from .. environment import getIndexes
from .. import constants as C
from . pitclass import PitClass
import abc
from .. constants import getDirections as getDirs


class BaseBank:
    """ Agent's Knowledge Bank

        Primary objective of this class is to establish accurate probabilities
        of each square in the environment being either a pit or a wumpus by
        using sensory data retrieved from each square that the agent has
        visited """

    __metaclass__ = abc.ABCMeta

    KnownWumpus = [False]
    ProbTable = dict()
    for Obj in ['P', 'W', 'G']:
        ProbTable[Obj] = C.getMatrix(0.0)

    def __init__(self, stimArr):
        self.stimArr = stimArr
        self.Indexes = getIndexes()
        self.Known = False

    @abc.abstractmethod
    def calcProbs(self):
        pass

    def getDirections(self, index, clean=True):
        directions = getDirs(index)
        directions = [D for D in directions]
        dummyDirs = directions[:]
        for D in dummyDirs:
            x, y = D
            if D not in self.Indexes:
                directions.remove(D)
            elif clean:
                if (self.Probs[x][y] == 0.0) or \
                   (self.Probs[x][y] == 1.0):
                    directions.remove(D)

        return directions


class Uniform(BaseBank):
    def __init__(self, stimArr):
        BaseBank.__init__(self, stimArr)
        self.Kbase = C.getMatrix(list())
        self.numOfSquares = self.NOS = pow(C.EnvSize, 2)

        self.listOfPercepts = []

        self.uniformDistribution()
        self.update((0, 0))

    def markSafe(self, index):
        x, y = index
        self.Probs[x][y] = 0.0
        K = self.Kbase[x][y]
        P = K[0]
        P[0] -= 1
        self.Kbase[x][y] = [[0]]

    def uniformDistribution(self):
        self.listOfPercepts.append([self.NOS])
        PerceptIndex = len(self.listOfPercepts) - 1
        for index in self.Indexes:
            x, y = index
            self.Kbase[x][y].append(self.listOfPercepts[PerceptIndex])
            self.Probs[x][y] = round(1 / self.NOS - 1, 3)

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
                Prob = round(Prob, 3)

                self.Probs[x][y] = Prob
                if Prob == 1.0:
                    self.Known = True

    def update(self, index):
        if index in self.Indexes:
            self.Indexes.remove(index)


class WBank(Uniform):
    def __init__(self, stimArr):
        self.Probs = self.ProbTable['W']
        Uniform.__init__(self, stimArr)

    def update(self, index):
        Uniform.update(self, index)
        self.markSafe(index)

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

    def calcProbs(self):
        Uniform.calcProbs(self)
        if self.Known:
            self.KnownWumpus[0] = True


class GBank(Uniform):
    def __init__(self, stimArr):
        self.Probs = self.ProbTable['G']
        Uniform.__init__(self, stimArr)

    def update(self, index):
        Uniform.update(self, index)
        self.markSafe(index)

        x, y = index
        senses = self.stimArr[x][y]

        if C.Gold in senses:
            self.Probs[x][y] = 1.0
            for I in self.Indexes:
                self.markSafe(I)
        else:
            self.markSafe(index)

        self.calcProbs()


class PBankFull(BaseBank):
    def __init__(self, stimArr):
        self.Probs = self.ProbTable['P']
        BaseBank.__init__(self, stimArr)

        self.PC = PitClass((0, 0))

        self.update((0, 0))

    def calcProbs(self):
        for index in self.PC.Indexes:
            x, y = index

            prob = round(self.PC.getProb(index), 3)

            self.Probs[x][y] = prob

    def update(self, index):
        x, y = index
        senses = self.stimArr[x][y]
        directions = self.getDirections(index, clean=False)

        for D in directions:
            self.PC.addIndex(D)

        self.PC.noChanceOfPit(index)
        if C.Wind in senses:
            self.PC.notAll(directions, 0)
        else:
            for D in directions:
                self.PC.noChanceOfPit(D)

        PossibleWumpus = []
        for index in self.PC.Indexes:
            x, y = index
            if self.ProbTable['W'][x][y]: PossibleWumpus.append(index)

        self.PC.notAll(PossibleWumpus, 1)

        self.PC.updateProbs()

        self.calcProbs()


class KBank:
    def __init__(self, stimArr):
        self.WBank = WBank(stimArr)
        self.GBank = GBank(stimArr)
        self.PBank = PBankFull(stimArr)

        self.location = (0, 0)
        self.Indexes = getIndexes()

        self.visited = {(0, 0)}
        self.options = {(0, 1), (1, 0)}

        self.BankList = [self.GBank, self.WBank, self.PBank]

    def update(self, index):
        self.location = index
        if index in self.Indexes:
            self.Indexes.remove(index)
        self.visited.add(index)
        for D in getDirs(index):
            if (D in self.Indexes) and (D not in self.visited):
                self.options.add(D)

        if index in self.options:
            self.options.remove(index)

        for Bank in self.BankList:
            Bank.update(index)
