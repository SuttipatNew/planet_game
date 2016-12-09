from arcade import key
import arcade
from random import randint
from random import random
from time import time
import math

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle

class Ship(Model):

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 90)
        self.ammo_num = 10
        self.full_health = 10
        self.health = self.full_health

    def animate(self, delta):
        if self.y > self.world.height:
            self.y = 0
        if self.x > self.world.width :
            self. x = 0

    def move(self, up, down):
        if up :
            self.x += math.cos(math.radians(self.angle)) * 2
            self.y += math.sin(math.radians(self.angle)) * 2
        if down :
            self.x -= math.cos(math.radians(self.angle)) * 2
            self.y -= math.sin(math.radians(self.angle)) * 2

    def turn(self, left, right):
        if left :
            self.angle += 2
        if right :
            self.angle -= 2

class Planet(Model) :
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

class Bullet(Model) :
    def __init__(self, world, x, y, angle):
        super().__init__(world, x, y, angle)

    def animate(self, delta) :
        self.x += math.cos(math.radians(self.angle)) * 4
        self.y += math.sin(math.radians(self.angle)) * 4

class Meteorite(Model) :
    def __init__(self, world, x, y):
        diff_x = world.planet.x - x
        diff_y = world.planet.y - y
        rad = None
        if diff_x != 0 :
            rad = math.atan(float(diff_y) / diff_x)
        else :
            rad = math.pi / 2
        angle = math.degrees(rad)
        if(x > world.planet.x) :
            angle += 180
        super().__init__(world, x, y, angle)
        self.velocity = 0.5

    def animate(self, delta):
        self.x += math.cos(math.radians(self.angle)) * self.velocity
        self.y += math.sin(math.radians(self.angle)) * self.velocity

class Ammo(Model) :
    def __init__(self, world, x, y) :
        super().__init__(world, x, y, 0)
        self.size = 5

class Listenner :
    def __init__(self) :
        self.__handlers = []

    def add(self, handler) :
        self.__handlers.append(handler)

    def notify(self, *args, **keywargs) :
        for handler in self.__handlers :
            handler(*args, **keywargs)

def random_prob(prob) :
    return random() <= prob
