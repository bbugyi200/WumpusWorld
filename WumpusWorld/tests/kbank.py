from .. environment import getEnv
from . pretty import TitlePrint, printEnv, makePretty, bcolors
from .. stimuli import Stimuli
from .. kbank.kbank import KBank
from .. agent import Agent
from . sims import getTestEnv
import os
import numpy as np


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
    TitlePrint('Probabilities')
    T = '====== {0} ======'
    fmt = '{12:<30}{13:<30}{14}\n{0:<30}{4:<30}{8}\n{1:<30}{5:<30}{9}\n{2:<30}{6:<30}{10}\n{3:<30}{7:<30}{11}\n'
    print(fmt.format(str(A.KB.PBank.Probs[0]),
                     str(A.KB.PBank.Probs[1]),
                     str(A.KB.PBank.Probs[2]),
                     str(A.KB.PBank.Probs[3]),
                     str(A.KB.WBank.Probs[0]),
                     str(A.KB.WBank.Probs[1]),
                     str(A.KB.WBank.Probs[2]),
                     str(A.KB.WBank.Probs[3]),
                     str(np.array(A.KB.WBank.Probs[0]) + np.array(A.KB.PBank.Probs[0])),
                     str(np.array(A.KB.WBank.Probs[1]) + np.array(A.KB.PBank.Probs[1])),
                     str(np.array(A.KB.WBank.Probs[2]) + np.array(A.KB.PBank.Probs[2])),
                     str(np.array(A.KB.WBank.Probs[3]) + np.array(A.KB.PBank.Probs[3])),
                     T.format('Pit'),
                     T.format('Wumpus'),
                     T.format('Death')))

    # TitlePrint('BitStrings')
    # print('-----------RED---------------')
    # print(A.KB.PBank.Red.IMap.items())
    # for O in A.KB.PBank.Red.outcomes:
    #     print(O.bitstr, ' = ', O.prob)
    # print('-----------BLUE---------------')
    # print(A.KB.PBank.Blue.IMap.items())
    # for O in A.KB.PBank.Blue.outcomes:
    #     print(O.bitstr, ' = ', O.prob)

    TitlePrint('Environment')
    printEnv(Env)

    print('Position of Agent: ({0},{1})'.format(x, y), end='\n')

    getch = _GetchUnix()
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
        Env[oldIndex] = bcolors.GREEN + 'X' + bcolors.ENDC

        if userInput == 'j':
            A.down()
        elif userInput == 'k':
            A.up()
        elif userInput == 'h':
            A.left()
        elif userInput == 'l':
            A.right()
        elif userInput == 'r':
            A.run()

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
