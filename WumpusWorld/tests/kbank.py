from .. environment import getEnv
from . pretty import TitlePrint, printEnv, makePretty, bcolors
from .. stimuli import Stimuli
from .. kbank.kbank import KBank
from . sims import getTestEnv
import os


env = getEnv()
Env = makePretty(env)

stimArr = Stimuli(env).stimArr
K = KBank(stimArr)

oldIndex = (0, 0)
x, y = (0, 0)
while(True):
    TitlePrint('Probabilities')
    T = '====== {0} ======'
    fmt = '{12:<30}{13:<30}{14}\n{0:<30}{4:<30}{8}\n{1:<30}{5:<30}{9}\n{2:<30}{6:<30}{10}\n{3:<30}{7:<30}{11}\n'
    print(fmt.format(str(K.PBank.Probs[0]),
                     str(K.PBank.Probs[1]),
                     str(K.PBank.Probs[2]),
                     str(K.PBank.Probs[3]),
                     str(K.WBank.Probs[0]),
                     str(K.WBank.Probs[1]),
                     str(K.WBank.Probs[2]),
                     str(K.WBank.Probs[3]),
                     str(K.GBank.Probs[0]),
                     str(K.GBank.Probs[1]),
                     str(K.GBank.Probs[2]),
                     str(K.GBank.Probs[3]),
                     T.format('Pit'),
                     T.format('Wumpus'),
                     T.format('Gold')))

    # TitlePrint('BitStrings')
    # print('-----------RED---------------')
    # print(K.PBank.Red.IMap.items())
    # for O in K.PBank.Red.outcomes:
    #     print(O.bitstr, ' = ', O.prob)
    # print('-----------BLUE---------------')
    # print(K.PBank.Blue.IMap.items())
    # for O in K.PBank.Blue.outcomes:
    #     print(O.bitstr, ' = ', O.prob)

    TitlePrint('Environment')
    printEnv(Env)

    print('Position of Agent: ({0},{1})'.format(x, y), end='\n\n')

    userInput = input('>>> ')
    os.system('clear')

    """ Instructions

     print('~~~ Input Options ~~~',
           '1. Enter Index (x y) to move agent.',
           '2. Enter N to get a new random (non-modified) environment.',
           '3. Enter M to get a new random (modified) environment.',
           sep='\n',
           end='\n\n')
    """

    oldIndex = (x, y)
    if len(userInput.split()) == 2:
        Env[oldIndex] = bcolors.GREEN + 'X' + bcolors.ENDC
        x, y = userInput.split()
        x = int(x); y = int(y)
        Env[x][y] = bcolors.GREEN + bcolors.BOLD + 'A' + bcolors.ENDC
        for Bank in K.BankList:
            Bank.update(index=(x, y))
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
