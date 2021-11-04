import copy
import numpy as np


class Vertex():

    def __init__(self, array=None):
        self.x, self.y, self.z = array
        self.iterer = None
        self.x *= 1.0
        self.y *= 1.0
        self.z *= 1.0

    def __add__(self, other):
        if(isinstance(other, Vertex)):
            return(Vertex([self.x+other.x, self.y+other.y, self.z+other.z]))

        return(Vertex([self.x+other, self.y+other, self.z+other]))

    def __radd__(self, other):
        if(isinstance(other, Vertex)):
            return(Vertex([self.x+other.x, self.y+other.y, self.z+other.z]))
        print(other)

        return(Vertex([self.x+other, self.y+other, self.z+other]))

    def __mul__(self, other):
        if isinstance(other, Vertex):
            return(Vertex([self.x*other.x, self.y*other.y, self.z*other.z]))

        return(Vertex([self.x*other, self.y*other, self.z*other]))

    def __truediv__(self, other):
        return(Vertex([self.x/other, self.y/other, self.z/other]))

    def __eq__(self, vertex):
        return(self.x == vertex.x and self.y == vertex.y and self.z == vertex.z)

    def __iter__(self):
        self.iterer = iter([self.x, self.y, self.z])
        return(self.iterer)

    def __next__(self):
        return(next(self.iterer))

    def __getitem__(self, index):
        if(index == 0):
            return(self.x)
        elif(index == 1):
            return(self.y)
        elif(index == 2):
            return(self.z)

    def __setitem__(self, index, val):
        if(index == 0):
            self.x = val
        elif(index == 1):
            self.y = val
        elif(index == 2):
            self.z = val

    def coords(self, extra=None):
        if(extra is not None):
            return([self.x, self.y, self.z, extra])
        else:
            return([self.x, self.y, self.z])

    def __repr__(self) -> str:
        return(f"({self.x},{self.y},{self.z})")


class Edge():
    def __init__(self, vertex_arr=None, index_arr=None):
        self.vertices = vertex_arr
        self.index_arr = index_arr
        self.iterer = None

    def auto(self, vertex_arr, index_arr):
        verticesLen = len(vertex_arr)
        edgesArr = []
        for i in range(verticesLen):
            edgesArr.append(
                Edge([vertex_arr[i % verticesLen], vertex_arr[(i+1) % verticesLen]], [index_arr[i % verticesLen], index_arr[(i+1) % verticesLen]]))
        return(edgesArr)

    def __iter__(self):
        self.iterer = iter(self.vertices)
        return(self.iterer)

    def __next__(self):
        return(next(self.iterer))

    def __getitem__(self, index):
        return(self.vertices[index])

    def __mul__(self, other):
        newEdge = copy.deepcopy(self)
        newEdge.vertices[0].x *= other
        newEdge.vertices[0].y *= other
        newEdge.vertices[0].z *= other
        newEdge.vertices[1].x *= other
        newEdge.vertices[1].y *= other
        newEdge.vertices[1].z *= other
        return(newEdge)

    def __truediv__(self, other):
        newEdge = copy.deepcopy(self)
        newEdge.vertices[0].x /= other
        newEdge.vertices[0].y /= other
        newEdge.vertices[0].z /= other
        newEdge.vertices[1].x /= other
        newEdge.vertices[1].y /= other
        newEdge.vertices[1].z /= other
        return(newEdge)

    def dot(self, other):
        Ax = self.vertices[1].x-self.vertices[0].x
        Ay = self.vertices[1].y-self.vertices[0].y
        Az = self.vertices[1].z-self.vertices[0].z
        Bx = other.vertices[1].x-other.vertices[0].x
        By = other.vertices[1].y-other.vertices[0].y
        Bz = other.vertices[1].z-other.vertices[0].z
        return(Ax*Bx+Ay*By+Az*Bz)

    def cross(self, other):
        Ax = self.vertices[1].x-self.vertices[0].x
        Ay = self.vertices[1].y-self.vertices[0].y
        Az = self.vertices[1].z-self.vertices[0].z
        Bx = other.vertices[1].x-other.vertices[0].x
        By = other.vertices[1].y-other.vertices[0].y
        Bz = other.vertices[1].z-other.vertices[0].z
        cP = Vertex([Ay*Bz-Az*By, Az*Bx-Ax*Bz, Ax*By-Ay*Bx])
        return(cP)

    def __repr__(self) -> str:
        return(f"{self.vertices}")

    def length(self):
        x1 = self.vertices[1].x-self.vertices[0].x
        y1 = self.vertices[1].y-self.vertices[0].y
        z1 = self.vertices[1].z-self.vertices[0].z
        return((x1**2+y1**2+z1**2)**0.5)


