import tkinter as tk
import math
import random
import json

def color_name_to_rgb(color_name):
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "gray": (128, 128, 128),
        "darkgray": (169, 169, 169),
        "lightblue": (173, 216, 230),
        "silver": (192, 192, 192),
        "lightgray": (211, 211, 211)
    }
    return colors.get(color_name, (255, 255, 255))
def density_to_color(density, color):
        base_color = color_name_to_rgb(color)
        brightness = 255 - int(density)
        brightness = max(0, min(brightness, 255))
        return f'#{brightness & 255:02x}{base_color[1]:02x}{base_color[2]:02x}'

def create_star(n=100):
    random.seed(0)
    for _ in range(n):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        brightness = random.randint(200, 255)
        color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
        canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=color)

def update_positions():

    canvas.delete("all")
    create_star()


    canvas.create_oval(sun_position[0] - 50, sun_position[1] - 50,
                       sun_position[0] + 50, sun_position[1] + 50,
                       fill='yellow')


    for i, planet in enumerate(planet_data):
        planet_angle, satellite_angles = angles[i]


        planet_x = sun_position[0] + planet["distance"] * math.cos(planet_angle)
        planet_y = sun_position[1] + planet["distance"] * math.sin(planet_angle)


        canvas.create_oval(planet_x - int(planet["radius"]), planet_y - int(planet["radius"]),
                           planet_x + int(planet["radius"]), planet_y + int(planet["radius"]),
                           fill=density_to_color(planet["density"], planet["color"]))

        angles[i] = (planet_angle + planet["speed"], satellite_angles)

        for j, satellite in enumerate(planet["satellites"]):
            satellite_angle = satellite_angles[j]


            satellite_x = planet_x + satellite["distance"] * math.cos(satellite_angle)
            satellite_y = planet_y + satellite["distance"] * math.sin(satellite_angle)


            canvas.create_oval(satellite_x - int(satellite["radius"]), satellite_y - int(satellite["radius"]),
                               satellite_x + int(satellite["radius"]), satellite_y + int(satellite["radius"]),
                               fill=density_to_color(satellite["density"], satellite["color"]))


            satellite_angles[j] += satellite["speed"]

        angles[i] = (angles[i][0], satellite_angles)

    canvas.after(10, update_positions)

sun_position = (250, 250)
planet_data = json.load(open('practic2.json'))['planets']

angles = [(0, [0] * len(planet["satellites"])) for planet in planet_data]

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500, bg='black')
canvas.pack()

update_positions()

root.mainloop()
