""" pitclass.py """


class Outcome:
    def __init__(self, bitstr, prob):
        self.bitstr = bitstr
        self.prob = prob


class PitClass:
    def __init__(self, start):
        self.Indexes = []
        self.IMap = dict()
        self.RevIMap = dict()
        self.count = 0

        self.initBStrings(start)
        self.getOutcomes()

    def initBStrings(self, start):
        self.bstrings = ['1', '0']

        self.IMap[self.count] = start
        self.RevIMap[start] = self.count

        self.Indexes.append(start)
        self.count += 1

    def getOutcomes(self):
        self.outcomes = []
        for bitstr in self.bstrings:
            prob = self.getBSProb(bitstr)
            self.outcomes.append(Outcome(bitstr, prob))

    def addIndex(self, index):
        if index in self.Indexes:
            return

        self.IMap[self.count] = index
        self.RevIMap[index] = self.count

        self.zeros = [bs + '0' for bs in self.bstrings]
        self.ones = [bs + '1' for bs in self.bstrings]
        self.bstrings = self.zeros + self.ones

        self.getOutcomes()
        self.Indexes.append(index)
        self.count += 1

    def getProb(self, index):
        bsIndex = self.RevIMap[index]
        totalProb = 0.0
        for outcome in self.outcomes:
            if int(outcome.bitstr[bsIndex]):
                totalProb += outcome.prob
        return totalProb

    def notAll(self, indexes, X='empty'):
        if not indexes:
            return

        if X == 'empty':
            Neg = 0
        elif X == 'full':
            Neg = 1

        bsIndexes = []
        badStrings = []
        for index in indexes:
            bsIndexes.append(self.RevIMap[index])
        for outcome in self.outcomes:
            match = True
            for index in bsIndexes:
                if abs(int(outcome.bitstr[index]) - Neg):
                    match = False
            if match:
                badStrings.append(outcome.bitstr)

        self.bstrings = [bs for bs in self.bstrings if bs not in badStrings]
        self.getOutcomes()

    def noChanceOfPit(self, index):
        bsIndex = self.RevIMap[index]
        self.bstrings = [bs for bs in self.bstrings if not int(bs[bsIndex])]
        self.getOutcomes()

    def getBSProb(self, bitstr):
        prob = 1.0
        for i, ch in enumerate(bitstr):
            x, y = self.IMap[i]
            chance = 0.2
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

        if sumOfProbs:
            prob_factor = 1 / sumOfProbs
            for outcome in self.outcomes:
                outcome.prob *= prob_factor

if __name__ == '__main__':
    PC = PitClass([(0, 0), (0, 1), (0, 2)])
    for outcome in PC.outcomes:
        print(outcome.bitstr, ' = ', outcome.prob)

    print('getProb = ', PC.getProb((0, 0)))
    print()

    PC.notAll([(0, 1), (0, 2)])
    PC.updateProbs()
    for outcome in PC.outcomes:
        print(outcome.bitstr, ' = ', outcome.prob)