class Vector():
    def __init__(self, vertex):
        self.vertex = vertex
        self.normalize()

    def normalize(self):
        x, y, z = self.vertex.coords()
        length = (x*x+y*y+z*z)**0.5
        for i in range(3):
            if(length > 0):
                self.vertex[i] = self.vertex[i]/length

    def x(self):
        return(self.vertex.x)

    def y(self):
        return(self.vertex.y)

    def z(self):
        return(self.vertex.z)

    def dot(self, other):
        Ax, Ay, Az = self.vertex.coords()
        Bx, By, Bz = other.coords()

        return(Ax*Bx+Ay*By+Az*Bz)


class Face():
    def __init__(self, edges_arr=[],):
        self.edges = edges_arr
        self.iterer = None

    def append(self, edge):
        self.edges.append(edge)

    def __iter__(self):
        self.iterer = iter(self.edges)
        return(self.iterer)

    def __next__(self):
        return(next(self.iterer))

    def __repr__(self) -> str:
        return(f"{self.edges}")


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
            vertices = []

            for index, edge in enumerate(arr):
                if(index*100/length % 5 == 0):
                    print(f"{100*index/length}%")
                edge = edge.split()
                if(6 > len(edge) > 1):
                    if (edge[0] == "v"):
                        vertices.append(Vertex([float(o) for o in edge[1:]])
                                        )
                    elif(edge[0] == "vn"):
                        pass
                    elif(edge[0] == "vt"):
                        pass
                    elif(edge[0] == "f"):
                        p4l = [vertices[int(o[0])-1] for o in edge[1:]]
                        self.faces.append(
                            Face(Edge().auto(p4l))
                        )
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
            Vertex([-side, -side, -side]),  # 0 left, front, down
            Vertex([-side, -side, +side]),  # 1 left, back, down
            Vertex([+side, -side, -side]),  # 2 right, front, down
            Vertex([+side, -side, +side]),  # 3 right, back, down
            Vertex([0.0, +side, 0.0]),  # 4 top
        ]
        self.faces = [
            Face(Edge().auto(
                [self.vertices[0], self.vertices[2], self.vertices[3]], [0, 2, 3])),
            Face(Edge().auto(
                [self.vertices[0], self.vertices[3], self.vertices[1]], [0, 3, 1])),
            Face(Edge().auto(
                [self.vertices[0], self.vertices[4], self.vertices[2]], [0, 4, 2])),
            Face(Edge().auto(
                [self.vertices[2], self.vertices[4], self.vertices[3]], [2, 4, 3])),
            Face(Edge().auto(
                [self.vertices[3], self.vertices[4], self.vertices[1]], [3, 4, 1])),
            Face(Edge().auto(
                [self.vertices[1], self.vertices[4], self.vertices[0]], [1, 4, 0])),

        ]

        super().__init__(faces=self.faces, vertices=self.vertices)


class Cube(Mesh):

    def __init__(self, side=1):
        self.faces = []
        side *= 0.5
        self.vertices = [
            Vertex([-side, -side, -side]),
            Vertex([-side, +side, -side]),
            Vertex([+side, +side, -side]),
            Vertex([+side, -side, -side]),
            Vertex([-side, -side, +side]),
            Vertex([-side, +side, +side]),
            Vertex([+side, +side, +side]),
            Vertex([+side, -side, +side])
        ]

        self.faces = [
            # Edge cant have more than 2 vertices :)
            Face(Edge().auto(
                [self.vertices[0], self.vertices[1], self.vertices[2]], [0, 1, 2])),
            Face(Edge().auto(
                [self.vertices[0], self.vertices[2], self.vertices[3]], [0, 2, 3])),
            Face(Edge().auto(
                [self.vertices[1], self.vertices[5], self.vertices[6]], [1, 5, 6])),
            Face(Edge().auto(
                [self.vertices[1], self.vertices[6], self.vertices[2]], [1, 6, 2])),
            Face(Edge().auto(
                [self.vertices[5], self.vertices[4], self.vertices[7]], [5, 4, 7])),
            Face(Edge().auto(
                [self.vertices[5], self.vertices[7], self.vertices[6]], [5, 7, 6])),
            Face(Edge().auto(
                [self.vertices[4], self.vertices[0], self.vertices[3]], [4, 0, 3])),
            Face(Edge().auto(
                [self.vertices[4], self.vertices[3], self.vertices[7]], [4, 3, 7])),
            Face(Edge().auto(
                [self.vertices[4], self.vertices[5], self.vertices[1]], [4, 5, 1])),
            Face(Edge().auto(
                [self.vertices[4], self.vertices[1], self.vertices[0]], [4, 1, 0])),
            Face(Edge().auto(
                [self.vertices[3], self.vertices[2], self.vertices[6]], [3, 2, 6])),
            Face(Edge().auto(
                [self.vertices[3], self.vertices[6], self.vertices[7]], [3, 6, 7])),
        ]
        super().__init__(faces=self.faces, vertices=self.vertices)
