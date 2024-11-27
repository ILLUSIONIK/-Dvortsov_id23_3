import sys
import math
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QPushButton, QLabel
from PyQt5.QtCore import QTimer, QRectF, Qt
from PyQt5.QtGui import QPainter, QColor

def density_to_color(density, color_string):
    base_color = QColor(color_string)
    try:
        density = float(density)
    except ValueError:
        density = 0
    factor = min(max(density / 255, 0), 1)
    r = int(base_color.red() * factor)
    g = int(base_color.green() * factor)
    b = int(base_color.blue() * factor)
    return QColor(r, g, b)

def create_star(n=100):
    random.seed(0)
    stars = []
    for _ in range(n):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        brightness = random.randint(200, 255)
        color = QColor(brightness, brightness, brightness)
        stars.append((x, y, color))
    return stars

def grow_on_collision(obj_radius, obj_density, asteroid_size, increment_factor=0.1):
    increment = asteroid_size * increment_factor
    obj_radius += increment
    obj_density = min(obj_density + increment, 255)
    return obj_radius, obj_density

class Asteroid:
    def __init__(self, x, y, size=2, speed=1):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.direction_x = 1
        self.direction_y = 1
        self.to_remove = False

    def move(self, width, height, sun, planets, gravity_constant=0.1):
        sun_x, sun_y, sun_mass = sun
        ax, ay = self.calculate_gravity_acceleration(sun_x, sun_y, sun_mass, gravity_constant)

        for planet in planets:
            planet_x, planet_y, planet_mass = planet
            px, py = self.calculate_gravity_acceleration(planet_x, planet_y, planet_mass, gravity_constant)
            ax += px
            ay += py

        self.direction_x += ax
        self.direction_y += ay

        norm = math.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        self.direction_x /= norm
        self.direction_y /= norm

        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        if self.x >= width - self.size or self.x <= 0 or self.y >= height - self.size or self.y <= 0:
            self.to_remove = True

    def calculate_gravity_acceleration(self, obj_x, obj_y, obj_mass, gravity_constant):
        distance_x = obj_x - self.x
        distance_y = obj_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = gravity_constant * obj_mass / (distance ** 2)
        ax = force * (distance_x / distance)
        ay = force * (distance_y / distance)

        return ax, ay

