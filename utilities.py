from pygame import mixer, Surface
import pygame
from enum import Enum

FPS = 60
TILE_SIZE = 48
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GAME_WINDOW_WIDTH = TILE_SIZE * 15
GAME_WINDOW_HEIGHT = TILE_SIZE * 10
CAMREA_CENTER_X = 7 * TILE_SIZE
CAMREA_CENTER_Y = 4.5 * TILE_SIZE
GAME_NAME = "PyEmerald"

A_BUTTON = "./sounds/a-button.mp3"

class SoundPlayer:

    def __init__(self):
        mixer.init()

    def A_button(self):
        mixer.Sound(A_BUTTON).play()

    def play_sound(self, sound):
        mixer.Sound(sound).play()

    def play_track(self, track):
        mixer.stop()
        mixer.music.load(track)
        mixer.music.play(-1)

GLOBAL_SOUND_PLAYER = SoundPlayer()


class Logger:
    def __init__(self) -> None:
        self.__message = []

    def push(self, log):
        self.__message.append(log)

    def pop(self):
        if len(self.__message) == 0:
            return None
        return self.__message.pop()

    def __str__(self) -> str:
        return self.__message.__str__()

LOGGER = Logger()

def LOG(log):
    global LOGGER
    LOGGER.push(log)

def GETLOG():
    global LOGGER
    return LOGGER.pop()

def find_lowest_pixel_in_transparent_image(image_path):
    import numpy as np
    from PIL import Image
    img = Image.open(image_path)
    img = img.convert("RGBA")
    arr = np.array(img)
    for row_num in range(len(arr) - 1, 0, -1):
        for pixel in arr[row_num]:
            if any(pixel):
                return row_num
    return -1

class INPUT(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    SELECT = "select"
    BACK = "back"
    

def check_input():
    keys_pressed = pygame.key.get_pressed()
    inputs = []
    if keys_pressed[pygame.K_a]:
        inputs.append(INPUT.LEFT)
    elif keys_pressed[pygame.K_d]:
        inputs.append(INPUT.RIGHT)
    elif keys_pressed[pygame.K_w]:
        inputs.append(INPUT.UP)
    elif keys_pressed[pygame.K_s]:
        inputs.append(INPUT.DOWN)
    elif keys_pressed[pygame.K_j]:
        inputs.append(INPUT.SELECT)
    elif keys_pressed[pygame.K_k]:
        inputs.append(INPUT.BACK)
    return inputs

a = []
a.append("1")
a.append("2")
a.append("3")
print(a.pop(0))