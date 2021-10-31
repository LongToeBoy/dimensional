import numpy as np


class Point():

    def __init__(self, array=None):
        self.x, self.y, self.z = array
        self.iterer = None
        self.x *= 1.0
        self.y *= 1.0
        self.z *= 1.0

    def __add__(self, other):
        if(isinstance(other, Point)):
            return(Point([self.x+other.x, self.y+other.y, self.z+other.z]))

        return(Point([self.x+other, self.y+other, self.z+other]))

    def __radd__(self, other):
        if(isinstance(other, Point)):
            return(Point([self.x+other.x, self.y+other.y, self.z+other.z]))
        print(other)

        return(Point([self.x+other, self.y+other, self.z+other]))

    def __mul__(self, other):
        if isinstance(other, Point):
            return(Point([self.x*other.x, self.y*other.y, self.z*other.z]))

        return(Point([self.x*other, self.y*other, self.z*other]))

    def __truediv__(self, other):
        return(Point([self.x/other, self.y/other, self.z/other]))

    def __eq__(self, point):
        return(self.x == point.x and self.y == point.y and self.z == point.z)

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


class Line():
    def __init__(self, point_arr=None):
        self.points = point_arr
        self.iterer = None

    def auto(self, point_arr):
        pointsLen = len(point_arr)
        linesArr = []
        for i in range(pointsLen):
            linesArr.append(
                Line([point_arr[i % pointsLen], point_arr[(i+1) % pointsLen]]))
        return(linesArr)

    def __iter__(self):
        self.iterer = iter(self.points)
        return(self.iterer)

    def __next__(self):
        return(next(self.iterer))

    def __getitem__(self, index):
        return(self.points[index])

    def __mul__(self, other):
        self.points[0].x *= other
        self.points[0].y *= other
        self.points[0].z *= other
        self.points[1].x *= other
        self.points[1].y *= other
        self.points[1].z *= other
        return(self)

    def __truediv__(self, other):
        self.points[0].x /= other
        self.points[0].y /= other
        self.points[0].z /= other
        self.points[1].x /= other
        self.points[1].y /= other
        self.points[1].z /= other
        return(self)

    def dot(self, other):
        Ax = self.points[1].x-self.points[0].x
        Ay = self.points[1].y-self.points[0].y
        Az = self.points[1].z-self.points[0].z
        Bx = other.points[1].x-other.points[0].x
        By = other.points[1].y-other.points[0].y
        Bz = other.points[1].z-other.points[0].z
        return(Ax*Bx+Ay*By+Az*Bz)

    def cross(self, other):
        Ax = self.points[1].x-self.points[0].x
        Ay = self.points[1].y-self.points[0].y
        Az = self.points[1].z-self.points[0].z
        Bx = other.points[1].x-other.points[0].x
        By = other.points[1].y-other.points[0].y
        Bz = other.points[1].z-other.points[0].z
        cP=Point([Ay*Bz-Az*By, Az*Bx-Ax*Bz, Ax*By-Ay*Bx])
        return(cP)

    def length(self):
        x1 = self.points[1].x-self.points[0].x
        y1 = self.points[1].y-self.points[0].y
        z1 = self.points[1].z-self.points[0].z
        return((x1**2+y1**2+z1**2)**0.5)


class Vector():
    def __init__(self, point):
        self.point = point
        self.normalize()

    def normalize(self):
        x, y, z = self.point.coords()
        length = (x*x+y*y+z*z)**0.5
        for i in range(3):
            if(length>0):
                self.point[i] = self.point[i]/length

    def x(self):
        return(self.point.x)

    def y(self):
        return(self.point.y)

    def z(self):
        return(self.point.z)

    def dot(self, other):
        Ax, Ay, Az = self.point.coords()
        Bx, By, Bz = other.coords()

        return(Ax*Bx+Ay*By+Az*Bz)


class Polygon():
    def __init__(self, lines_arr=[]):
        self.lines = lines_arr
        self.iterer = None

    def append(self, line):
        self.lines.append(line)

    def __iter__(self):
        self.iterer = iter(self.lines)
        return(self.iterer)

    def __next__(self):
        return(next(self.iterer))


class Mesh():

    def __init__(self, polygons=None):
        self.polygons = polygons
        self.iteTris = None

    def load(self, obj):
        with open(obj, "r") as obj:
            arr = [l[:-1] for l in obj]
            length = len(arr)
            self.polygons = []
            points = []

            for index, line in enumerate(arr):
                if(index*100/length % 5 == 0):
                    print(f"{100*index/length}%")
                line = line.split()
                if(6 > len(line) > 1):
                    if (line[0] == "v"):
                        points.append(Point([float(o) for o in line[1:]])
                                      )
                    elif(line[0] == "vn"):
                        pass
                    elif(line[0] == "vt"):
                        pass
                    elif(line[0] == "f"):
                        p4l = [points[int(o[0])-1] for o in line[1:]]
                        self.polygons.append(
                            Polygon(Line().auto(p4l))
                        )
            return(len(self.polygons))

    def __iter__(self):
        self.iteTris = iter(self.polygons)
        return(self.iteTris)

    def __next__(self):
        return(next(self.iteTris))


class Cube(Mesh):

    def __init__(self, side=1):
        self.polygons = []
        side *= 0.5
        points = [
            Point([-side, -side, -side]),
            Point([-side, +side, -side]),
            Point([+side, +side, -side]),
            Point([+side, -side, -side]),
            Point([-side, -side, +side]),
            Point([-side, +side, +side]),
            Point([+side, +side, +side]),
            Point([+side, -side, +side])
        ]

        self.polygons = [
            # Line cant have more than 2 points :)
            Polygon(Line().auto([points[0], points[1], points[2]])),
            Polygon(Line().auto([points[0], points[2], points[3]])),
            Polygon(Line().auto([points[1], points[5], points[6]])),
            Polygon(Line().auto([points[1], points[6], points[2]])),
            Polygon(Line().auto([points[5], points[4], points[7]])),
            Polygon(Line().auto([points[5], points[7], points[6]])),
            Polygon(Line().auto([points[4], points[0], points[3]])),
            Polygon(Line().auto([points[4], points[3], points[7]])),
            Polygon(Line().auto([points[4], points[5], points[1]])),
            Polygon(Line().auto([points[4], points[1], points[0]])),
            Polygon(Line().auto([points[3], points[2], points[6]])),
            Polygon(Line().auto([points[3], points[6], points[7]])),
        ]
