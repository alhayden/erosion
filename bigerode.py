#!/bin/python


from random import random, randint
from outputs import *
from matxutils import *


def buildField(matx):
    volume = makerix(len(matx) - 1)
    velocity = [[ [0, 0, 0] for x in range(len(matx) - 1)] for y in range(len(matx) - 1)]


if __name__ == "__main__":
    m = makerix(8)
    buildField(m)
