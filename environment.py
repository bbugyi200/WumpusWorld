import numpy as np
import random
import constants as C

# Initializes 4-by-4 numpy array
# dtype=np.int sets the element type to integers
env = np.zeros((4, 4), dtype=np.int)


def getIndexes():
    """ Fills 'Indexes' list with all potential coordinate locations in
        environment. Indexes = [(0,0), (0,1), ..., (3,2), (3,3)] """
    Indexes = []
    for x in range(4):
        for y in range(4):
            Indexes.append((x, y))
    return Indexes

Indexes = getIndexes()


def setElement(index, value):
    x, y = index
    env[x][y] = value
    # Removes location from Indexes after it is used.
    Indexes.remove(index)


def randomize_pits():
    pit_probability = [1, 0, 0, 0, 0]
    for index in Indexes:
        setPit = random.choice(pit_probability)
        if setPit:
            setElement(index, C.Pit)


def setWumpus():
    index = random.choice(Indexes)
    setElement(index, C.Wumpus)


def setGold():
    index = random.choice(Indexes)
    setElement(index, C.Gold)


def setAgent():
    index = (0, 0)
    setElement(index, C.Agent)


def refreshGlobals():
    global Indexes
    global env
    Indexes = getIndexes()
    env = np.zeros((4, 4), dtype=np.int)


def getEnv():
    refreshGlobals()
    setAgent()
    setGold()
    setWumpus()
    randomize_pits()
    return env


if __name__ == '__main__':
    print('Agent = 1', 'Pit = 2', 'Wumpus = 3', 'Gold = 4\n', sep='\n')
    setAgent()
    setGold()
    setWumpus()
    randomize_pits()
    print(env)
