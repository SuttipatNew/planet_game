from arcade import key
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

class Bar:
    def __init__(self, world, x, y, max_size, width) :
        self.x = x
        self.y = y
        self.max_size = max_size
        self.width = width
        self.items = []

    def add_item(self) :
        if len(self.items) >= self.max_size :
            return
        if len(self.items) == 0 :
            self.items.append(Item(self, self.x - self.max_size / 2 * self.width, self.y))
            return
        self.items.append(Item(self, self.items[len(self.items) - 1].x + self.width, self.y))

class Item:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y

class Ship(Model):

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 90)
        self.ammo_num = 10

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

class WaterBar(Bar) :
    width = 4
    height = 16
    def __init__(self, world, x, y, max_size) :
        super().__init__(world, x, y, max_size, WaterBar.width)

class HealthBar(Bar) :
    width = 4
    height = 4
    def __init__(self, world, x, y, max_size, ship) :
        super().__init__(world, x, y, max_size, HealthBar.width)
        self.ship = ship

    def animate(self, delta) :
        self.x = self.ship.x
        self.y = self.ship.y + 80
        for i in range(len(self.items)) :
            if i == 0 :
                self.items[i].x = self.x - self.max_size / 2 * self.width
            else :
                self.items[i].x = self.items[i - 1].x + self.width
            self.items[i].y = self.y

class Meteorite(Model) :
    def __init__(self, world, x, y):
        diff_x = world.planet.x - x
        diff_y = world.planet.y - y
        rad = math.atan(float(diff_y) / diff_x)
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

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.planet = Planet(self, 400, 300)
        self.ship = Ship(self, 100, 100)
        self.water_bar = WaterBar(self, self.planet.x,self.planet.y + 100, 40)
        self.health_bar = HealthBar(self, self.ship.x, self.ship.y + 80, 20, self.ship)
        for i in range(self.health_bar.max_size) :
            self.health_bar.add_item()

        self.score = 0

        self.meteorites = []
        self.key_list = []
        self.bullets = []
        self.ammos = []

        self.water_bar_update_counter = time()

    def animate(self, delta):
        self.update()
        self.ship.animate(delta)
        self.bullets_animate(delta)
        self.meteorites_animate(delta)
        self.health_bar.animate(delta)

    def update(self):
        up = key.W in self.key_list
        down = key.S in self.key_list
        left = key.A in self.key_list
        right = key.D in self.key_list
        self.ship.move(up, down)
        self.ship.turn(left, right)

        self.update_ship_fire()

        self.update_meteorites()


    def on_key_press(self, key, key_modifiers):
        self.key_list.append(key)

    def on_key_release(self, key, key_modifiers):
        try:
            self.key_list.remove(key)
        except:
            pass

    def update_ship_fire(self) :
        if key.SPACE in self.key_list and self.ship.ammo_num > 0:
            self.create_bullet()
            self.ship.ammo_num -= 1
            try:
                self.key_list.remove(key.SPACE)
            except:
                pass

    def update_meteorites(self) :
        if(len(self.meteorites) < 5) :
            if random_prob(0.01) :
                rand_num = randint(0,3)
                on_right = rand_num == 0
                on_top = rand_num == 1
                on_left = rand_num == 2
                x = 0; y = 0
                if on_right or on_left:
                    y = randint(0, self.height - 1)
                    if on_right :
                        x = self.width + 50
                    else :
                        x = 0
                else :
                    x = randint(0, self.width)
                    if on_top :
                        y = self.height
                    else :
                        y = 0
                self.meteorites.append(Meteorite(self, x, y))

    def create_bullet(self):
        self.bullets.append(Bullet(self, self.ship.x, self.ship.y, self.ship.angle))

    def bullets_animate(self, delta) :
        for bullet in self.bullets :
            bullet.animate(delta)
            if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height :
                self.bullets.remove(bullet)

    def meteorites_animate(self, delta) :
        for meteorite in self.meteorites :
            meteorite.animate(delta)
            if meteorite.x < 0 or meteorite.x > self.width or meteorite.y < 0 or meteorite.y > self.height :
                self.meteorites.remove(meteorite)

    def ship_on_planet(self) :
        if time() - self.water_bar_update_counter >= 1 :
            self.water_bar_update_counter = time()
            self.water_bar.add_item()

    def create_ammo(self, x, y) :
        self.ammos.append(Ammo(self, x, y))


def random_prob(prob) :
    return random() <= prob
