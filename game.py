from pygame.locals import *
from sound_player import SoundPlayer
from entity import *
from battlescene import *
from utilities import *
import pygame
import json
import time

class OpenWorld:
    def __init__(self, window, player: Player):
        self.window = window
        self.player = player
        self.sound_player = SoundPlayer()
        self.entity_list = []
        self.load_map()

    def __add_entity(self, entity):
        self.entity_list.append(entity)

    def load_map(self, map=None):
        self.entity_list = []
        object = json.load(open("./Maps/map.json"))["testMap"]
        map = object["map"]
        background_music = object["backgroundMusic"]
        self.sound_player.play_track(background_music)
        x = y =  0
        for row in map:
            x = 0
            for tile in row:
                if tile == 0:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GROUND))
                elif tile == 1:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GROUND2))
                elif tile == 2:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.FLOWER))
                elif tile == 3:
                    self.__add_entity(SolidEntity(x, y, 1, 1, EntitySurfaceType.MUSH))
                elif tile == 4:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GRASS))
                x += TILE_WIDTH
            y += TILE_WIDTH

    def draw_entity_list(self):
        self.window.fill(WHITE)
        for entity in self.entity_list:
            entity.draw(self.window)
        self.player.update(self.entity_list)
        self.player.draw(self.window)

FPS = 60
WIDTH = 640
HEIGHT = 480
GAME_NAME = "Pokemon Light"

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.player = Player(64, 64)
        self.open_world = OpenWorld(self.window, self.player)

    def draw_window(self):
        self.open_world.draw_entity_list()
        pygame.display.update()

    def run(self):
        print("Game lauched.")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_window()
        pygame.quit()

def main():
    Game().run()

if __name__ == "__main__":
    main()