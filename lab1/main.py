import time
from tkinter import *
from math import *

def move_point(speed = 0.05, direction = 1):
    a = 0
    while a < 360:
        root.update()
        x = cos(radians(a)) * 200 * pi / 180 * direction
        y = sin(radians(a)) * 200 * pi / 180
        a += 1
        canvas.move(point, x, y)
        time.sleep(speed)

root = Tk()
canvas = Canvas(root, width=600, height=600)
canvas.pack()
radius = 200

canvas_middle = [int(canvas['width'])/2, int(canvas['height'])/2]
canvas.create_oval(canvas_middle[0] - radius, canvas_middle[1] - radius,
                   canvas_middle[0] + radius, canvas_middle[1] + radius)

radius_point = 10
point = canvas.create_oval(300 - radius_point , 100 - radius_point,
                           300 + radius_point, 100 + radius_point, fill = "pink") #x0, y0, x1, y1


while True:
    move_point(0.05, -1)

