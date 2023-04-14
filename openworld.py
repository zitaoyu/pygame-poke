import json

from entity import *
from utilities import *
from battlescene import *


class OpenWorld:
    def __init__(self, window: Surface, player: Player):
        self.window: Surface = window
        self.player: Player = player
        self.entity_list: List[Entity] = []
        self.load_map(player_start_x=15 * TILE_SIZE, player_start_y=11 * TILE_SIZE)
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
                x += TILE_SIZE
            y += TILE_SIZE

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
                    self.__add_entity(SolidEntity(x, y, 2, 2, EntitySurfaceType.TREE))
                x += TILE_SIZE
            y += TILE_SIZE

    def __move_entity_list(self, move_x, move_y):
        for entity in self.entity_list:
            entity.x += move_x
            entity.y += move_y
            if isinstance(entity, SolidEntity):
                entity.bounding_box.move_ip(move_x, move_y)

    def __is_bb_collide_with_entity_list(self, bb):
        for entity in self.entity_list:
            if isinstance(entity, SolidEntity) and bb.colliderect(entity.bounding_box):
                return True
        return False

    def update_player(self):
        # check control
        # TODO: implement universal input controller instead of saperate input check for battlescene and player
        player = self.player
        camera_x = player.camera_x
        camera_y = player.camera_y
        if camera_x == player.next_camera_x and camera_y == player.next_camera_y:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                player.surface = player.left_surface
                if not self.__is_bb_collide_with_entity_list(player.left_bounding_box):
                    player.next_camera_x =  camera_x + TILE_SIZE
            elif keys_pressed[pygame.K_d]:
                player.surface = player.right_surface
                if not self.__is_bb_collide_with_entity_list(player.right_bounding_box):
                    player.next_camera_x =  camera_x - TILE_SIZE
                else:
                    player.encouter = True
            elif keys_pressed[pygame.K_w]:
                player.surface = player.back_surface
                if not self.__is_bb_collide_with_entity_list(player.top_bounding_box):
                    player.next_camera_y = camera_y + TILE_SIZE
            elif keys_pressed[pygame.K_s]:
                player.surface = player.front_surface
                if not self.__is_bb_collide_with_entity_list(player.bottom_bounding_box):
                    player.next_camera_y = camera_y - TILE_SIZE
            if keys_pressed[pygame.K_k]:
                player.running = True
            else:
                player.running = False
        
        #  update position
        if not (camera_x == player.next_camera_x and camera_y == player.next_camera_y):
            velocity = 4 if player.running else 2
            move_x = 0
            move_y = 0
            if camera_x < player.next_camera_x:
                move_x = velocity
            elif camera_x > player.next_camera_x:
                move_x = -velocity
            if camera_y < player.next_camera_y:
                move_y = velocity
            elif camera_y > player.next_camera_y:
                move_y = -velocity

            player.camera_x += move_x
            player.camera_y += move_y
            self.__move_entity_list(move_x, move_y)

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
            self.update_player()
            for entity in self.entity_list:
                entity.draw(self.window)
            self.player.draw(self.window)