#!/bin/python

from random import random, randint
from outputs import *
from matxutils import *
from basegen import *


##TODO velocity-based rates/spread, diagonals / rt2

size = 256
cache = (0, 0)
sqrt2 = 2 ** 0.5


def erode(x, y, matx):
    adjacency = [(-1, -1, sqrt2), (0, -1, 1), (-1, 0, 1), (-1, 1, sqrt2), (1, -1, sqrt2), (1, 0, 1), (0, 1, 1), (1, 1, sqrt2)]
    contents = 0
    maxContents = 0.02
    deltaContents = 0.001
    ttl = 0
    while 1 <= x < len(matx) - 1 and 1 <= y < len(matx) - 1:
        val = matx[y][x]
        others = sorted(adjacency[:], key=lambda k: matx[y + k[1]][x + k[0]] / k[2])
        h = others[0][0] + x
        j = others[0][1] + y
        if matx[j][h] >= val:
            break
        if contents < maxContents:
            delta = min(0.005, val - matx[j][h])
            sumFuzzy(x, y, delta * -1, matx)#matx[y][x] -= delta
            contents += delta
            #repose(x, y, matx)
        x = h
        y = j
        ttl += 1
        maxContents = max(maxContents - deltaContents, 0)
        if contents > maxContents:
            sumFuzzy(x, y, contents - maxContents, matx)
            contents = maxContents
    sumFuzzy(x, y, contents, matx)#matx[y][x] += contents
    #if matx[y][x] < 0:
    #    print(f'AAAAA!  {x}, {y} is {matx[y][x]}!')
    #repose(x, y, matx)

def repose(x, y, matx):
    val = matx[y][x]
    if 1 >= x or x >= len(matx) - 1 or 1 >= y or y >= len(matx) - 1:
        return
    adjacency = [(-1, -1), (0, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (0, 1), (1, 1)]
    slopes = [val - matx[y + a[1]][x + a[0]] for a in adjacency]
    for s in range(len(slopes)):
        if abs(slopes[s]) > 0.085:
            slump([x, y], [x + adjacency[s][0], y + adjacency[s][1]], matx)

def slump (a, b, matx):
    delta = matx[a[0]][a[1]] - matx[b[0]][b[1]]
    if delta < 0:
        delta *= -1
        c = b
        b = a
        a = c
    dd = (delta - 0.085) / 2
    matx[a[0]][a[1]] -= dd
    matx[b[0]][b[1]] += dd

#    repose(a[0], a[1], matx)
#    repose(b[0], b[1], matx)

def erode2(x, y, matx):
    adjacency = [(1, 1), (1, 0), (0, 1), (-1, -1), (, -1, 0), (0 ,-1), (-1 ,1), (1, -1)]
    v = [0, 0]
    adjacency = sorted(adjacency[:], key=lambda k: matx[y + k[1]][x + k[0]])
    
    
    
def addV(v, n, loc):
    if abs(loc[0]) + abs(loc[1]) > 1:
        n = n / 2
    if abs(loc[0]) > 0:
        v[0] += n ** 2 / n
    if abs(loc[1]) > 0:
        v[1] += n ** 2 / n
    return n

def runErode2(matx, n):
    for x in range(n):
        print(f"running {x} of {n}")
        erode2(randint(0, len(matx) - 1), randint(0, len(matx) - 1), matx)


if __name__ == "__main__":
    siz = 256
    #terrain = generateBase(siz)
    #terrain = generateBaseMagic(siz)
    terrain = generateBig(siz)
    for x in range(70000):
        if x % 10000 == 0:
            print(x)
        erode(randint(0, siz-1), randint(0, siz-1), terrain)

    stlify(terrain,horizscale=0.5).save("terrain.stl")
