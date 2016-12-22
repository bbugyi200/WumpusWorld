from environment import getEnv, getIndexes
import constants as C

env = getEnv()
Indexes = getIndexes()

senseMapping = SMap = {C.Pit: C.Wind,
                       C.Wumpus: C.Stench}


class Stimuli:
    def __init__(self, env):
        self.stimArr = [[set(), set(), set(), set()],
                        [set(), set(), set(), set()],
                        [set(), set(), set(), set()],
                        [set(), set(), set(), set()]]

        # Loops through each element in stimArr and sets the senses of that
        # element to correspond with the elements of env found to the left,
        # right, above, and below of the current index (x, y)
        for x, y in Indexes:
            if env[x][y] and env[x][y] != 1:
                self.addSense((x, y), env[x][y])

            if (x + 1, y) in Indexes:
                num = SMap.get(env[x + 1][y], None)
                if num:
                    self.addSense((x, y), num)

            if (x - 1, y) in Indexes:
                num = SMap.get(env[x - 1][y], None)
                if num:
                    self.addSense((x, y), num)

            if (x, y + 1) in Indexes:
                num = SMap.get(env[x][y + 1], None)
                if num:
                    self.addSense((x, y), num)

            if (x, y - 1) in Indexes:
                num = SMap.get(env[x][y - 1], None)
                if num:
                    self.addSense((x, y), num)

    def addSense(self, index, num):
        x, y = index
        self.stimArr[x][y].add(num)


if __name__ == '__main__':
    stimArr = Stimuli(env).stimArr
    print(env, end='\n\n')
    for row in stimArr:
        print(row)
