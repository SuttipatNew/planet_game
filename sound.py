import arcade
class Sound:
    def __init__(self) :
        self.fire = arcade.sound.load_sound('sound/fire.mp3')

    def play_fire(self) :
        try :
            arcade.sound.play_sound(self.fire)
        except :
            pass
