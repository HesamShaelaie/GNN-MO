from argparse import ArgumentError
from re import L

from random import randint, seed
from random import choice
# seed random number generator
seed(1)
import numpy as np

n =10
Neighbours = np.zeros(n, dtype=int)

for x in range(n):
    Neighbours[x] = randint(0,3000)

print(Neighbours)
ArgNeighbourMax = np.argsort(Neighbours)

print(ArgNeighbourMax)
print(np.flip(ArgNeighbourMax))



