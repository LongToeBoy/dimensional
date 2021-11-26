import copy
import numpy as np


projMat = np.zeros(16).reshape((4, 4))
rotMatZ = np.zeros(9).reshape((3, 3))
rotMatX = np.zeros(9).reshape((3, 3))
rotMatY = np.zeros(9).reshape((3, 3))
rotMatZ[2][2] = 1
rotMatX[0][0] = 1
rotMatY[1][1] = 1
projMat[0][0] = 1*1/np.tan(90*np.pi/360)
projMat[1][1] = 1/np.tan(90*np.pi/360)
projMat[2][2] = 1000.0/(1000-0.1)
projMat[3][2] = (-1000*0.1)/(1000-0.1)
projMat[2][3] = 1.0


def rotateX(point, elapsed):
    rotMatX[1][1] = np.cos(elapsed)
    rotMatX[1][2] = np.sin(elapsed)
    rotMatX[2][1] = -np.sin(elapsed)
    rotMatX[2][2] = np.cos(elapsed)
    dot1 = np.matmul(point, rotMatX)
    return(dot1)


def rotateY(point, elapsed):
    rotMatY[0][0] = np.cos(elapsed)
    rotMatY[0][2] = np.sin(elapsed)
    rotMatY[2][0] = -np.sin(elapsed)
    rotMatY[2][2] = np.cos(elapsed)
    dot1 = np.matmul(point, rotMatY)
    return(dot1)


def rotateZ(point, elapsed):
    rotMatZ[0][0] = np.cos(elapsed)
    rotMatZ[0][1] = np.sin(elapsed)
    rotMatZ[1][0] = -np.sin(elapsed)
    rotMatZ[1][1] = np.cos(elapsed)
    dot1 = np.matmul(point, rotMatZ)
    return(dot1)


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


class World():
    def __init__(self, aspectRatio=1.0, fFov=90, fFar=1000, fNear=0.1):
        fFovRad = 1/np.tan(fFov*np.pi/360)
        projMat[0][0] = aspectRatio*fFovRad
        projMat[1][1] = fFovRad
        projMat[2][2] = fFar/(fFar-fNear)
        projMat[3][2] = (-fFar*fNear)/(fFar-fNear)


class Mesh():

    def __init__(self, faces=[], vertices=[]):
        self.faces = faces
        self.vertices = vertices
        self.iterVar = None

    def __iter__(self):
        self.iterVar = iter(self.faces)
        return(self.iterVar)

    def __next__(self):
        return(next(self.iterVar))

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
                        self.faces.append(
                            [int(o.split('/')[0])-1 for o in edge[1:]])
            return(len(self.faces))

    def sorter(self, faces, points_arrs):
        faces = copy.deepcopy(faces)
        faces.sort(reverse=False, key=lambda pnts:
                   sum([(points_arrs[indx])[2] for indx in pnts])/len(pnts))
        return(faces)

    def push(self, pushAr):
        x, y, z = pushAr
        for i in range(len(self.vertices)):
            self.vertices[i][0] += x
            self.vertices[i][1] += y
            self.vertices[i][2] += z

    def rotateZ(self, angle):
        for i, point in enumerate(self.vertices):
            rotatedPZ = rotateZ(point, angle)
            self.vertices[i] = rotatedPZ

    def rotateY(self, angle):
        for i, point in enumerate(self.vertices):
            rotatedPY = rotateY(point, angle)
            self.vertices[i] = rotatedPY


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
