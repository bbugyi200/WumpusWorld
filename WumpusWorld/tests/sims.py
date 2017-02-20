import random
import numpy as np
from ..environment import getEnv
from .. import constants as C


def getTestEnv():
    M1 = np.zeros((4, 4), dtype=int)
    A = C.Agent
    P = C.Pit
    M1[0] = [A, 0, 0, P]
    M1[1] = [0, 0, P, 0]
    M1[2] = [0, P, 0, 0]
    M1[3] = [P, 0, 0, 0]

    return M1


def testRandomEnvs(loops=100000):
    totalPits = 0
    for i in range(loops):
        env = getEnv()
        unique, counts = np.unique(env, return_counts=True)
        try:
            totalPits += dict(zip(unique, counts))[C.Pit]
        except KeyError:
            pass
    return totalPits / loops


def PPSim(num, tests=100000, GP=0.2, IncludeGold=False):
    """ Simulates Pit Probabilities """
    numOfSuccesses = 0
    total = tests
    for x in range(tests):
        num = int(num)
        squares = [0] * num
        pit_probability = [0, 0, 0, 0, 1]
        Indexes = list(range(num))

        selected = random.choice(Indexes)
        squares[selected] = 1
        Indexes.remove(selected)

        for i in Indexes:
            if random.choice(pit_probability):
                squares[i] = 1

        def setGold():
            gold_probability = [0] * (int(1 / GP) - 1)
            gold_probability[0] = 1

            goldPlaced = False
            for i in range(num - 1):
                if not goldPlaced:
                    if random.choice(gold_probability):
                        goldIndex = random.choice(Indexes)
                        squares[goldIndex] = 2
                        goldPlaced = True
                        Indexes.remove(goldIndex)

        if IncludeGold: setGold()

        if squares[0] == 0 and squares[1] == 0:
            total -= 1
        if squares[0] == 1:
            numOfSuccesses += 1

    print('{0}%'.format(numOfSuccesses / total * 100))

counts = testRandomEnvs()
print(counts)
