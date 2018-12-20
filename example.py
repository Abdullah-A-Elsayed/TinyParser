import functions
from functions import *

h = open('input.txt')
text = h.read()

tokens = [i.split(', ') for i in text.strip().split('\n')]
i = 0
nodes = []
functions.tokens = tokens 
functions.i = i
functions.nodes = nodes
program()

draw(functions.nodes)
