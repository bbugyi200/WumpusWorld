import os
import importlib
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-m', '--module', action='store', dest='module')
parser.add_option('-f', '--function', action='store', dest='function')
options, args = parser.parse_args()

os.system('clear')

modStr = options.module
funcStr = options.function

module = importlib.import_module('WumpusWorld.' + modStr)

if funcStr:
    Func = getattr(module, funcStr)
    argsList = dict()
    for i in range(10):
        if len(args) - 1 < i: break
        key, value = args[i].split('=')
        argsList.update({key: value})

    F = Func(**argsList)
