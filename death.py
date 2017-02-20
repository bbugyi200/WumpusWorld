""" death.py """

from .. import constants as C


class Death(Exception):
    """ Exception class that will be raised in the event of the agent's
        death. """
    def __init__(self, DeathType=None):
        if DeathType == C.Pit:
            output = "The Agent has fallen down into a pit!!! SHE'S DEAD!!!"
        elif DeathType == C.Wumpus:
            output = "The Agent entered a room with the Wumpus!!! SHE HAS " \
                "BEEN EATEN!!!"
        else:
            output = "The Agent has went into a room with either a pit or a " \
                "wumpus!!! SHE IS DEAD!!!"

        Exception.__init__(self, output)
