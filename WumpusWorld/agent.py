from . kbank.kbank import KBank
from . constants import getDirections, getPath, getGraph
from . import constants as C


class Agent:
    def __init__(self, stimArr):
        self.stimArr = stimArr
        self.mCount = 0
        self.KB = KBank(stimArr)
        self.actions = {'left': self.left,
                        'right': self.right,
                        'up': self.up,
                        'down': self.down}
        self.Log = []

    def run(self):
        x, y = self.KB.location
        options = self.KB.options

        if C.Gold in self.stimArr[x][y]:
            target, path = self.maxUtility([(0, 0)])
            print("THE AGENT HAS FOUND THE GOLD IN {0} MOVES!!!".format(self.mCount))
        else:
            target, path = self.maxUtility(options)
        for action in self.getActionSequence(path, []):
            self.mCount += 1
            print('action  = ', action)
            self.Log.append(action)
            action()

    def maxUtility(self, options):
        DeathProbs = dict()
        for option in options:
            x, y = option
            DProb = self.KB.PBank.Probs[x][y] + self.KB.WBank.Probs[x][y]
            DeathProbs[option] = DProb

        Min = min(DeathProbs.values())
        options = []
        for index, prob in DeathProbs.items():
            if prob == Min:
                options.append(index)

        target = ...
        path = ...
        Min = 100
        for index in options:
            graph = getGraph(self.KB.visited | {index})
            P = getPath(graph, self.KB.location, index)
            D = len(P)
            if D < Min:
                Min = D
                target = index
                path = P

        return target, path

    def getActionSequence(self, path, ActionSeq):
        if len(path) < 2:
            return ActionSeq

        location = path[0]
        nextSquare = path[1]
        path = path[1:]

        directions = getDirections(location)
        for key in self.actions:
            if nextSquare == getattr(directions, key):
                ActionSeq.append(self.actions[key])
                ActionSeq = self.getActionSequence(path, ActionSeq)
        return ActionSeq

    def left(self):
        index = getDirections(self.KB.location).left
        self.KB.update(index)

    def right(self):
        index = getDirections(self.KB.location).right
        self.KB.update(index)

    def up(self):
        index = getDirections(self.KB.location).up
        self.KB.update(index)

    def down(self):
        index = getDirections(self.KB.location).down
        self.KB.update(index)