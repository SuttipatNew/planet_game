import pyglet
class Sound:
    def __init__(self) :
        self.player = pyglet.media.Player()
        self.sound = None
        self.bgm = pyglet.media.load('sound/bgm.mp3')
        self.full_water = pyglet.media.load('sound/coin.wav')
        self.bomb = pyglet.media.load('sound/explosion.wav')
        self.ammo = pyglet.media.load('sound/ammo.wav')

        self.change_sound = pyglet.media.load('sound/change.mp3')
        self.select_sound = pyglet.media.load('sound/select.mp3')

    def play(self, message) :
        self.player.next()
        if message == 'fire':
            self.sound = pyglet.media.load('sound/fire.mp3')
        elif message == 'change':
            self.sound = pyglet.media.load('sound/change.mp3')
        elif message == 'select':
            self.sound = pyglet.media.load('sound/select.mp3')
        else:
            self.sound = None
        if self.sound != None:
            self.player.queue(self.sound)
        self.player.play()
