from tkinter import Tk, Canvas, PhotoImage, Widget, mainloop
from tkinter.filedialog import askopenfilename

from math import sin
from threading import Thread
from dimensional import *
import time
import copy
import numpy as np
WIDTH, HEIGHT = 640, 480


window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
iters = 0
#img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), state="normal")
need_run = True
fNear = 0.1
fFar = 1000.0
fFov = 90.0
aspectRatio = HEIGHT*1.0/WIDTH
fFovRad = 1/np.tan(fFov*np.pi/360)
projMat = np.zeros(16).reshape((4, 4))
projMat[0][0] = aspectRatio*fFovRad
projMat[1][1] = fFovRad
projMat[2][2] = fFar/(fFar-fNear)
projMat[3][2] = (-fFar*fNear)/(fFar-fNear)
projMat[2][3] = 1.0
rotMatZ = np.zeros(9).reshape((3, 3))
rotMatX = np.zeros(9).reshape((3, 3))
rotMatZ[2][2] = 1
rotMatX[0][0] = 1


def rotateZ(point, elapsed):
    rotMatZ[0][0] = np.cos(elapsed)
    rotMatZ[0][1] = np.sin(elapsed)
    rotMatZ[1][0] = -np.sin(elapsed)
    rotMatZ[1][1] = np.cos(elapsed)

    dot1 = np.matmul(point.coords(), rotMatZ)
    return(Vertex(array=dot1))


def rotateX(point, elapsed):
    rotMatX[1][1] = np.cos(elapsed/2)
    rotMatX[1][2] = np.sin(elapsed/2)
    rotMatX[2][1] = -np.sin(elapsed/2)
    rotMatX[2][2] = np.cos(elapsed/2)

    dot1 = np.matmul(point.coords(), rotMatX)
    return(Vertex(array=dot1))


def draw(mesh):
    print("drawing")
    sttime = time.time()
    secRun = 0.0
    fps = 1/10.0
    while(secRun < 10):
        secRun += fps
        elapsed = time.time()-sttime
        if(elapsed < fps):
            time.sleep(fps-elapsed)
            sttime = time.time()
        canvas.delete("all")
        increment = (secRun)
        points_arr = [Vertex(vertex.coords()) for vertex in mesh.vertices]
        # print(mesh.vertices)
        for i, point in enumerate(points_arr):
            rotatedPZ = Vertex(rotateZ(point, increment))
            rotatedPX = Vertex(rotateX(rotatedPZ, increment))
            points_arr[i] = rotatedPX
            points_arr[i].z += 50
            # print(i,points_arr[i])
            # pass
        for polygon in mesh:
            lines = polygon.edges
            points = []
            for line in lines:
                for i in line.index_arr:
                    pnt = points_arr[i]
                    points.append(Vertex(pnt.coords()))
            normal = Vector(lines[0].cross(lines[1]))
            if(normal.dot(Vertex([0, 0, -1])) < 0):
                for i, point in enumerate(points):
                    points[i] = np.matmul(point.coords(1), projMat)
                    points[i] = Vertex(array=points[i][:3]/points[i][3])
                    points[i].x += 1
                    points[i].y += 1
                    points[i].x *= 0.5*WIDTH
                    points[i].y *= 0.5*HEIGHT
                Lz = (int(abs(normal.z()*-1.0)*255),
                      0,
                      int(abs(normal.z()*-1.0)*255))
                color = '#%02x%02x%02x' % Lz
                canvas.create_polygon([[point.x, point.y]
                                       for point in points], fill=color)
                canvas.create_line([[point.x, point.y]
                                    for point in points], fill="#FFFFFF")


polygons = Cube(side=25)
# print(polygons.faces)
# polygons.load(askopenfilename(initialdir="/"))
t = Thread(target=draw, args=(polygons,))
t.start()


def on_exit():
    global need_run
    need_run = False
    exit()


window.protocol("WM_DELETE_WINDOW", on_exit)
# draw(Cube())
# update()
mainloop()
