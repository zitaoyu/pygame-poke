from enum import Enum
from utilities import *
import pygame
import os

DEBUG = 1

# TODO: these coordinates are manually measured, this is sort of hard coded, 
# need a more generic way of loading sprite sheets
PLAYER_HEIGHT = 48
PLAYER_SHEET = pygame.image.load(os.path.join("assets", "player.png"))
PLAYER_FRONT_SURFACE = PLAYER_SHEET.subsurface(7, 2, 17, 25)
PLAYER_BACK_SURFACE  = PLAYER_SHEET.subsurface(7, 34, 17, 25)
PLAYER_LEFT_SURFACE  = PLAYER_SHEET.subsurface(39, 33, 17, 25)
PLAYER_RIGHT_SURFACE = PLAYER_SHEET.subsurface(39, 2, 17, 25)
TILE_SHEET = pygame.image.load(os.path.join("assets", "tileset.png"))

class EntitySurfaceType(Enum):
    GROUND = TILE_SHEET.subsurface(0, 32, 16, 16)
    GROUND2 = TILE_SHEET.subsurface(16, 32, 16, 16)
    FLOWER = TILE_SHEET.subsurface(32, 32, 16, 16)
    MUSH = TILE_SHEET.subsurface(48, 32, 16, 16)
    GRASS = TILE_SHEET.subsurface(64, 32, 16, 16)

class Entity:
    def __init__(self, x, y, width, height, entity_surface_type: EntitySurfaceType):
        self.x = x
        self.y = y
        self.width = width * TILE_WIDTH
        self.height = width * TILE_WIDTH
        self.surface = entity_surface_type.value
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))

    def draw(self, window):
        if self.surface != None:
            window.blit(self.surface, (self.x, self.y))

class SolidEntity(Entity):
    def __init__(self, x, y, width, height, entity_surface_type: EntitySurfaceType):
        super().__init__(x, y, width, height, entity_surface_type)
        self.bounding_box = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        super().draw(window)
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y

        self.camera_x = 0
        self.camera_y = 0
        self.next_camera_x = 0
        self.next_camera_y = 0

        # sprites
        self._front_surface = pygame.transform.scale(PLAYER_FRONT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self._back_surface = pygame.transform.scale(PLAYER_BACK_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self._left_surface = pygame.transform.scale(PLAYER_LEFT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self._right_surface = pygame.transform.scale(PLAYER_RIGHT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self.surface = self._front_surface

        # bounding boxes
        self.bounding_box = pygame.Rect(x, y, TILE_WIDTH, TILE_WIDTH)
        self._top_bounding_box = pygame.Rect(x, y - TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self._bottom_bounding_box = pygame.Rect(x, y + TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self._left_bounding_box = pygame.Rect(x - TILE_WIDTH, y, TILE_WIDTH, TILE_WIDTH)
        self._right_bounding_box = pygame.Rect(x + TILE_WIDTH, y, TILE_WIDTH, TILE_WIDTH)
        
    def draw(self, window):
        window.blit(self.surface, (self.x, self.y - TILE_WIDTH // 2))
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)

    def update(self, entity_list):
        # check control
        if self.camera_x == self.next_camera_x and self.camera_y == self.next_camera_y:
            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_a]:
                self.surface = self._left_surface
                if not is_bb_collide_with_entity_list(self._left_bounding_box, entity_list):
                    self.next_camera_x =  self.camera_x + TILE_WIDTH
            elif keysPressed[pygame.K_d]:
                self.surface = self._right_surface
                if not is_bb_collide_with_entity_list(self._right_bounding_box, entity_list):
                    self.next_camera_x =  self.camera_x - TILE_WIDTH
            elif keysPressed[pygame.K_w]:
                self.surface = self._back_surface
                if not is_bb_collide_with_entity_list(self._top_bounding_box, entity_list):
                    self.next_camera_y = self.camera_y + TILE_WIDTH
            elif keysPressed[pygame.K_s]:
                self.surface = self._front_surface
                if not is_bb_collide_with_entity_list(self._bottom_bounding_box, entity_list):
                    self.next_camera_y = self.camera_y - TILE_WIDTH
            if keysPressed[pygame.K_k]:
                self.running = True
            else:
                self.running = False
        
        #  update position
        if not (self.camera_x == self.next_camera_x and self.camera_y == self.next_camera_y):
            velocity = 4 if self.running else 2
            move_x = move_y = 0
            if self.camera_x < self.next_camera_x:
                move_x = velocity
            elif self.camera_x > self.next_camera_x:
                move_x = -velocity
            if self.camera_y < self.next_camera_y:
                move_y = velocity
            elif self.camera_y > self.next_camera_y:
                move_y = -velocity

            # self.bounding_box.move_ip(move_x, move_y)
            # for entity in entity_list:
            #     if isinstance(entity, SolidEntity) and self.bounding_box.colliderect(entity.bounding_box):
            #         self.bounding_box.move_ip(-move_x, -move_y)
            #         self.next_camera_x = self.camera_x
            #         self.next_camera_y = self.camera_y
            #         move_x = move_y = 0
            #         break
            self.camera_x += move_x
            self.camera_y += move_y
            move_entity_list(entity_list, move_x, move_y)

def move_entity_list(entity_list, move_x, move_y):
    for entity in entity_list:
        entity.x += move_x
        entity.y += move_y
        if isinstance(entity, SolidEntity):
            entity.bounding_box.move_ip(move_x, move_y)

def is_bb_collide_with_entity_list(bb, entity_list):
    for entity in entity_list:
        if isinstance(entity, SolidEntity) and bb.colliderect(entity.bounding_box):
            return True
    return False