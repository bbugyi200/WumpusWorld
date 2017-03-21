""" constants.py

Holds all state information that this program as a whole should be aware of
"""

from collections import namedtuple

Agent = 1
Pit = 2
Wumpus = 3
Gold = 4
Wind = 5
Stench = 6

EnvSize = 5


def getMatrix(item):
    matrix = []
    try:
        copy = getattr(item, 'copy')
    except AttributeError:
        copy = None
    for i in range(EnvSize):
        matrix.append([])
        for j in range(EnvSize):
            if copy:
                matrix[i].append(copy())
            else:
                matrix[i].append(item)

    return matrix


def getDirections(index):
    """ Returns a list of indexs made up of the following set:

        {D: D is an index of a square adjacent to 'index'} """
    x, y = index
    Dirs = namedtuple('Dirs', 'up right down left')
    directions = Dirs(down=(x + 1, y),
                      up=(x - 1, y),
                      right=(x, y + 1),
                      left=(x, y - 1))

    return directions


def getIndexes():
    """ Fills 'Indexes' list with all potential coordinate locations in
        environment. This will act as an index set for the Wumpus World
        environment. Indexes = [(0,0), (0,1), ..., (3,2), (3,3)] """
    Indexes = []
    for x in range(EnvSize):
        for y in range(EnvSize):
            Indexes.append((x, y))
    return Indexes
