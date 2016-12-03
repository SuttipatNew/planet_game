from arcade import key
from random import randint
from random import random
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
        super().__init__(world, x, y, 90)

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

class WaterBar(Model) :
    width = 4
    height = 16
    max_bars = 40
    def __init__(self, world, x, y) :
        super().__init__(world, x, y, 0)

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

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.planet = Planet(self, 400, 300)
        self.ship = Ship(self, 100, 100)

        self.score = 0

        self.meteorites = []
        self.water_bars = []
        self.key_list = []
        self.bullets = []

    def animate(self, delta):
        self.update()
        self.ship.animate(delta)
        self.bullets_animate(delta)
        self.meteorites_animate(delta)

    def update(self):
        up = key.W in self.key_list
        down = key.S in self.key_list
        left = key.A in self.key_list
        right = key.D in self.key_list
        self.ship.move(up, down)
        self.ship.turn(left, right)

        self.update_ship_fire()

        self.update_meteorites()

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

    def update_ship_fire(self) :
        if(key.SPACE in self.key_list):
            self.create_bullet()
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

    def increaseBar(self):
        if len(self.water_bars) >= WaterBar.max_bars :
            return
        if len(self.water_bars) == 0 :
            self.water_bars.append(WaterBar(self, self.planet.x - WaterBar.max_bars / 2 * WaterBar.width, self.planet.y + 100))
            return
        self.water_bars.append(WaterBar(self, self.water_bars[len(self.water_bars) - 1].x + WaterBar.width, self.planet.y + 100))

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

def random_prob(prob) :
    return random() <= prob
