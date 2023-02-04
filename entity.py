import os

from animation import *
from utilities import *
from pokemon import *

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

        self.type = entity_surface_type
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
        self.front_surface = pygame.transform.scale(PLAYER_FRONT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self.back_surface = pygame.transform.scale(PLAYER_BACK_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self.left_surface = pygame.transform.scale(PLAYER_LEFT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self.right_surface = pygame.transform.scale(PLAYER_RIGHT_SURFACE, (TILE_WIDTH, PLAYER_HEIGHT))
        self.surface = self.front_surface

        # bounding boxes
        self.bounding_box = pygame.Rect(self.x, self.y, TILE_WIDTH, TILE_WIDTH)
        self.top_bounding_box = pygame.Rect(self.x, self.y - TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self.bottom_bounding_box = pygame.Rect(self.x, self.y + TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
        self.left_bounding_box = pygame.Rect(self.x - TILE_WIDTH, self.y, TILE_WIDTH, TILE_WIDTH)
        self.right_bounding_box = pygame.Rect(self.x + TILE_WIDTH, self.y, TILE_WIDTH, TILE_WIDTH)

        self.party: PokemonParty = PokemonParty([Pokemon(1, 5)])
        self.encouter = False
        
    def draw(self, window):
        window.blit(self.surface, (self.x, self.y - TILE_WIDTH // 2))
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)