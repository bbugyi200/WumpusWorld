from ..environment import getEnv
from .pretty import TitlePrint, makePretty
from ..stimuli import Stimuli
from ..kbank import KBank
from .sims import getTestEnv
import os


env = getEnv()
Env = makePretty(env)

stimArr = Stimuli(env).stimArr
K = KBank(stimArr)

oldIndex = (0, 0)
x, y = (0, 0)
while(True):
    TitlePrint('Percepts')
    count = 0
    for row in K.pKbase:
        for percept in row:
            count += 1
            if count % 4 == 0:
                print(percept)
            else:
                print(percept, end=' --- ')
    print()
    for row in K.wKbase:
        for percept in row:
            count += 1
            if count % 4 == 0:
                print(percept)
            else:
                print(percept, end=' --- ')
    print()

    for row in K.gKbase:
        for percept in row:
            count += 1
            if count % 4 == 0:
                print(percept)
            else:
                print(percept, end=' --- ')
    print()

    TitlePrint('Probabilities')
    T = '====== {0} ======'
    fmt = '{12:<30}{13:<30}{14}\n{0:<30}{4:<30}{8}\n{1:<30}{5:<30}{9}\n{2:<30}{6:<30}{10}\n{3:<30}{7:<30}{11}\n'
    print(fmt.format(str(K.pProb[0]),
                     str(K.pProb[1]),
                     str(K.pProb[2]),
                     str(K.pProb[3]),
                     str(K.wProb[0]),
                     str(K.wProb[1]),
                     str(K.wProb[2]),
                     str(K.wProb[3]),
                     str(K.gProb[0]),
                     str(K.gProb[1]),
                     str(K.gProb[2]),
                     str(K.gProb[3]),
                     T.format('Pit'),
                     T.format('Wumpus'),
                     T.format('Gold')))

    TitlePrint('Environment')
    print(Env, end='\n\n')

    print('Position of Agent: ({0},{1})'.format(x, y), end='\n\n')

    userInput = input('>>> ')
    os.system('clear')

    ##### Instructions #####
    #
    # print('~~~ Input Options ~~~',
    #       '1. Enter Index (x y) to move agent.',
    #       '2. Enter N to get a new random (non-modified) environment.',
    #       '3. Enter M to get a new random (modified) environment.',
    #       sep='\n',
    #       end='\n\n')

    oldIndex = (x, y)
    if len(userInput.split()) == 2:
        Env[oldIndex] = 'X'
        x, y = userInput.split()
        x = int(x); y = int(y)
        Env[x][y] = 'A'
        K.update(index=(x, y))
    elif userInput in 'MN':
        if userInput == 'M':
            env = getTestEnv()
            Env = makePretty(env)
        elif userInput == 'N':
            env = getEnv()
            Env = makePretty(env)
        x, y = (0, 0)
        stimArr = Stimuli(env).stimArr
        K = KBank(stimArr)
    elif userInput == 'P':
        TitlePrint('Percepts')
        for row in K.pKbase:
            print(row)
        print()
