from math import ceil, floor

cache = (0, 0)

def makerix(size):
    '''creates a [size] x [size] matrix'''
    return [[0 for x in range(size)] for y in range(size)]

def sumMatrix(matrix1, matrix2):
    '''returns the sum of two matrices.  Does not manipulate original'''
    assert len(matrix1) == len(matrix2)
    matrix = matrix1[:]
    for x in range(len(matrix1)):
        assert len(matrix1[x]) == len(matrix2[x])
        for y in range(len(matrix1[x])):
            matrix[x][y] += matrix2[x][y]
    return matrix

def scaleMatrix(matx, scale):
    '''returns a scaled version of the input matrix using bilinear interpolation'''
    new = makerix(len(matx) * scale)
    l = len(matx)
    for x in range(len(new)):
        for y in range(len(new[x])):
            new[x][y] = bilinear(matx, (x * (l - 1)) / (l * scale), (y * (l - 1)) / (l * scale))
    return new

def bilinear(matx, x, y):
    '''returns the bilinear interpolation of a position in a matrix'''
    val = 0
    higher = [ceil(x+0.00000001), ceil(y+0.0000001)]
    lower = [floor(x), floor(y)]
    matrix = pad(matx)
    #print(higher)
    #print(lower)
    #if higher[0] >= len(matrix):
    #    higher[0] = lower[0]
    #
    #if higher[1] >= len(matrix[0]):
    #    higher[1] = lower[1]

    one = (higher[0] - x) * matrix[lower[0]][higher[1]] + (x - lower[0]) * matrix[higher[0]][higher[1]]
    two = (higher[0] - x) * matrix[lower[0]][lower[1]] + (x - lower[0]) * matrix[higher[0]][lower[1]]

    return (higher[1] - y) * two + (y - lower[1]) * one

def pad(mat):
    '''adds a row and column to the ends of a matrix'''
    global cache
    if mat == cache[0]:
        return cache[1]
    out = []
    for col in mat:
        c = col[:]
        c.append(col[len(col)-1])
        out.append(c)
    out.append(out[len(out)-1][:])
    cache = (mat, out)
    return out

def sumFuzzy(x, y, value, matx):
    '''adds a value to a matrix using i n t e r p o l a t  i o n'''
    adjacents = [(-1, -1, 0.025), (0, -1, 0.1), (1, -1, 0.025),
              (-1, 0, 0.1), (0, 0, 0.5), (1, 0, 0.1),
              (-1, 1, 0.025), (0, 1, 0.1), (1, 1, 0.025)]
    leftover = 0
    for a in adjacents:
        if 0 <= y + a[1] < len(matx) and 0 <= x + a[0] < len(matx):
            matx[y + a[1]][x + a[0]] += value * a[2]
        else:
            leftover += a[2] * value
    matx[y][x] += leftover
