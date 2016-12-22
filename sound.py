import arcade
class Sound:
    def __init__(self) :
        self.fire = arcade.sound.load_sound('sound/fire.mp3')
        self.bgm = arcade.sound.load_sound('sound/bgm.mp3')

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
            arcade.sound.pause(self.bgm)
        except:
            pass
