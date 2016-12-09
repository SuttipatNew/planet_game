from models import *

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.full_meteorites = 5
        self.prob_meteorites = 0.01

        self.water = 0
        self.full_water = 10

        self.planet = Planet(self, 400, 300)
        self.ship = Ship(self, 100, 100)

        self.score = 0

        self.meteorites = []
        self.key_list = []
        self.bullets = []
        self.ammos = []

        self.water_bar_update_counter = time()

        self.bullet_listenner = Listenner()
        self.meteorite_listenner = Listenner()
        self.gameover_listenner = Listenner()
        self.water_bar_full_listenner = Listenner()

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

        self.update_planet()

        self.check_gameover()


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
        if(len(self.meteorites) < self.full_meteorites) :
            if random_prob(self.prob_meteorites) :
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
                new_item = Meteorite(self, x, y)
                self.meteorites.append(new_item)
                self.meteorite_listenner.notify('new', new_item)

    def create_bullet(self):
        new_item = Bullet(self, self.ship.x, self.ship.y, self.ship.angle)
        self.bullets.append(new_item)
        self.bullet_listenner.notify('new', new_item)

    def bullets_animate(self, delta) :
        for bullet in self.bullets :
            bullet.animate(delta)
            if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height :
                self.bullet_listenner.notify('remove', bullet)
                self.bullets.remove(bullet)
                del bullet

    def meteorites_animate(self, delta) :
        for meteorite in self.meteorites :
            meteorite.animate(delta)
            if meteorite.x < 0 or meteorite.x > self.width or meteorite.y < 0 or meteorite.y > self.height :
                self.meteorite_listenner.notify('remove', meteorite)
                self.meteorites.remove(meteorite)
                del meteorite
            elif math.fabs(meteorite.x - self.planet.x) < 40 and math.fabs(meteorite.y - self.planet.y) < 40 :
                self.gameover_listenner.notify()

    def ship_on_planet(self) :
        if time() - self.water_bar_update_counter >= 1 :
            self.water_bar_update_counter = time()
            if self.water < self.full_water :
                self.water += 1

    def create_ammo(self, x, y) :
        self.ammos.append(Ammo(self, x, y))

    def check_gameover(self) :
        if self.ship.health <= 0 :
            self.gameover_listenner.notify()

    def update_planet(self) :
        if self.water == self.full_water :
            self.score += 100
            self.water = 0
            self.full_water += 10
            if self.ship.full_health < 40 :
                self.ship.full_health += 2
            self.ship.health = self.ship.full_health
            self.ship.ammo_num += 10
            self.water_bar_full_listenner.notify()
            self.full_meteorites += 2
            self.prob_meteorites += 0.01
