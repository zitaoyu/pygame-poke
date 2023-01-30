import json

from entity import *
from utilities import *


class OpenWorld:
    def __init__(self, window: Surface, player: Player):
        self.window = window
        self.player = player
        self.entity_list = []
        self.load_map(player_start_x=15 * TILE_WIDTH, player_start_y=11 * TILE_WIDTH)

    def __add_entity(self, entity):
        self.entity_list.append(entity)

    def load_map(self, player_start_x=0, player_start_y=0, map=None):
        self.entity_list = []
        object = json.load(open("./Maps/map.json"))["testMap"]
        map = object["map"]
        background_music = object["backgroundMusic"]
        GLOBAL_SOUND_PLAYER.play_track(background_music)
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