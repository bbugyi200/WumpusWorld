""" tests.py

Set of functions intended to run specific tests on this program """

from algorithms import Solvable
from environment import getEnv, getIndexes
from sys import argv
import timeit
import random
import constants as C


def makePretty(env):
    """ Takes random environment and makes it easier on the eyes """
    Env = env.astype(str)

    for i in range(len(Env)):
        for j in range(len(Env[i])):
            if int(Env[i][j]) == C.Pit:
                Env[i][j] = 'P'
            elif int(Env[i][j]) == C.Wumpus:
                Env[i][j] = 'W'
            elif int(Env[i][j]) == C.Gold:
                Env[i][j] = 'G'
            elif int(Env[i][j]) == 1:
                Env[i][j] = 'A'

    return Env


def TitlePrint(title):
    """ Pretty-Prints a title

        Intended to be used for demonstration purposes """
    titleLength = len(title)
    barLength = titleLength + 12
    fmtdTitle = '----- {0} -----'.format(title)
    bar = '-' * barLength
    print(bar, fmtdTitle, bar,
          sep='\n', end='\n\n')


def TestSolvable(verbose=False, displayMax=10, loops=10000):
    """ Tests the Solvable function """
    loops = int(loops)
    displayMax = int(displayMax)

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


def PPSim(num, tests=100000, GP=0.2, IncludeGold=False):
    """ Simulates Pit Probabilities """
    numOfSuccesses = 0
    total = tests
    for x in range(tests):
        num = int(num)
        squares = [0] * num
        pit_probability = [0, 0, 0, 0, 1]
        Indexes = list(range(num))

        # selected = random.choice(Indexes)
        # squares[selected] = 1
        # Indexes.remove(selected)

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


if __name__ == '__main__':
    # argsList = dict()
    # for i in range(2, 10):
    #     if len(argv) - 1 < i: break
    #     if argv[i][:2] == '--' and '=' in argv[i]:
    #         key, value = argv[i][2:].split('=')
    #         argsList.update({key: value})

    # globals()[argv[1]](**argsList)

    PPSim(argv[1])
