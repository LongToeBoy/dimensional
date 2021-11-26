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
world = World(aspectRatio, fFov, fFar, fNear)


def draw(mesh):
    print("drawing")
    sttime = time.time()
    secRun = 0.0
    fps = 1/10.0
    #points_arr = copy.deepcopy(mesh.vertices)

    mesh.rotateZ(np.pi)
        
    while(time.time()-sttime < 2):
        secRun += fps
        elapsed = time.time()-sttime
        if(elapsed < fps):
            time.sleep(fps-elapsed)
            sttime = time.time()
        canvas.delete("all")
        increment = (secRun)
        tempoints = copy.deepcopy(mesh)
        faces = mesh.sorter(mesh.faces, tempoints.vertices)

        tempoints.rotateY(np.pi)
        tempoints.push([0,0,3])

        for verticArr in faces:
            pnt1 = tempoints.vertices[verticArr[0]]
            pnt2 = tempoints.vertices[verticArr[1]]
            pnt3 = tempoints.vertices[verticArr[2]]
            line1 = [pnt2[0]-pnt1[0], pnt2[1]-pnt1[1], pnt2[2]-pnt1[2]]
            line2 = [pnt3[0]-pnt2[0], pnt3[1]-pnt2[1], pnt3[2]-pnt2[2]]
            cP = cross(line1, line2)
            normal = normalize(cP)
            nmlDot = dot(normal, pnt3)
            # print(normal.dot(Vertex([0,0,-1])))
            points = [np.append(p, [1])
                      for p in [tempoints.vertices[o] for o in verticArr]]

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
#polygons.load(askopenfilename(initialdir="/"))
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
