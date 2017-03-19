from . kbank.kbank import KBank
from . constants import getDirections
from . graphs import getPath, getGraph
from . import constants as C
import time
import os


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
        self.dead = False
        self.forfeit = False
        self.foundG = False

    def act(self):
        x, y = self.KB.location
        options = self.KB.options
        senses = self.stimArr[x][y]

        if C.Gold in senses:
            path = self.maxUtility([(0, 0)])
        else:
            path = self.maxUtility(options)

        for action in self.getActionSequence(path, []):
            self.mCount += 1
            print('action  = ', action)
            self.Log.append(action)
            action()

        self.react()

    def react(self):
        """ React to Gold, Pit, or Wumpus """

        deathSen = "\nTHE AGENT HAS ENTERED A ROOM WITH A {0}!!! SHE IS DEAD!!!"
        goldSen = "\nTHE AGENT HAS FOUND THE GOLD IN {0} MOVES!!!"
        sentences = {C.Gold: goldSen.format(self.mCount),
                     C.Pit: deathSen.format("PIT"),
                     C.Wumpus: deathSen.format("WUMPUS")}

        x, y = self.KB.location
        senses = self.stimArr[x][y]
        if C.Gold in senses:
            os.system('clear')
            print(sentences[C.Gold])
            time.sleep(2)
            self.foundG = True
        elif C.Wumpus in senses:
            os.system('clear')
            print(sentences[C.Wumpus])
            time.sleep(2)
            self.dead = True
        elif C.Pit in senses:
            os.system('clear')
            print(sentences[C.Pit])
            time.sleep(2)
            self.dead = True

    def maxUtility(self, options):
        DeathProbs = dict()
        for option in options:
            x, y = option
            DProb = self.KB.PBank.Probs[x][y] + self.KB.WBank.Probs[x][y]
            DeathProbs[option] = DProb

        Min = min(DeathProbs.values())
        options = []
        if Min < 0.5:
            for index, prob in DeathProbs.items():
                if prob == Min:
                    options.append(index)
        else:
            os.system('clear')
            print("THE AGENT HAS FORFEITED THE GAME!")
            time.sleep(1)
            options = [(0, 0)]
            self.forfeit = True

        path = ...
        Min = 100
        for index in options:
            graph = getGraph(self.KB.visited | {index})
            P = getPath(graph, self.KB.location, index)
            D = len(P)
            if D < Min:
                Min = D
                path = P

        return path

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
