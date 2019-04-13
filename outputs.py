from PIL import Image
import numpy as np
from stl import mesh

def pront(matx):
    print("-" * len(matx[0]))
    for line in matx:
        print(line)
    print('-' * len(matx[0]))

def imageify(matx):
    img = Image.new('L', (len(matx),len(matx)), 255)
    for y in range(len(matx)):
        for x in range(len(matx)):
            img.putpixel((x, y), int(matx[y][x] * 255))
    return img

def stlify(matx, box=True, height=10, horizscale=1):
    vertices = []
    for x in range(len(matx)):
        for y in range(len(matx)):
            vertices.append(np.asarray([x, y, matx[x][y] * height]))
    offset = len(vertices)

    if box:
        for x in range(len(matx)):
            for y in range(len(matx)):
                vertices.append(np.asarray([x, y, 0]))

    vertices = np.asarray(vertices)
    vertices[...,:2] *= horizscale
    faces = []

    for x in range(len(matx) - 1):
        for y in range(len(matx) -1):
            faces.append(np.asarray([x * len(matx) + y, x * len(matx) + y + 1, (x+1) * len(matx) + y + 1]))
            faces.append(np.asarray([x * len(matx) + y, (x + 1) * len(matx) + y, (x+1) * len(matx) + y + 1]))

    if box:
        for x in range(len(matx) - 1):
            for y in range(len(matx) - 1):
                l = len(matx)
                faces.append(np.asarray([x * l + y + offset, x * l + y + 1 + offset, (x+1) * l + y + 1 + offset]))
                faces.append(np.asarray([x * l + y + offset, (x + 1) * l + y + offset, (x + 1) * l + y + 1 + offset]))
        for i in range(len(matx) - 1):
            l = len(matx)
            l2 = l - 1
            ll = len(vertices) - 1
            faces.append(np.asarray([offset + i * l, i * l, (i+1) * l]))
            faces.append(np.asarray([offset + i * l, offset + (i+1) * l, (i+1) * l]))
            faces.append(np.asarray([offset + i, i, i + 1]))
            faces.append(np.asarray([offset + i, offset + i + 1, i + 1]))

            faces.append(np.asarray([offset + i * l + l2, i * l + l2, (i+1) * l + l2]))
            faces.append(np.asarray([offset + i * l + l2, offset + (i+1) * l + l2, (i+1) * l + l2]))
            faces.append(np.asarray([ll - offset - i, ll - i, ll - i - 1]))
            faces.append(np.asarray([ll - offset - i, ll - offset - i - 1, ll - i - 1]))

    faces = np.asarray(faces)

    stl = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            stl.vectors[i][j] = vertices[f[j],:]
    return stl