class SolarSystem(QMainWindow):
    def __init__(self, planet_data):
        super().__init__()
        self.setWindowTitle("Solar System Simulation")
        self.setGeometry(100, 100, 500, 500)

        self.is_paused = False

        self.sun_position = (250, 250)
        self.sun_radius = 50
        self.sun_density = 100
        self.planet_data = planet_data
        self.angles = [(0, [0] * len(planet.get("satellites", []))) for planet in planet_data]
        self.stars = create_star()
        self.points = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_positions)

        self.pause_button = QPushButton("Pause", self)
        self.start_pos = None
        self.current_pos = None
        self.pause_button.setGeometry(10, 10, 80, 30)
        self.pause_button.clicked.connect(self.toggle_pause)


        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.setGeometry(410, 380, 80, 20)

        self.speed_label = QLabel("Speed: 5", self)
        self.speed_label.setStyleSheet("color: white")
        self.speed_label.setGeometry(410, 350, 80, 20)
        self.speed_slider.valueChanged.connect(self.update_speed_label)

        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setMinimum(5)
        self.size_slider.setMaximum(100)
        self.size_slider.setValue(10)
        self.size_slider.setGeometry(410, 450, 80, 20)

        self.size_label = QLabel("Size: 10", self)
        self.size_label.setStyleSheet("color: white")
        self.size_label.setGeometry(410, 420, 80, 20)
        self.size_slider.valueChanged.connect(self.update_size_label)

        self.timer.start(10)

    def update_speed_label(self, value):
        self.speed_label.setText(f"Speed: {value}")

    def update_size_label(self, value):
        self.size_label.setText(f"Size: {value}")

    def toggle_pause(self):
        if self.is_paused:
            self.timer.start(10)
            self.pause_button.setText("Pause")
        else:
            self.timer.stop()
            self.pause_button.setText("Play")
        self.is_paused = not self.is_paused

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_scene(QPainter(self))

    def draw_scene(self, painter):
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.rect())

        for x, y, color in self.stars:
            painter.setBrush(color)
            painter.drawEllipse(x - 1, y - 1, 2, 2)

        painter.setBrush(QColor('yellow'))
        sun_x, sun_y = self.sun_position
        painter.drawEllipse(QRectF(sun_x - self.sun_radius, sun_y - self.sun_radius,
                                   2 * self.sun_radius, 2 * self.sun_radius))

        for i, planet in enumerate(self.planet_data):
            planet_angle, satellite_angles = self.angles[i]
            planet_x = sun_x + planet["distance"] * math.cos(planet_angle)
            planet_y = sun_y + planet["distance"] * math.sin(planet_angle)

            color = density_to_color(planet["density"], planet["color"])
            painter.setBrush(color)
            painter.drawEllipse(QRectF(planet_x - int(planet["radius"]),
                                       planet_y - int(planet["radius"]),
                                       2 * int(planet["radius"]), 2 * int(planet["radius"])))

            if not self.is_paused:
                self.angles[i] = (planet_angle + planet["speed"], satellite_angles)

            for j, satellite in enumerate(planet.get("satellites", [])):
                satellite_angle = satellite_angles[j]
                satellite_x = planet_x + satellite["distance"] * math.cos(satellite_angle)
                satellite_y = planet_y + satellite["distance"] * math.sin(satellite_angle)

                color = density_to_color(satellite["density"], satellite["color"])
                painter.setBrush(color)
                painter.drawEllipse(
                    QRectF(satellite_x - int(satellite["radius"]),
                           satellite_y - int(satellite["radius"]),
                           2 * int(satellite["radius"]), 2 * int(satellite["radius"])))

                if not self.is_paused:
                    satellite_angles[j] += satellite["speed"]

            self.angles[i] = (self.angles[i][0], satellite_angles)

        for asteroid in self.points:
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(QRectF(asteroid.x - asteroid.size / 2,
                                       asteroid.y - asteroid.size / 2,
                                       asteroid.size, asteroid.size))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            size = self.size_slider.value()
            speed = self.speed_slider.value()
            self.start_pos = event.pos()
            self.points.append(Asteroid(event.x(), event.y(), size, speed))

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            self.current_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_pos and self.current_pos:
            dx = self.current_pos.x() - self.start_pos.x()
            dy = self.current_pos.y() - self.start_pos.y()

            if len(self.points) > 0:
                last_asteroid = self.points[-1]
                norm = math.sqrt(dx ** 2 + dy ** 2)
                last_asteroid.direction_x = dx / norm
                last_asteroid.direction_y = dy / norm

            self.start_pos = None
            self.current_pos = None

    def update_positions(self):
        if self.is_paused:
            return

        removal_list = []

        sun_data = (self.sun_position[0], self.sun_position[1], self.sun_density)
        planets_data = []
        for i, planet in enumerate(self.planet_data):
            planet_x = self.sun_position[0] + planet["distance"] * math.cos(self.angles[i][0])
            planet_y = self.sun_position[1] + planet["distance"] * math.sin(self.angles[i][0])
            planets_data.append((planet_x, planet_y, planet["density"]))

        for asteroid in self.points[:]:
            asteroid.move(self.width(), self.height(), sun_data, planets_data)
            if asteroid.to_remove:
                removal_list.append(asteroid)
            if self.check_collision(asteroid, self.sun_position, self.sun_radius):
                self.sun_radius, self.sun_density = grow_on_collision(self.sun_radius,
                                                                      self.sun_density,
                                                                      asteroid.size)
                removal_list.append(asteroid)

            for i, planet in enumerate(self.planet_data):
                planet_x = self.sun_position[0] + planet["distance"] * math.cos(self.angles[i][0])
                planet_y = self.sun_position[1] + planet["distance"] * math.sin(self.angles[i][0])
                planet_radius = planet["radius"]
                if self.check_collision(asteroid, (planet_x, planet_y), planet_radius):
                    self.planet_data[i]["radius"], self.planet_data[i]["density"] = \
                        grow_on_collision(planet_radius, planet["density"], asteroid.size)
                    for satellite in planet.get("satellites", []):
                        satellite["distance"] += 1
                    removal_list.append(asteroid)
                    break

        for asteroid in removal_list:
            self.points.remove(asteroid)
        self.repaint()

    def check_collision(self, asteroid, obj_position, obj_radius):
        obj_x, obj_y = obj_position
        distance = ((asteroid.x - obj_x) ** 2 + (asteroid.y - obj_y) ** 2) ** 0.5
        return distance <= obj_radius

def main():
    app = QApplication(sys.argv)

    planet_data = json.load(open('../../practic2.json'))['planets']

    window = SolarSystem(planet_data)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
