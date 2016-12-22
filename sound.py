import arcade
class Sound:
    def __init__(self) :
        self.fire = arcade.sound.load_sound('sound/fire.mp3')
        self.bgm = arcade.sound.load_sound('sound/bgm.mp3')
        self.full_water = arcade.sound.load_sound('sound/coin.wav')
        self.bomb = arcade.sound.load_sound('sound/explosion.wav')
        self.ammo = arcade.sound.load_sound('sound/ammo.wav')

    def play_fire(self) :
        try :
            arcade.sound.play_sound(self.fire)
        except :
            pass

    def play_bgm(self):
        try :
            arcade.sound.play_sound(self.bgm)
        except :
            pass

    def stop_bgm(self):
        try:
            self.bgm.stop()
        except:
            pass

    def play_full_water(self):
        try:
            arcade.sound.play_sound(self.full_water)
        except:
            pass

    def play_explosion(self):
        try:
            arcade.sound.play_sound(self.bomb)
        except:
            pass

    def play_ammo(self):
        try:
            arcade.sound.play_sound(self.ammo)
        except:
            pass
