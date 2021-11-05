import copy
import numpy as np


def dot(one, two):
    Ax = one[0]
    Ay = one[1]
    Az = one[2]
    Bx = two[0]
    By = two[1]
    Bz = two[2]
    return(Ax*Bx+Ay*By+Az*Bz)


def cross(one, two):
    Ax = one[0]
    Ay = one[1]
    Az = one[2]
    Bx = two[0]
    By = two[1]
    Bz = two[2]
    return([Ay*Bz-Az*By, Az*Bx-Ax*Bz, Ax*By-Ay*Bx])


def normalize(triplet):
    tr = triplet
    sumtr = (tr[0]**2+tr[1]**2+tr[2]**2)**0.5
    sumtr = 1/sumtr if sumtr != 0 else 0
    return([o*sumtr for o in tr])


class Mesh():

    def __init__(self, faces=[], vertices=[]):
        self.faces = faces
        self.vertices = vertices
        self.iterVar = None

    def load(self, obj):
        with open(obj, "r") as obj:
            arr = [l[:-1] for l in obj]
            length = len(arr)
            self.faces = []
            self.vertices = []

            for index, edge in enumerate(arr):
                if(index*100/length % 5 == 0):
                    print(f"{100*index/length}%")
                edge = edge.split()
                if(6 > len(edge) > 1):
                    if (edge[0] == "v"):
                        self.vertices.append([float(o) for o in edge[1:]])
                    elif(edge[0] == "vn"):
                        pass
                    elif(edge[0] == "vt"):
                        pass
                    elif(edge[0] == "f"):
                        #p4l = [self.vertices[int(o[0])-1] for o in edge[1:]]
                        self.faces.append(
                            [int(o.split('/')[0])-1 for o in edge[1:]])
            return(len(self.faces))

    def __iter__(self):
        self.iterVar = iter(self.faces)
        return(self.iterVar)

    def __next__(self):
        return(next(self.iterVar))


class Pyramid(Mesh):
    def __init__(self, side=1):

        self.faces = []
        side *= 0.5
        self.vertices = [
            [-side, -side, -side],  # 0 left, front, down
            [-side, -side, +side],  # 1 left, back, down
            [+side, -side, -side],  # 2 right, front, down
            [+side, -side, +side],  # 3 right, back, down
            [0.0, +side, 0.0]  # 4 top
        ]
        self.faces = [
            [0, 2, 3],
            [0, 3, 1],
            [0, 4, 2],
            [2, 4, 3],
            [3, 4, 1],
            [1, 4, 0]
        ]

        super().__init__(faces=self.faces, vertices=self.vertices)


class Cube(Mesh):

    def __init__(self, side=1):
        self.faces = []
        side *= 0.5
        self.vertices = [
            [-side, -side, -side],
            [-side, +side, -side],
            [+side, +side, -side],
            [+side, -side, -side],
            [-side, -side, +side],
            [-side, +side, +side],
            [+side, +side, +side],
            [+side, -side, +side]
        ]

        self.faces = [
            # Edge cant have more than 2 vertices :)
            [0, 1, 2],
            [0, 2, 3],
            [1, 5, 6],
            [1, 6, 2],
            [5, 4, 7],
            [5, 7, 6],
            [4, 0, 3],
            [4, 3, 7],
            [4, 5, 1],
            [4, 1, 0],
            [3, 2, 6],
            [3, 6, 7]
        ]
        super().__init__(faces=self.faces, vertices=self.vertices)
