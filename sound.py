import pyglet
class Sound:
    def __init__(self) :
        self.gameover = False
        self.menu_player = pyglet.media.Player()
        self.fire_player = pyglet.media.Player()
        self.bgm_player = pyglet.media.Player()
        self.full_water_player = pyglet.media.Player()
        self.bomb_player = pyglet.media.Player()
        self.ammo_player = pyglet.media.Player()

    def play(self, message) :
        if message == 'fire':
            self.fire_player.next()
            self.fire = pyglet.media.load('sound/fire.mp3')
            self.fire_player.queue(self.fire)
        elif message == 'change':
            self.menu_player.next()
            self.menu = pyglet.media.load('sound/change.mp3')
            self.menu_player.queue(self.menu)
        elif message == 'select':
            self.menu_player.next()
            self.menu = pyglet.media.load('sound/select.mp3')
            self.menu_player.queue(self.menu)
        elif message == 'ammo':
            self.ammo_player.next()
            self.ammo = pyglet.media.load('sound/ammo.wav')
            self.ammo_player.queue(self.ammo)
        elif message == 'full_water':
            self.full_water_player.next()
            self.full_water = pyglet.media.load('sound/coin.wav')
            self.full_water_player.queue(self.full_water)
        elif message == 'bgm':
            self.bgm_player.next()
            self.bgm = pyglet.media.load('sound/bgm.mp3')
            self.bgm_player.queue(self.bgm)
        elif message == 'bomb':
            self.bomb_player.next()
            self.bomb = pyglet.media.load('sound/explosion.wav')
            self.bomb_player.queue(self.bomb)

        if not self.gameover:
            self.fire_player.play()
            self.ammo_player.play()
            self.bomb_player.play()
            self.full_water_player.play()
            self.bgm_player.play()

        self.menu_player.play()
