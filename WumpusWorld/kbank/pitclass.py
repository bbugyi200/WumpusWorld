""" pitclass.py """

from collections import namedtuple
import itertools


class PitClass:
    def __init__(self, partition):

        BS = bitStrings(partition)
        bStrings = BS.get()

        Outcome = namedtuple('outcome', 'bitstr prob')
        self.outcomes = []


class bitStrings:
    def __init__(self, partition):
        self.length = len(partition)

        self.IMap = dict()
        for i, index in enumerate(partition):
            self.IMap[index] = i

        self.strings = [''.join(seq) for seq in itertools.product("01", repeat=self.length)]

    def get(self):
        return self.strings

if __name__ == '__main__':
    PC = PitClass
