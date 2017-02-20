from sys import argv
import os

os.system('clear')

A = argv[1]
if A == '-K':
    import WumpusWorld.tests.kbank
if A == '--sim':
    from WumpusWorld.tests.sims import PPSim
    PPSim(argv[2])
