from arcade import key
from random import randint
import math

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Ship(Model):

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def animate(self, delta):
        if self.y > self.world.height:
            self.y = 0
        if self.x > self.world.width :
            self. x = 0

    def move(self, up, down, left, right):
        if up:
            self.y += 2
        if down:
            self.y -= 2
        if left:
            self.x -= 2
        if right:
            self.x += 2

    def turn(self, up, down, left, right):
        if up :
            if left :
                self.angle = 45
            elif right :
                self.angle = -45
            else :
                self.angle = 0
        elif down :
            if left :
                self.angle = 135
            elif right :
                self.angle = 225
            else :
                self.angle = 180
        elif left :
            self.angle = 90
        elif right :
            self.angle = -90

class Planet(Model) :
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.planet = Planet(self, 200, 300)
        self.ship = Ship(self, 100, 100)

        self.score = 0

        self.key_list = []

    def animate(self, delta):
        self.update()
        self.ship.animate(delta)

    def update(self):
        up = key.W in self.key_list
        down = key.S in self.key_list
        left = key.A in self.key_list
        right = key.D in self.key_list
        self.ship.move(up, down, left, right)
        self.ship.turn(up, down, left, right)

    def on_key_press(self, key, key_modifiers):
        self.key_list.append(key)

    def on_key_release(self, key, key_modifiers):
        self.key_list.remove(key)
