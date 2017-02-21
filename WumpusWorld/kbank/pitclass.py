""" pitclass.py """

import itertools


class Outcome:
    def __init__(self, bitstr, prob):
        self.bitstr = bitstr
        self.prob = prob


class PitClass:
    def __init__(self, partition):
        # self.pchances = pchances
        self.partition = partition
        self.initBStrings()

    def initBStrings(self):
        self.IMap = dict()
        self.RevIMap = dict()
        for i, index in enumerate(self.partition):
            self.IMap[i] = index
            self.RevIMap[index] = i

        N = len(self.partition)
        self.bstrings = [''.join(seq) for seq in itertools.product("01", repeat=N)]

        self.outcomes = []
        for bitstr in self.bstrings:
            prob = self.getBSProb(bitstr)
            self.outcomes.append(Outcome(bitstr, prob))

    def getProb(self, index):
        bsIndex = self.RevIMap[index]
        totalProb = 0.0
        for outcome in self.outcomes:
            if int(outcome.bitstr[bsIndex]):
                totalProb += outcome.prob
        return totalProb

    def notAll(self, directions, X='empty'):
        bsIndexes = []
        badStrings = []
        for D in directions:
            bsIndexes.append(self.RevIMap[D])
        for outcome in self.outcomes:

            if X == 'empty':
                Neg = 0
            elif X == 'full':
                Neg = 1

            match = True
            for index in bsIndexes:
                if int(outcome.bitstr[index]) - Neg:
                    match = False
            if match:
                badStrings.append(outcome.bitstr)

        self.outcomes = [O for O in self.outcomes if O.bitstr not in badStrings]

    def noChanceOfPit(self, index):
        bsIndex = self.RevIMap[index]
        self.outcomes = [O for O in self.outcomes if not int(O.bitstr[bsIndex])]

    def updateChances(self, pchances):
        self.pchances = pchances
        self.updateProbs()

    def getBSProb(self, bitstr):
        prob = 1.0
        for i, ch in enumerate(bitstr):
            x, y = self.IMap[i]
            chance = 0.2
            # chance = self.pchances[x][y]
            if ch == '0':
                chance = 1 - chance
            prob *= chance
        return prob

    def updateProbs(self):
        for i, outcome in enumerate(self.outcomes):
            prob = self.getBSProb(outcome.bitstr)
            self.outcomes[i].prob = prob
        self.normalize()

    def normalize(self):
        sumOfProbs = 0.0
        for outcome in self.outcomes:
            sumOfProbs += outcome.prob

        if sumOfProbs != 0:
            prob_factor = 1 / sumOfProbs
            for outcome in self.outcomes:
                outcome.prob *= prob_factor

if __name__ == '__main__':
    pchances = [[0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.]]
    PC = PitClass([(0, 0), (0, 1), (0, 2)], pchances)
    pchances[0][0] = 0.2
    pchances[0][1] = 0.5
    pchances[0][2] = 0.99
    PC.updateChances(pchances)
    for outcome in PC.outcomes:
        print(outcome.bitstr, ' = ', outcome.prob)

    print('getProb = ', PC.getProb((0, 0)))
    print()

    PC.notAll([(0, 1), (0, 2)])
    PC.updateProbs()
    for outcome in PC.outcomes:
        print(outcome.bitstr, ' = ', outcome.prob)
