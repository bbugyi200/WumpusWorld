""" helpers.py

helper functions for kbank """

from collections import namedtuple


def getDirections(index):
    """ Returns a list of indexs made up of the following set:

        {D: D is an index of a square adjacent to 'index'} """
    x, y = index
    Dirs = namedtuple('Dirs', 'up right down left')
    directions = Dirs(right=(x + 1, y),  # right
                      left=(x - 1, y),  # left
                      down=(x, y + 1),  # down
                      up=(x, y - 1))  # up

    return directions
