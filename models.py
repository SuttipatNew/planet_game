from arcade import key
from random import randint
import math

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle

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

    def move(self, up, down):
        if up :
            self.x -= math.sin(math.radians(self.angle)) * 2
            self.y += math.cos(math.radians(self.angle)) * 2
        if down :
            self.x += math.sin(math.radians(self.angle)) * 2
            self.y -= math.cos(math.radians(self.angle)) * 2

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
        self.x -= math.sin(math.radians(self.angle)) * 4
        self.y += math.cos(math.radians(self.angle)) * 4

class WaterBar(Model) :
    width = 4
    height = 16
    def __init__(self, world, x, y) :
        super().__init__(world, x, y, 0)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.planet = Planet(self, 200, 300)
        self.ship = Ship(self, 100, 100)

        self.score = 0

        self.water_bars = []
        self.key_list = []
        self.bullets = []

    def animate(self, delta):
        self.update()
        self.ship.animate(delta)
        for bullet in self.bullets :
            bullet.animate(delta)
            if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height :
                self.bullets.remove(bullet)

    def update(self):
        up = key.W in self.key_list
        down = key.S in self.key_list
        left = key.A in self.key_list
        right = key.D in self.key_list
        self.ship.move(up, down)
        self.ship.turn(left, right)

        if(key.SPACE in self.key_list):
            self.createBullet()
            try:
                self.key_list.remove(key.SPACE)
            except:
                pass

        if(key.M in self.key_list):
            self.increaseBar()
            try:
                self.key_list.remove(key.M)
            except:
                pass


    def on_key_press(self, key, key_modifiers):
        self.key_list.append(key)

    def on_key_release(self, key, key_modifiers):
        try:
            self.key_list.remove(key)
        except:
            pass

    def createBullet(self):
        self.bullets.append(Bullet(self, self.ship.x, self.ship.y, self.ship.angle))

    def increaseBar(self):
        if len(self.water_bars) == 0 :
            self.water_bars.append(WaterBar(self, 200, 500))
            return
        self.water_bars.append(WaterBar(self, self.water_bars[len(self.water_bars) - 1].x + WaterBar.width, 500))
