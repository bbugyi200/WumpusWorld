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
    for x in range(4):
        for y in range(4):
            Indexes.append((x, y))
    return Indexes


def getPath(graph, start, end, path=[]):
    path = path + [start]

    if start == end:
        return path

    if start not in graph:
        return None

    shortest = None

    for node in graph[start]:
        if node not in path:
            newpath = getPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def getGraph(nodes):
    graph = dict()
    for node in nodes:
        directions = set(getDirections(node))
        graph[node] = nodes & directions  # Set Intersection

    return graph

if __name__ == '__main__':
    nodes = {(0, 0), (0, 1), (1, 0), (2, 0), (3, 0), (3, 1)}
    graph = getGraph(nodes)
    path = getPath(graph, (0, 0), (3, 1))
    print(path)
