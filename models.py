import arcade.key
from random import randint

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Ship(Model):
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.direction = Ship.DIR_VERTICAL

    def switch_direction(self):
        if self.direction == Ship.DIR_HORIZONTAL:
            self.direction = Ship.DIR_VERTICAL
            self.angle = 0
        else:
            self.direction = Ship.DIR_HORIZONTAL
            self.angle = -90

    def forward(self):
        self.x += 2

    def animate(self, delta):
        if self.direction == Ship.DIR_VERTICAL :
            if self.y > self.world.height:
                self.y = 0
            # self.y += 5
        else :
            if self.x > self.world.width :
                self.x = 0
            # self.x += 5

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
        if arcade.key.W in self.key_list:
            self.ship.forward()

    def on_key_press(self, key, key_modifiers):
        self.key_list.append(key)

    def on_key_release(self, key, key_modifiers):
        self.key_list.remove(key)
