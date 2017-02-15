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
