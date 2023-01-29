import os

from animation import *
from utilities import *

# show red bounding box toggle
DEBUG = 0

CAMREA_CENTER_X = 9 * TILE_WIDTH
CAMREA_CENTER_Y = 7 * TILE_WIDTH
# TODO: these coordinates are manually measured, this is sort of hard coded, 
# need a more generic way of loading sprite sheets
PLAYER_HEIGHT = 48
PLAYER_SHEET = pygame.image.load(os.path.join("assets", "player.png"))
PLAYER_FRONT_SURFACE = PLAYER_SHEET.subsurface(7, 2, 17, 25)
PLAYER_BACK_SURFACE  = PLAYER_SHEET.subsurface(7, 34, 17, 25)
PLAYER_LEFT_SURFACE  = PLAYER_SHEET.subsurface(39, 33, 17, 25)
PLAYER_RIGHT_SURFACE = PLAYER_SHEET.subsurface(39, 2, 17, 25)

FLOWER_SS = pygame.image.load(os.path.join("assets", "flower.png"))

class EntitySurfaceType(Enum):
    GROUND  = [pygame.image.load(os.path.join("assets", "ground_0.png"))]
    GROUND2 = [pygame.image.load(os.path.join("assets", "ground_1.png"))]
    FLOWER  = [FLOWER_SS.subsurface(0, 0, 32, 32), FLOWER_SS.subsurface(32, 0, 32, 32)]
    MUSH    = [pygame.image.load(os.path.join("assets", "mushroom.png"))]
    GRASS   = [pygame.image.load(os.path.join("assets", "grass.png"))]
    TREE    = [pygame.image.load(os.path.join("assets", "tree.png"))]

class Entity:
    def __init__(self, x, y, width, height, entity_surface_type: EntitySurfaceType):
        self.x = x
        self.y = y
        self.width = width * TILE_WIDTH
        self.height = height * TILE_WIDTH

        sprite_list = entity_surface_type.value
        for i in range(len(sprite_list)):
            sprite_list[i] = pygame.transform.scale(sprite_list[i], (self.width, self.height))
        self.animation = Animation(sprite_list, HALF_SEC_INTERVAL)

    def draw(self, window):
        window.blit(self.animation.get_sprite(), (self.x, self.y))

class SolidEntity(Entity):
    def __init__(self, x, y, width, height, entity_surface_type: EntitySurfaceType):
        super().__init__(x, y, width, height, entity_surface_type)
        self.bounding_box = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        super().draw(window)
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)


class Player():
    def __init__(self):
        self.x = CAMREA_CENTER_X
        self.y = CAMREA_CENTER_Y
        self.next_x = CAMREA_CENTER_X
        self.next_y = CAMREA_CENTER_Y

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
        self.bounding_box = pygame.Rect(self.x, self.y, TILE_WIDTH, TILE_WIDTH)
        self._top_bounding_box = pygame.Rect(self.x, self.y - TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self._bottom_bounding_box = pygame.Rect(self.x, self.y + TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self._left_bounding_box = pygame.Rect(self.x - TILE_WIDTH, self.y, TILE_WIDTH, TILE_WIDTH)
        self._right_bounding_box = pygame.Rect(self.x + TILE_WIDTH, self.y, TILE_WIDTH, TILE_WIDTH)
        
    def draw(self, window):
        window.blit(self.surface, (self.x, self.y - TILE_WIDTH // 2))
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)

    def update(self, entity_list):
        # check control
        if self.camera_x == self.next_camera_x and self.camera_y == self.next_camera_y:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                self.surface = self._left_surface
                if not is_bb_collide_with_entity_list(self._left_bounding_box, entity_list):
                    self.next_camera_x =  self.camera_x + TILE_WIDTH
            elif keys_pressed[pygame.K_d]:
                self.surface = self._right_surface
                if not is_bb_collide_with_entity_list(self._right_bounding_box, entity_list):
                    self.next_camera_x =  self.camera_x - TILE_WIDTH
            elif keys_pressed[pygame.K_w]:
                self.surface = self._back_surface
                if not is_bb_collide_with_entity_list(self._top_bounding_box, entity_list):
                    self.next_camera_y = self.camera_y + TILE_WIDTH
            elif keys_pressed[pygame.K_s]:
                self.surface = self._front_surface
                if not is_bb_collide_with_entity_list(self._bottom_bounding_box, entity_list):
                    self.next_camera_y = self.camera_y - TILE_WIDTH
            if keys_pressed[pygame.K_k]:
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

            self.camera_x += move_x
            self.camera_y += move_y
            move_entity_list(entity_list, move_x, move_y)



'''
Helper functions
'''

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