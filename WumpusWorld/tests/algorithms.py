""" tests.py

Set of functions intended to run specific tests on this program """

from ..algorithms import Solvable
from ..environment import getEnv, getIndexes
from sys import argv
import timeit


def TestSolvable(verbose=False, displayMax=10, loops=10000):
    """ Tests the Solvable function """
    loops = int(loops)
    displayMax = int(displayMax)
    verbose = int(verbose)

    if verbose:
        title = '*** Sample Subset of Unsolvable Environments Found ***'
        print()
        print('*' * len(title))
        print(title)
        print('*' * len(title))
        print()

    NotSCounter = 0
    AllSums = 0
    NotSSums = 0

    for i in range(loops):
        env = getEnv()
        AllSums += env.sum()
        Indexes = getIndexes()
        S = Solvable(env, Indexes=Indexes)

        if not S[0]:
            NotSCounter += 1
            NotSSums += env.sum()
            if verbose and NotSCounter < displayMax: print(env, '\n')

    percentNotS = (NotSCounter / loops) * 100
    title = '*** Statistics ***'
    bar = '*' * len(title)
    print(bar, title, bar, sep='\n', end='\n\n')
    print('- Average Matrix Sum for all Environments = %.2f' % (AllSums / loops))
    print('- Average Matrix Sum for Unsolvable Environments = %.2f' % (NotSSums / NotSCounter))
    print('-', NotSCounter,
          'out of', loops, 'environments were found to be unsolvable.',
          '(%.2f%%)' % percentNotS)


def TimeSolvable():
    """ Times the Solvable function """
    stmts = '''
env = getEnv()
Indexes = getIndexes()
Solvable(env, Indexes=Indexes)
'''

    setup = '''
from envsolver import Solvable
from environment import getEnv, getIndexes
'''

    number = 100000
    envTime = timeit.timeit('env = getEnv()',
                            setup=setup,
                            number=number)
    IndexTime = timeit.timeit('Indexes = getIndexes()',
                              setup=setup,
                              number=number)
    # extraTime = envTime + IndexTime

    extraTime = timeit.timeit('env = getEnv(); Indexes = getIndexes()',
                              setup=setup,
                              number=number)

    print('Time to Create Environment = ', envTime)
    print('Time to Create Indexes = ', IndexTime)
    print('Time when Indexes and Environment Created Together = ', extraTime)
    print('\nSolvable Function Time = ',
          timeit.timeit(stmts, setup=setup, number=number) - extraTime)


if __name__ == '__main__':
    argsList = dict()
    for i in range(2, 10):
        if len(argv) - 1 < i: break
        if argv[i][:2] == '--' and '=' in argv[i]:
            key, value = argv[i][2:].split('=')
            argsList.update({key: value})

    globals()[argv[1]](**argsList)
