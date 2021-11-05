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
rotMatY = np.zeros(9).reshape((3, 3))
rotMatZ[2][2] = 1
rotMatX[0][0] = 1
rotMatY[1][1] = 1


def rotateZ(point, elapsed):
    rotMatZ[0][0] = np.cos(elapsed)
    rotMatZ[0][1] = np.sin(elapsed)
    rotMatZ[1][0] = -np.sin(elapsed)
    rotMatZ[1][1] = np.cos(elapsed)
    dot1 = np.matmul(point, rotMatZ)
    return(dot1)


def rotateY(point, elapsed):
    rotMatY[0][0] = np.cos(elapsed)
    rotMatY[0][2] = np.sin(elapsed)
    rotMatY[2][0] = -np.sin(elapsed)
    rotMatY[2][2] = np.cos(elapsed)
    dot1 = np.matmul(point, rotMatY)
    return(dot1)


def rotateX(point, elapsed):
    rotMatX[1][1] = np.cos(elapsed)
    rotMatX[1][2] = np.sin(elapsed)
    rotMatX[2][1] = -np.sin(elapsed)
    rotMatX[2][2] = np.cos(elapsed)

    dot1 = np.matmul(point, rotMatX)
    return(dot1)


def sorter(faces, points_arrs):
    faces = copy.deepcopy(faces)
    faces.sort(reverse=True, key=lambda pnts:
               sum([(points_arrs[indx])[2] for indx in pnts])/len(pnts))
    return(faces)


def draw(mesh):
    print("drawing")
    sttime = time.time()
    secRun = 0.0
    fps = 1/10.0
    #points_arr = copy.deepcopy(mesh.vertices)

    for i, point in enumerate(mesh.vertices):

        rotatedPZ = rotateZ(point, np.pi)
        #rotatedPX = rotateX(rotatedPZ, increment)
        mesh.vertices[i] = rotatedPZ
        pass
    while(time.time()-sttime < 10):
        secRun += fps
        elapsed = time.time()-sttime
        if(elapsed < fps):
            time.sleep(fps-elapsed)
            sttime = time.time()
        canvas.delete("all")
        increment = (secRun)
        tempoints = copy.deepcopy(mesh.vertices)
        faces = sorter(mesh.faces, tempoints)

        for i, point in enumerate(tempoints):
            rotatedPY = rotateY(point, np.pi+np.pi/2)
            tempoints[i] = rotatedPY
            tempoints[i][2] += 4

        for verticArr in faces:
            pnt1 = tempoints[verticArr[0]]
            pnt2 = tempoints[verticArr[1]]
            pnt3 = tempoints[verticArr[2]]
            line1 = [pnt2[0]-pnt1[0], pnt2[1]-pnt1[1], pnt2[2]-pnt1[2]]
            line2 = [pnt3[0]-pnt2[0], pnt3[1]-pnt2[1], pnt3[2]-pnt2[2]]
            cP = cross(line1, line2)
            normal = normalize(cP)
            nmlDot = dot(normal, pnt3)
            # print(normal.dot(Vertex([0,0,-1])))
            points = [np.append(p, [1])
                      for p in [tempoints[o] for o in verticArr]]

            # print("points",points)
            if(nmlDot < 0):
                for i, point in enumerate(points):
                    # print(points[i])
                    points[i] = np.matmul(points[i], projMat)
                    points[i] = points[i][:3]/points[i][3]
                    points[i][0] += 1.0
                    points[i][1] += 1.0
                    points[i][0] *= 0.5*WIDTH
                    points[i][1] *= 0.5*HEIGHT
                calcol = int(abs(normal[2]*-1.0)*255)
                calcol = 255 if calcol > 255 else calcol
                Lz = (calcol,
                      0,
                      calcol)
                color = '#%02x%02x%02x' % Lz
                canvas.create_polygon([[point[0], point[1]]
                                      for point in points], fill=color)
                # canvas.create_line([[point[0], point[1]]
                #                    for point in points], fill="#FFFFFF")


polygons = Cube(side=2.0)
# print(polygons.faces)
polygons.load(askopenfilename(initialdir="/"))
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
