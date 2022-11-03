from pygame import mixer

class SoundPlayer:

    def __init__(self):
        mixer.init()

    def play_sound(self, sound):
        pass

    def play_track(self, track):
        mixer.stop()
        mixer.music.load(track)
        mixer.music.play(-1)
