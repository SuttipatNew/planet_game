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

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.world = World(width, height)

        self.ship_sprite = ModelSprite('images/ship.png', model=self.world.ship)
        # self.gold_sprite = ModelSprite('images/Gold.png',model=self.world.gold)
        self.planet_sprite = ModelSprite('images/planet.png', model=self.world.planet)


    def on_draw(self):
        arcade.start_render()
        # self.gold_sprite.draw()
        self.planet_sprite.draw()
        self.ship_sprite.draw()

        arcade.draw_text(str(self.world.score), self.width - 30, self.height - 30, arcade.color.WHITE, 20)

    def animate(self, delta):
        self.world.animate(delta);

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
