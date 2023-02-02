import json

from entity import *
from utilities import *
from battlescene import *


class OpenWorld:
    def __init__(self, window: Surface, player: Player):
        self.window = window
        self.player = player
        self.entity_list = []
        self.load_map(player_start_x=15 * TILE_WIDTH, player_start_y=11 * TILE_WIDTH)
        self.battle_scene: BattleScene = None

    def __add_entity(self, entity):
        self.entity_list.append(entity)

    def load_map(self, player_start_x=0, player_start_y=0, map=None):
        self.entity_list = []
        object = json.load(open("./Maps/map.json"))["testMap"]
        map = object["map"]
        self.background_music = object["backgroundMusic"]
        GLOBAL_SOUND_PLAYER.play_track(self.background_music)
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
        # TODO: better logic to switch between openworld and battlescene
        if self.player.encouter:
            self.battle_scene = BattleScene(self.window, BattleManager(self.player.party, PokemonParty([Pokemon(4, 5)])))
            self.player.encouter = False
        self.window.fill(WHITE)
        if self.battle_scene:
            if self.battle_scene.is_ended:
                self.battle_scene = None
                GLOBAL_SOUND_PLAYER.play_track(self.background_music)
                return
            self.battle_scene.draw_entity_list()
        else:
            self.player.update(self.entity_list)
            for entity in self.entity_list:
                entity.draw(self.window)
            self.player.draw(self.window)