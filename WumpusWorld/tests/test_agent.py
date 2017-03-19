from .. environment import getEnv
from . pretty import TitlePrint, printEnv, makePretty, bcolors
from .. stimuli import Stimuli
from .. agent import Agent
from . sims import getTestEnv
import os
import time


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

env = getEnv()
Env = makePretty(env)

stimArr = Stimuli(env).stimArr
A = Agent(stimArr)

oldIndex = (0, 0)
x, y = (0, 0)
while(True):
    TitlePrint('BitStrings')
    print(A.KB.PBank.PC.bstrings)
    TitlePrint('Probabilities')

    T = '====== {0} ======'
    # fmt = """
# {12:<30}{13:<30}{14}
# {0:<30}{4:<30}{8}
# {1:<30}{5:<30}{9}
# {2:<30}{6:<30}{10}
# {3:<30}{7:<30}{11}
# """

    fmt = """\
{3}\n{0}\n
{4}\n{1}\n
{5}\n{2}\n\n
"""

    PPs = [row[:] for row in A.KB.PBank.Probs]
    WPs = [row[:] for row in A.KB.WBank.Probs]

    DPs = []
    for i in range(len(PPs)):
        DPs.append([])
        for j in range(len(PPs[0])):
            DPs[i].append(round(PPs[i][j] + WPs[i][j], 3))

    for XXs in [PPs, WPs, DPs]:
        Indexes = [index for index in A.KB.visited | A.KB.options]
        for i, row in enumerate(XXs):
            for j, _ in enumerate(row):
                if (i, j) not in Indexes:
                    XXs[i][j] = '-'
            XXs[i] = str(XXs[i])

    # print(fmt.format(str('\n'.join(PPs)),
    #                  str('\n'.join(WPs)),
    #                  str('\n'.join(DPs)),
    #                  T.format('Pit'),
    #                  T.format('Wumpus'),
    #                  T.format('Death')))

    print(T.format('Death'))
    print('\n'.join(DPs), end='\n\n')

    TitlePrint('Environment')
    printEnv(Env)

    print('Position of Agent: ({0},{1})'.format(x, y), end='\n')

    getch = _GetchUnix()
    auto = False

    if auto:
        if A.dead or A.forfeit or A.foundG:
            userInput = 'N'
        else:
            userInput = 'r'
            time.sleep(0.5)
    else:
        userInput = getch()
    os.system('clear')

    """ Instructions

     print('~~~ Input Options ~~~',
           '1. hjkl commands to move',
           '2. Enter N to get a new random (non-modified) environment.',
           '3. Enter M to get a new modified environment.',
           sep='\n',
           end='\n\n')
    """

    oldIndex = (x, y)

    if userInput in 'hjklr':
        x, y = oldIndex
        Env[x][y] = bcolors.GREEN + 'X' + bcolors.ENDC

        if userInput == 'j':
            A.down()
        elif userInput == 'k':
            A.up()
        elif userInput == 'h':
            A.left()
        elif userInput == 'l':
            A.right()
        elif userInput == 'r':
            A.act()

        x, y = A.KB.location
        Env[x][y] = bcolors.GREEN + bcolors.BOLD + 'A' + bcolors.ENDC

    elif userInput in 'MNF0123456789':
        if userInput == 'M':
            env = getTestEnv()
            Env = makePretty(env)
        elif userInput == 'N':
            env = getEnv()
            Env = makePretty(env)
        elif userInput == 'F':
            env = getEnv(fair=True)
            Env = makePretty(env)
        else:
            env = getTestEnv(userInput)
            Env = makePretty(env)
        x, y = (0, 0)
        stimArr = Stimuli(env).stimArr
        A = Agent(stimArr)

    elif userInput == 'Q':
        exit()
