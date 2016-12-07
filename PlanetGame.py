import arcade
from models import World, Ship, random_prob

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()

class BarSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            # self.angle = 0

    def draw(self):
        self.sync_with_model()
        super().draw()

class PlanetGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.background = arcade.Sprite('images/background_star.png')
        self.background.set_position(width/2, height/2)

        self.world = World(width, height)

        self.ship_sprite = ModelSprite('images/ship.png', model=self.world.ship)
        self.planet_sprite = ModelSprite('images/planet3-1.png', model=self.world.planet)
        self.bullet_sprites = []
        self.water_bar_sprites = []
        self.health_bar_sprites = []
        self.meteorite_sprites = []
        self.ammo_sprites = []

        self.present_score = self.world.score
        self.present_ammo_num = self.world.ship.ammo_num

        self.world.bullet_listenner.add(self.bullet_listenner_nofify)
        self.world.meteorite_listenner.add(self.meteorite_listenner_notify)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.planet_sprite.draw()
        for bullet_sprite in self.bullet_sprites:
            bullet_sprite.draw()

        for ammo_sprite in self.ammo_sprites :
            ammo_sprite.draw()

        self.ship_sprite.draw()

        for meteorite_sprite in self.meteorite_sprites:
            meteorite_sprite.draw()

        for water_bar_sprite in self.water_bar_sprites:
            water_bar_sprite.draw()

        for health_bar_sprite in self.health_bar_sprites :
            health_bar_sprite.draw()


        arcade.draw_text("SCORE: " + str(self.present_score), self.width - 120, self.height - 30, arcade.color.WHITE, 16)
        arcade.draw_text("AMMO: " + str(self.present_ammo_num), self.width - 120, 20, arcade.color.WHITE, 16)

    def animate(self, delta):
        self.world.animate(delta)
        self.update_water_bar()
        self.update_health_bar()
        self.remove_bullet_and_meteorite()
        self.ship_on_planet()
        self.create_sprite_for_new_ammo()
        self.ship_pick_ammo()
        self.meteorite_hit_ship()
        self.remove_unuse_health_bar()
        self.update_ui()
        self.update_planet()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def update_water_bar(self) :
        if(len(self.world.water_bar.items) > 0) :
            for water_bar in self.world.water_bar.items :
                sprite_exists = False
                for water_bar_sprite in self.water_bar_sprites :
                    if water_bar == water_bar_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.water_bar_sprites.append(BarSprite('images/rect-blue.png', model=water_bar))

    def remove_bullet_and_meteorite(self) :
        for bullet_sprite in self.bullet_sprites :
            for meteorite_sprite in self.meteorite_sprites :
                if arcade.check_for_collision(bullet_sprite, meteorite_sprite) :
                    if random_prob(0.5) :
                        self.world.create_ammo(meteorite_sprite.model.x, meteorite_sprite.model.y)
                    self.world.score += 1
                    try:
                        self.world.bullets.remove(bullet_sprite.model)
                        self.bullet_sprites.remove(bullet_sprite)
                        self.world.meteorites.remove(meteorite_sprite.model)
                        self.meteorite_sprites.remove(meteorite_sprite)
                        del bullet_sprite.model
                        del bullet_sprite
                        del meteorite_sprite.model
                        del meteorite_sprite
                    except:
                        pass
                    return

    def ship_on_planet(self) :
        if arcade.check_for_collision(self.ship_sprite, self.planet_sprite) :
            self.world.ship_on_planet()

    def create_sprite_for_new_ammo(self) :
        if(len(self.world.ammos) > 0) :
            for ammo in self.world.ammos :
                sprite_exists = False
                for ammo_sprite in self.ammo_sprites :
                    if ammo == ammo_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.ammo_sprites.append(ModelSprite('images/ammo.png', model=ammo))

    def ship_pick_ammo(self) :
        for ammo_sprite in self.ammo_sprites :
            if arcade.check_for_collision(ammo_sprite, self.ship_sprite) :
                self.world.ship.ammo_num += ammo_sprite.model.size
                try:
                    self.world.ammos.remove(ammo_sprite.model)
                    self.ammo_sprites.remove(ammo_sprite)
                    del ammo_sprite.model
                    del ammo_sprite
                except:
                    pass
                return

    def update_health_bar(self) :
        if(len(self.world.health_bar.items) > 0) :
            for health_bar in self.world.health_bar.items :
                sprite_exists = False
                for health_bar_sprite in self.health_bar_sprites :
                    if health_bar == health_bar_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.health_bar_sprites.append(BarSprite('images/rect-red.png', model=health_bar))

    def meteorite_hit_ship(self) :
        for meteorite_sprite in self.meteorite_sprites :
            if arcade.check_for_collision(meteorite_sprite, self.ship_sprite) :
                try:
                    self.world.health_bar.items.pop()
                    self.world.health_bar.items.pop()
                except:
                    print('ship destroyed')
                try:
                    self.world.meteorites.remove(meteorite_sprite.model)
                    self.meteorite_sprites.remove(meteorite_sprite)
                    del meteorite_sprite.model
                    del meteorite_sprite
                except:
                    pass
                return

    def remove_unuse_health_bar(self) :
        for health_bar_sprite in self.health_bar_sprites :
            if health_bar_sprite.model not in self.world.health_bar.items:
                self.health_bar_sprites.remove(health_bar_sprite)
                del health_bar_sprite

    def update_ui(self) :
        if self.present_score < self.world.score :
            self.present_score += 1
        if self.present_ammo_num < self.world.ship.ammo_num :
            self.present_ammo_num += 1
        if self.present_ammo_num > self.world.ship.ammo_num :
            self.present_ammo_num -= 1

    def bullet_listenner_nofify(self, message, bullet) :
        if message == 'remove':
            for bullet_sprite in self.bullet_sprites :
                if bullet_sprite.model == bullet :
                    self.bullet_sprites.remove(bullet_sprite)
                    del bullet_sprite
        elif message == 'new':
            self.bullet_sprites.append(ModelSprite('images/bullet.png', model=bullet))


    def meteorite_listenner_notify(self, message, meteorite) :
        if message == 'remove':
            for meteorite_sprite in self.meteorite_sprites :
                if meteorite_sprite.model == meteorite :
                    self.meteorite_sprites.remove(meteorite_sprite)
                    del meteorite_sprite
        elif message == 'new' :
            self.meteorite_sprites.append(ModelSprite('images/meteorite.png', model=meteorite))

    def update_planet(self) :
        level = len(self.world.water_bar.items) / self.world.water_bar.max_size * 100
        if level < 20 :
            self.planet_sprite = ModelSprite('images/planet3-1.png', model=self.world.planet)
        elif level < 40 :
            self.planet_sprite = ModelSprite('images/planet3-2.png', model=self.world.planet)
        elif level < 60 :
            self.planet_sprite = ModelSprite('images/planet3-3.png', model=self.world.planet)
        elif level < 80 :
            self.planet_sprite = ModelSprite('images/planet3-4.png', model=self.world.planet)
        elif level == 100 :
            self.planet_sprite = ModelSprite('images/planet3-5.png', model=self.world.planet)

if __name__ == '__main__':
    window = PlanetGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
