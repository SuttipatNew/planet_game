import arcade
from models import World, Ship

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

class PlanetGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.world = World(width, height)

        self.ship_sprite = ModelSprite('images/ship.png', model=self.world.ship)
        self.planet_sprite = ModelSprite('images/planet2.png', model=self.world.planet)
        self.bullet_sprites = []
        self.water_bar_sprites = []
        self.meteorite_sprites = []

    def on_draw(self):
        arcade.start_render()

        self.planet_sprite.draw()
        for bullet_sprite in self.bullet_sprites:
            bullet_sprite.draw()
        self.ship_sprite.draw()

        for meteorite_sprite in self.meteorite_sprites:
            meteorite_sprite.draw()

        for water_bar_sprite in self.water_bar_sprites:
            water_bar_sprite.draw()

        arcade.draw_text(str(self.world.score), self.width - 30, self.height - 30, arcade.color.WHITE, 20)

    def animate(self, delta):
        self.world.animate(delta)
        self.create_sprite_for_new_bullet()
        self.remove_unuse_bullet_sprite()
        self.create_sprite_for_new_water_bar()
        self.create_sprite_for_new_meteorite()
        self.remove_unuse_meteorite_sprite()
        self.remove_bullet_and_meteorite()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def create_sprite_for_new_bullet(self) :
        if(len(self.world.bullets) > 0) :
            for bullet in self.world.bullets :
                sprite_exists = False
                for bullet_sprite in self.bullet_sprites :
                    if bullet == bullet_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.bullet_sprites.append(ModelSprite('images/bullet.png', model=bullet))

    def remove_unuse_bullet_sprite(self) :
        if(len(self.bullet_sprites) > 0) :
            for bullet_sprite in self.bullet_sprites :
                if(bullet_sprite.model not in self.world.bullets) :
                    self.bullet_sprites.remove(bullet_sprite)

    def create_sprite_for_new_water_bar(self) :
        if(len(self.world.water_bars) > 0) :
            for water_bar in self.world.water_bars :
                sprite_exists = False
                for water_bar_sprite in self.water_bar_sprites :
                    if water_bar == water_bar_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.water_bar_sprites.append(ModelSprite('images/rect-blue.png', model=water_bar))

    def create_sprite_for_new_meteorite(self) :
        if(len(self.world.meteorites) > 0) :
            for meteorite in self.world.meteorites :
                sprite_exists = False
                for meteorite_sprite in self.meteorite_sprites :
                    if meteorite == meteorite_sprite.model :
                        sprite_exists = True
                        break
                if not sprite_exists :
                    self.meteorite_sprites.append(ModelSprite('images/meteorite.png', model=meteorite))

    def remove_unuse_meteorite_sprite(self) :
        if(len(self.meteorite_sprites) > 0) :
            for meteorite_sprite in self.meteorite_sprites :
                if(meteorite_sprite.model not in self.world.meteorites) :
                    self.meteorite_sprites.remove(meteorite_sprite)

    def remove_bullet_and_meteorite(self) :
        for bullet_sprite in self.bullet_sprites :
            for meteorite_sprite in self.meteorite_sprites :
                if arcade.check_for_collision(bullet_sprite, meteorite_sprite) :
                    try:
                        # self.bullet_sprites.remove(bullet_sprite)
                        # self.meteorite_sprites.remove(meteorite_sprite)
                        self.world.bullets.remove(bullet_sprite.model)
                        self.world.meteorites.remove(meteorite_sprite.model)
                    except:
                        pass

if __name__ == '__main__':
    window = PlanetGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
