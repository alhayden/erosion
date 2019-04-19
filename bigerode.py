#!/bin/python


from random import random, randint, shuffle
from outputs import *
from matxutils import *
from terrain import *

adjacency = [(-1, -1), (0, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (0, 1), (1, 1)]


def calculateFlows(matx):
    # initial condition: 1 rain unit at each point with zero velocity
    size = len(matx)
    volume = [[1 for x in range(size)] for y in range(size)]
    velocity = makerix(size)
    
    #assume water flows straight downhill, v doesn't need direction
    #velocity = [[ [0, 0] for x in range(len(matx) - 1)] for y in range(len(matx) - 1)]
    
    # work from top to bottom (assume no water flows uphill)
    locations = []
    for x in range(size - 2):
        for y in range(size - 2):
            locations.append((x + 1, y + 1))
    locations = sorted(locations[:], key=lambda k: matx[k[1]][k[0]])

    ## calculate parameters
    for loc in locations:
        x = loc[0]
        y = loc[1]
        elev = matx[y][x]
        # get lowest neighbor
        #shuffle(adjacency)
        others = sorted(adjacency[:], key=lambda k: matx[y + k[1]][x + k[0]])
        h = others[0][0] + x
        j = others[0][1] + y
        delta = elev - matx[j][h]
        # no lower adjacency
        if delta <= 0:
            if velocity[y][x] > (2 * 0.0981 * -delta) ** 0.5:
                velocity[y][x] -= (2 * 0.0981 * -delta) ** 0.5
            else:
                velocity[y][x] = 0
                continue
        else:
            # water speeds up
            velocity[y][x] += (2 * 0.0981 * delta) ** 0.5
        #water slows down
        velocity[y][x] -= (velocity[y][x] * 0.01)
        #update downstream
        volume[j][h] += volume[y][x]
        velocity[j][h] += velocity[y][x]
    ## erode based on parameters
    constant = 0.001
    for x in range(size):
        for y in range(size):
            matx[y][x] -= constant * (volume[y][x] / size ** 2) * velocity[y][x]



if __name__ == "__main__":
    m = generateBig(256)
    for x in range(1000):
        print(f" {x} / 500   ",end="\r")
        calculateFlows(m)
    stlify(m,horizscale=0.5).save("bigTerrain.stl")
