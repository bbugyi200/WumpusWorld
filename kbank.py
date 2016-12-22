""" kbank.py

Agent's Knowledge Bank.
"""

##############################################################################
#                               TODO                                         #
##############################################################################
#
# [X] Move all constants to constants.py
# [X] Create Death Exception Class
# [X] Set surrounding squares to 0 if no wind or stench sense
# [] Correct probabilities to include consideration for 1/15 chance of wumpus
#    and gold (Remember that Wumpus is only a factor if a Stench sense is
#    present).
#
##############################################################################

from stimuli import Stimuli
from environment import getEnv, getIndexes
import constants as C
from tests import TitlePrint
import numpy
import math
import os


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

        self.pKbase = [[list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()]]

        self.wKbase = [[list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()],
                       [list(), list(), list(), list()]]

        self.listOfPercepts = []
        self.Indexes = getIndexes()
        self.setInitialProb()
        self.stimArr = stimArr

        self.update(index=(0, 0))

    def __str__(self):
        return '{0}\n{1}\n{2}\n{3}\n'.format(self.pProb[0],
                                             self.pProb[1],
                                             self.pProb[2],
                                             self.pProb[3])

    def setInitialProb(self):
        """ Sets the initial probabilities of each square being a pit """
        for index in self.Indexes:
            x, y = index
            self.pKbase[x][y].append([5])
            self.pProb[x][y] = 0.2

    def markSafe(self, index):
        """ Sets pitProb at index to 0 """
        x, y = index
        for P in self.pKbase[x][y]:
            P[0] -= 1
        self.pProb[x][y] = 0.0

    def calcProbs(self):
        """ Uses percepts to calculate the pitProb of each square """
        for index in self.Indexes:
            x, y = index
            percepts = self.pKbase[x][y]

            Prob = 0.0
            if self.pProb[x][y]:
                for P in percepts:
                    P = P[0]
                    try:
                        P = 1 / P
                    except:
                        print('x:{0}\ny:{1}\nP:{2}'.format(x, y, P))
                    Prob = 1 - ((1 - Prob) * (1 - P))
                    Prob = math.ceil((Prob * 100)) / 100

            self.pProb[x][y] = Prob

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

        self.markSafe(index)

        directions = self.getDirections(index)

        # Check for adjacent square with probability of pit equal to 1.0.
        #
        # If found, end the function. Pit is known to be in adjacent square,
        # so C.Wind is not new data.
        for D in directions:
            x, y = D
            try:
                if self.pProb[x][y] == 1.0:
                    self.calcProbs()
                    return
            except IndexError:
                fmt = 'IndexError triggerred using (x={0}, y={1})'
                print(fmt.format(x, y))

        # If there is no wind sense in the current square, set probabilities
        # in adjacent squares to zero. (Use directions to avoid altering
        # squares that already have a zero probability)
        if not (C.Wind in senses):
            for D in directions:
                self.markSafe(D)
            self.calcProbs()

        else:
            # numOfPossibleLocations
            NoPL = len(directions)

            if C.Wind in senses:
                self.listOfPercepts.append([NoPL])
                i = len(self.listOfPercepts) - 1
                for D in directions:
                    x, y = D

                    self.pKbase[x][y].append(self.listOfPercepts[i])

        self.calcProbs()


if __name__ == '__main__':
    def getModifiedEnv():
        numOfTwos = 0
        while numOfTwos < 2:
            env = getEnv()
            env[env > 2] = 0
            unique, counts = numpy.unique(env, return_counts=True)
            try:
                numOfTwos = dict(zip(unique, counts))[2]
            except KeyError:
                numOfTwos = 0
        return env

    env = getEnv()

    stimArr = Stimuli(env).stimArr
    K = KBank(stimArr)

    oldIndex = (0, 0)
    x, y = (0, 0)
    while(True):
        print('Position of Agent: ({0},{1})'.format(x, y), end='\n\n')
        TitlePrint('Environment')
        print(env, end='\n\n')

        TitlePrint('Percepts')
        count = 0
        for row in K.pKbase:
            for percept in row:
                count += 1
                if count % 4 == 0:
                    print(percept)
                else:
                    print(percept, end=' --- ')
        print()

        TitlePrint('Pit Probabilities')
        print(K)

        print('~~~ Input Options ~~~',
              '1. Enter Index (x y) to move agent.',
              '2. Enter N to get a new random (non-modified) environment.',
              '3. Enter M to get a new random (modified) environment.',
              sep='\n',
              end='\n\n')

        userInput = input('>>> ')
        os.system('clear')

        if len(userInput.split()) == 2:
            x, y = userInput.split()
            x = int(x); y = int(y)
            oldIndex = (x, y)
            K.update(index=(x, y))
        elif userInput in 'MN':
            if userInput == 'M':
                env = getModifiedEnv()
            elif userInput == 'N':
                env = getEnv()
            x, y = (0, 0)
            stimArr = Stimuli(env).stimArr
            K = KBank(stimArr)
        elif userInput == 'P':
            TitlePrint('Percepts')
            for row in K.pKbase:
                print(row)
            # for D in K.getDirections(oldIndex):
            #     x, y = D
            #     fmt = 'Percepts for ({0},{1}) --> {2}'
            #     print(fmt.format(x, y, K.pKbase[x][y]))
            print()
