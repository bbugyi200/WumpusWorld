""" helpers.py

helper functions for kbank """

from collections import namedtuple


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
