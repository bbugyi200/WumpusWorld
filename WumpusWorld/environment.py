""" environment.py

Set of functions that are used to create a Wumpus World environment with
the following requirements, as described by Stuart Russel and Peter Norvig
in their text, "Artificial Intelligence: A Modern Apprach":

    - 4x4 matrix
    - Square (0,0) is reserved for the agent
    - A single Wumpus is placed at a random location on the board
    - A single block of gold is placed at a random location on the board
    - Every other remaining square that does not already have an agent, a
      Wumpus, or a block of gold placed on it is given a 0.2 probability
      of being a pit
"""

import numpy as np
import random
from . import constants as C
from . constants import getIndexes


# dtype=np.int sets the element type to integers
env = np.zeros((4, 4), dtype=np.int)


Indexes = getIndexes()


def setElement(index, value):
    """ Sets env[index] to value and then removes this index from the
        main index set """
    x, y = index
    env[x][y] = value
    # Removes location from Indexes after it is used.
    Indexes.remove(index)


def randomize_pits():
    """ Loops through every index in the index set, selects certain
        indexes (based on 0.2 probability of selection), and places
        pits at the selected squares """
    pit_probability = [1, 0, 0, 0, 0]
    for index in Indexes:
        setPit = random.choice(pit_probability)
        if setPit:
            setElement(index, C.Pit)


def setWumpus():
    """ Places a Wumpus at a randomly selected square """
    index = random.choice(Indexes)
    setElement(index, C.Wumpus)


def setGold():
    """ Places a block of gold at a randomly selected square """
    index = random.choice(Indexes)
    setElement(index, C.Gold)


def setAgent():
    """ Places the agent at square (0,0) """
    index = (0, 0)
    setElement(index, C.Agent)


def refreshGlobals():
    """ Resets the index set and the environment """
    global Indexes
    global env
    Indexes = getIndexes()
    env = np.zeros((4, 4), dtype=np.int)


def getEnv(fair=False):
    """ Returns a new Wumpus World environment """
    refreshGlobals()
    if fair:
        Indexes.remove((0, 1))
        Indexes.remove((1, 0))
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
