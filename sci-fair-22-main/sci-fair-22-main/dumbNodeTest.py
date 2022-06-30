# from node import Node
from api import Foldapi
import asyncio
import random
import time
from graphviz import Digraph


# gra = Digraph('testGraph')
#
# gra.node('a','node 1',shape = 'rectangle')
# gra.node('b','node 2',shape='rectangle')
# gra.node('c','node 3',shape='rectangle')
# gra.node('d','node 4',shape='rectangle')
# gra.node('e','node 5',shape='rectangle')
# gra.node('f','node 6',shape='rectangle')
# gra.node('g','node 7',shape='rectangle')
# gra.node('h','node 8',shape='rectangle')
#
# gra.edges(['ab','bc','cd','de','df','fg','ch'])
#
# gra.attr(rankdir='LR')
#
# print(gra.source)
#
# a=gra.render()
#
# print(a)

a = [1, 2, 3, 4, 5, 6, 7]

i = slice(1,4)

print(a[i])