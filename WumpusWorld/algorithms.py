""" algorithms.py

Set of functions that can be used to mathematically assess properties of the
Wumpus World environment """

from . environment import getEnv, getIndexes

Indexes = getIndexes()


def Solvable(env, x=0, y=0, Indexes=Indexes):
    """ Tests if env is a solvable environment for the agent

    Returns (True, index) if a solution is found

    Returns (False, (0,0)) if a solution is NOT found """
    Indexes.remove((x, y))

    # Base Step
    badVals = [2, 3]
    if env[x][y] in badVals:
        return False, (0, 0)
    elif env[x][y] == 4:
        return True, (x, y)

    # Go Right
    if (x, y + 1) in Indexes:
        found, index = Solvable(env, x, y + 1, Indexes=Indexes)
        if found: return (found, index)

    # Go Down
    if (x + 1, y) in Indexes:
        found, index = Solvable(env, x + 1, y, Indexes=Indexes)
        if found: return (found, index)

    # Go Left
    if (x, y - 1) in Indexes:
        found, index = Solvable(env, x, y - 1, Indexes=Indexes)
        if found: return (found, index)

    # Go Up
    if (x - 1, y) in Indexes:
        found, index = Solvable(env, x - 1, y, Indexes=Indexes)
        if found: return (found, index)

    return False, (0, 0)


if __name__ == '__main__':
    env = getEnv()
    print(env)
    print()
    print(Solvable(env))
