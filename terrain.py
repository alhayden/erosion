#!/bin/python

from random import random, randint
from outputs import *
from matxutils import *


##TODO velocity-based rates/spread, diagonals / rt2

size = 256
cache = (0, 0)
sqrt2 = 2 ** 0.5

def generateBase(size):
    terrain = makerix(size)
    L = 4
    base = 0.5
    for x in range(L):
        l = int(2 ** (1+x))
        temp = makerix(size // l)
        randomPopulate(temp, 0.5 / (L - x))
        temp = scaleMatrix(temp, l)
        terrain = sumMatrix(terrain, temp)
        #imageify(temp).show()
        #input("")

    return terrain

def generateBaseMagic(size):
    matx = makerix(size)
    #levels = [(8, 0.7), (16, 0.2), (32, 0.1), (64, 0.05)]
    levels = [(8, 2), (16, 0.5), (32, 0.25), (64, 0.125), (256, 0.01)]
    for l in levels:
        temp = makerix(l[0])
        randomPopulate(temp, l[1])
        temp = scaleMatrix(temp, size // l[0])
        matx = sumMatrix(matx, temp)
    return matx

def generateBaseBlob(size):
    matx = makerix(size)
    levels = [(4, 1, 64), (8, 0.5, 32), (16, 0.25, 16), (32, 0.125, 8), (64, 0.1, 4)]
    for l in levels:
        blobPopulate(matx, l[0], l[1], l[2])
    return matx

def randomPopulate(matx, n):
    for x in range(len(matx)):
        for y in range(len(matx)):
            if random() < 0.5:
                matx[x][y] = n
    return matx

def blobPopulate(matx, f, n, r):
    for x in range(len(matx)):
        for y in range(len(matx)):
            if random() < f / len(matx) ** 2:
                for a in range(-r, r):
                    for b in range(-r, r):
                        if 0 > y + b or y + b >= len(matx) or 0 > x + a or x + a >= len(matx):
                            continue
                        d = (a ** 2 + b ** 2) ** 0.5
                        d = d / r
                        matx[y + b][x + a] += n * (-d ** 3 + 1)
    return matx

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


siz = 256
#terrain = generateBase(siz)
terrain = generateBaseMagic(siz)
for x in range(70000):
    if x % 10000 == 0:
        print(x)
    erode(randint(0, siz-1), randint(0, siz-1), terrain)

stlify(terrain,horizscale=0.5).save("terrain.stl")
