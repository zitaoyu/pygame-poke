from pygame import mixer, Surface
import pygame
from enum import Enum

FPS = 60
TILE_WIDTH = 32
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GAME_WINDOW_WIDTH = 640
GAME_WINDOW_HEIGHT = 480
GAME_NAME = "PyEmerald"

class SoundPlayer:

    def __init__(self):
        mixer.init()

    def play_sound(self, sound):
        pass

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