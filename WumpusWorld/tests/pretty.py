from .. import constants as C


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def makePretty(env):
    """ Takes random environment and makes it easier on the eyes """
    Env = env.astype(str)

    for i in range(len(Env)):
        for j in range(len(Env[i])):
            if int(Env[i][j]) == C.Pit:
                Env[i][j] = bcolors.FAIL + 'P' + bcolors.ENDC
            elif int(Env[i][j]) == C.Wumpus:
                Env[i][j] = bcolors.BLUE + 'W' + bcolors.ENDC
            elif int(Env[i][j]) == C.Gold:
                Env[i][j] = bcolors.YELLOW + 'G' + bcolors.ENDC
            elif int(Env[i][j]) == C.Agent:
                Env[i][j] = bcolors.GREEN + bcolors.BOLD + 'A' + bcolors.ENDC

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


def printEnv(env):
    for row in env:
        for elem in row:
            print(elem, end='  ')
        print()
    print('\n')
