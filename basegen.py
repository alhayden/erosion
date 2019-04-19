#!/bin/python

from random import random, randint
from matxutils import *

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

def generateBig(size):
    matx = makerix(size)
    levels = [(16, 0.3), (32, 0.15), (64, 0.1), (256, 0.01)]
    for l in levels:
        temp = makerix(l[0])
        randomPopulate(temp, l[1])
        temp = scaleMatrix(temp, size // l[0])
        matx = sumMatrix(matx, temp)
    for x in range(size):
        for y in range(size):
            matx[y][x] += x / (size * 1)
    return matx
