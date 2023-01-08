import json

import pygame
from pygame.locals import *

from battlescene import *
from entity import *
from sound_player import SoundPlayer
from utilities import *


class OpenWorld:
    def __init__(self, window, player: Player):
        self.window = window
        self.player = player
        self.sound_player = SoundPlayer()
        self.entity_list = []
        self.load_map(player_start_x=15 * TILE_WIDTH, player_start_y=11 * TILE_WIDTH)

    def __add_entity(self, entity):
        self.entity_list.append(entity)

    def load_map(self, player_start_x=0, player_start_y=0, map=None):
        self.entity_list = []
        object = json.load(open("./Maps/map.json"))["testMap"]
        map = object["map"]
        background_music = object["backgroundMusic"]
        self.sound_player.play_track(background_music)
        camera_offest_x = -(player_start_x - CAMREA_CENTER_X)
        camera_offest_y = -(player_start_y - CAMREA_CENTER_Y)

        ground_map = map["groundTiles"]
        y = camera_offest_y
        for row in ground_map:
            x = camera_offest_x
            for tile in row:
                if tile == 0:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GROUND))
                elif tile == 1:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GROUND2))
                elif tile == 2:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.FLOWER))
                x += TILE_WIDTH
            y += TILE_WIDTH

        object_map = map["objects"]
        x = camera_offest_x
        y = camera_offest_y
        for row in object_map:
            x = camera_offest_x
            for tile in row:
                if tile == 3:
                    self.__add_entity(SolidEntity(x, y, 1, 1, EntitySurfaceType.MUSH))
                elif tile == 4:
                    self.__add_entity(Entity(x, y, 1, 1, EntitySurfaceType.GRASS))
                elif tile == 5:
                    self.__add_entity(SolidEntity(x, y, 3, 3, EntitySurfaceType.TREE))
                x += TILE_WIDTH
            y += TILE_WIDTH

    def draw_entity_list(self):
        self.window.fill(WHITE)
        self.player.update(self.entity_list)
        for entity in self.entity_list:
            entity.draw(self.window)
        self.player.draw(self.window)

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.player = Player()
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