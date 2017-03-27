from . kbank.kbank import KBank
from . constants import getDirections
from . graphs import getPath, getGraph
from . import constants as C


class Agent:
    def __init__(self, stimArr, verbose=False):
        self.stimArr = stimArr
        self.verbose = verbose
        self.mCount = 0
        self.KB = KBank(stimArr)
        self.actions = {'left': self.left,
                        'right': self.right,
                        'up': self.up,
                        'down': self.down}
        self.Log = []
        self.dead = False
        self.forfeit = False
        self.foundG = False

    def act(self):
        x, y = self.KB.location
        options = self.KB.options
        senses = self.stimArr[x][y]

        if C.Gold in senses:
            path = self.UtilityFunc([(0, 0)])
        else:
            path = self.UtilityFunc(options)

        for action in self.getActionSequence(path, []):
            self.mCount += 1
            if self.verbose: print('action  = ', action)
            self.Log.append(action)
            action()

        self.react()

    def react(self):
        """ React to Gold, Pit, or Wumpus """
        x, y = self.KB.location
        senses = self.stimArr[x][y]

        if C.Gold in senses:
            self.foundG = True
        elif C.Wumpus in senses:
            self.dead = True
        elif C.Pit in senses:
            self.dead = True

    def UtilityFunc(self, options):
        DeathProbs = dict()
        for option in options:
            x, y = option
            DProb = self.KB.PBank.Probs[x][y] + self.KB.WBank.Probs[x][y]
            DeathProbs[option] = DProb

        minDeathProb = min(DeathProbs.values())
        filtered_options = []
        if minDeathProb < 0.5:
            for index, prob in DeathProbs.items():
                if prob == minDeathProb:
                    filtered_options.append(index)
        else:
            filtered_options = [(0, 0)]
            self.forfeit = True

        path = ...
        minDistance = 100
        for index in filtered_options:
            graph = getGraph(self.KB.visited | {index})
            path = getPath(graph, self.KB.location, index)
            distance = len(path)
            if distance < minDistance:
                minDistance = distance
                final_path = path

        return final_path

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
