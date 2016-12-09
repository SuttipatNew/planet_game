import arcade
from time import time
from models import Ship, random_prob
from world import World
import pyglet.gl as gl

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
        self.width = width
        self.height = height
        arcade.set_background_color(arcade.color.BLACK)

        self.on_menu = True
        # self.on_menu = False
        self.menu_selecting = 0
        self.max_menu = 2
        self.selector_sprite = arcade.Sprite('images/selector.png')
        self.selector_sprite.set_position(200, 255)

        self.menu_screen = arcade.Sprite('images/menu.png')
        self.menu_screen.set_position(width/2, height/2)
        self.menu_keys = []

        self.instruction_screen = arcade.Sprite('images/instruction.jpg')
        self.instruction_screen.set_position(width/2, height/2)
        self.on_instruction = False

        self.menu_prop = arcade.Sprite('images/planet3-6.png')
        self.menu_prop_x = 650
        self.menu_prop_y = 150
        self.menu_prop_direction = 'up'
        self.menu_prop.set_position(self.menu_prop_x, self.menu_prop_y)

        self.gameover_screen = arcade.Sprite('images/gameover.jpg')
        self.gameover_screen.set_position(width/2, height/2)
        self.gameover = False
        self.gameover_selecting = 0
        self.gameover_keys = []
        self.max_gameover_menu = 2
        # self.gameover_listenner_notify()

    def on_draw(self):
        arcade.start_render()
        if self.on_menu :
            self.menu_screen.draw()
            self.selector_sprite.draw()
            self.menu_prop.draw()
        elif self.on_instruction :
            self.instruction_screen.draw()
        elif self.gameover :
            self.gameover_screen.draw()
            self.selector_sprite.draw()
            self.menu_prop.draw()
            arcade.draw_text("SCORE: " + str(self.world.score), self.width / 2 - 50, self.height / 2, arcade.color.WHITE, 20)
        else :
            self.background.draw()
            self.planet_sprite.draw()
            for bullet_sprite in self.bullet_sprites:
                bullet_sprite.draw()

            for ammo_sprite in self.ammo_sprites :
                ammo_sprite.draw()

            self.ship_sprite.draw()

            for meteorite_sprite in self.meteorite_sprites:
                meteorite_sprite.draw()

            gl.glDisable(gl.GL_TEXTURE_2D)
            ship = self.world.ship
            planet = self.world.planet
            water = self.world.water
            full_water = self.world.full_water

            arcade.draw_lrtb_rectangle_filled(ship.x - ship.full_health * 4 / 2, \
             ship.x - ship.full_health * 4 / 2 + ship.health * 4, ship.y + 60, ship.y + 56, arcade.color.RED)
            arcade.draw_lrtb_rectangle_filled(planet.x - full_water * 4 / 2 , \
             planet.x - full_water * 4 / 2 + water * 4, planet.y + 100, planet.y + 90, (0, 174, 239))

            arcade.draw_text("SCORE: " + str(self.present_score), self.width - 150, self.height - 30, arcade.color.WHITE, 16)
            arcade.draw_text("AMMO: " + str(self.present_ammo_num), self.width - 120, 20, arcade.color.WHITE, 16)

    def animate(self, delta):
        if self.on_menu :
            self.update_menu()
            self.update_selector_menu()
            self.update_menu_prop()
        elif self.on_instruction :
            pass
        elif self.gameover :
            self.update_menu_prop()
            self.update_selector_gameover()
            self.update_gameover()
        else :
            self.world.animate(delta)
            self.remove_bullet_and_meteorite()
            self.ship_on_planet()
            self.create_sprite_for_new_ammo()
            self.ship_pick_ammo()
            self.meteorite_hit_ship()
            self.update_ui()
            self.update_planet()

    def update_menu_prop(self) :
        if self.menu_prop_y < 156 and self.menu_prop_direction == 'up':
            self.menu_prop_y += 0.2
        elif self.menu_prop_y >= 156 and self.menu_prop_direction == 'up':
            self.menu_prop_direction = 'down'
        elif self.menu_prop_y > 144 and self.menu_prop_direction == 'down':
            self.menu_prop_y -= 0.2
        elif self.menu_prop_y <= 144 and self.menu_prop_direction == 'down' :
            self.menu_prop_direction = 'up'

        self.menu_prop.set_position(self.menu_prop_x, self.menu_prop_y)

    def update_instruction(self, key) :
        if key == 65293 :
            self.on_instruction = False
            self.on_menu = True

    def update_menu(self) :
        if len(self.menu_keys) > 0 :
            # print(self.menu_keys)
            if 65362 in self.menu_keys :
                self.menu_selecting -= 1
                self.menu_selecting %= self.max_menu
            elif 65364 in self.menu_keys :
                self.menu_selecting += 1
                self.menu_selecting %= self.max_menu
            elif 65293 in self.menu_keys :
                if self.menu_selecting == 0 :
                    self.on_menu = False
                    self.init_game()
                elif self.menu_selecting == 1 :
                    self.on_instruction = True
                    self.on_menu = False
                    self.gameover = False
                    self.menu_selecting = 0
            self.menu_keys = []

    def update_selector_menu(self) :
        if self.menu_selecting == 0 :
            self.selector_sprite.set_position(200, 255)
        else :
            self.selector_sprite.set_position(200, 190)

    def gameover_listenner_notify(self) :
        self.gameover = True
        self.on_menu = False
        self.on_instruction = False
        self.selector_sprite.set_position(280, 180)
        self.gameover_selecting = 0

    def update_selector_gameover(self) :
        if self.gameover_selecting == 0 :
            self.selector_sprite.set_position(280, 180)
        elif self.gameover_selecting == 1 :
            self.selector_sprite.set_position(280, 110)

    def update_gameover(self) :
        if len(self.gameover_keys) > 0 :
            # print(self.menu_keys)
            if 65362 in self.gameover_keys :
                self.gameover_selecting -= 1
                self.gameover_selecting %= self.max_gameover_menu
            elif 65364 in self.gameover_keys :
                self.gameover_selecting += 1
                self.gameover_selecting %= self.max_gameover_menu
            elif 65293 in self.gameover_keys :
                if self.gameover_selecting == 0 :
                    self.on_menu = False
                    self.on_instruction = False
                    self.gameover = False
                    self.init_game()
                elif self.gameover_selecting == 1 :
                    self.on_instruction = False
                    self.gameover = False
                    self.on_menu = True
                self.gameover_selecting = 0
            self.gameover_keys = []

    def init_game(self) :
        self.background = arcade.Sprite('images/background_star.png')
        self.background.set_position(self.width/2, self.height/2)

        self.world = World(self.width, self.height)

        self.ship_sprite = ModelSprite('images/ship.png', model=self.world.ship)
        self.planet_sprite = ModelSprite('images/planet3-1.png', model=self.world.planet)
        self.bullet_sprites = []
        self.meteorite_sprites = []
        self.ammo_sprites = []

        self.present_score = self.world.score
        self.present_ammo_num = self.world.ship.ammo_num

        self.world.bullet_listenner.add(self.bullet_listenner_nofify)
        self.world.meteorite_listenner.add(self.meteorite_listenner_notify)
        self.world.gameover_listenner.add(self.gameover_listenner_notify)
        self.world.water_bar_full_listenner.add(self.water_bar_full_listenner_notify)

        self.water_bar_decrease_timer = time()

    def on_key_press(self, key, key_modifiers):
        if self.on_menu :
            self.menu_keys.append(key)
        elif self.on_instruction :
            self.update_instruction(key)
        elif self.gameover :
            self.gameover_keys.append(key)
        else :
            self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        if self.on_menu :
            try :
                self.menu_keys.remove(key)
            except :
                pass
        elif self.on_instruction :
            pass
        elif self.gameover :
            try :
                self.gameover_keys.remove(key)
            except :
                pass
        else :
            self.world.on_key_release(key, key_modifiers)

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
            self.water_bar_decrease_timer = time()
        elif time() - self.water_bar_decrease_timer >= 2:
            self.water_bar_decrease_timer = time()
            if self.world.water > 0 :
                self.world.water -= 1

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

    def meteorite_hit_ship(self) :
        for meteorite_sprite in self.meteorite_sprites :
            if arcade.check_for_collision(meteorite_sprite, self.ship_sprite) :
                if self.world.ship.health > 0 :
                    self.world.ship.health -= 1
                else :
                    print('ship destroyed')
                try:
                    self.world.meteorites.remove(meteorite_sprite.model)
                    self.meteorite_sprites.remove(meteorite_sprite)
                    del meteorite_sprite.model
                    del meteorite_sprite
                except:
                    pass
                return

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

    def water_bar_full_listenner_notify(self) :
        self.planet_sprite = ModelSprite('images/planet3-1.png', model=self.world.planet)

    def meteorite_listenner_notify(self, message, meteorite) :
        if message == 'remove':
            for meteorite_sprite in self.meteorite_sprites :
                if meteorite_sprite.model == meteorite :
                    self.meteorite_sprites.remove(meteorite_sprite)
                    del meteorite_sprite
        elif message == 'new' :
            self.meteorite_sprites.append(ModelSprite('images/meteorite.png', model=meteorite))
        elif message == 'hit_planet' :
            try :
                self.meteorite_listenner_notify('remove', meteorite)
                self.world.water -= 2
            except :
                pass

    def update_planet(self) :
        level = self.world.water / self.world.full_water * 100
        if level < 20 :
            self.planet_sprite = ModelSprite('images/planet3-1.png', model=self.world.planet)
        elif level < 40 :
            self.planet_sprite = ModelSprite('images/planet3-2.png', model=self.world.planet)
        elif level < 60 :
            self.planet_sprite = ModelSprite('images/planet3-3.png', model=self.world.planet)
        elif level < 80 :
            self.planet_sprite = ModelSprite('images/planet3-5.png', model=self.world.planet)
        elif level < 100 :
            self.planet_sprite = ModelSprite('images/planet3-6.png', model=self.world.planet)
        # else :
        #     self.planet_sprite = ModelSprite('images/planet3-6.png', model=self.world.planet)

if __name__ == '__main__':
    window = PlanetGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
