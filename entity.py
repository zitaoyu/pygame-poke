import os

from animation import *
from utilities import *
from pokemon import *

# show red bounding box toggle
DEBUG = 0

FLOWER_SS = pygame.image.load(os.path.join("assets", "flower.png"))

class EntitySurfaceType(Enum):
    GROUND  = Animation(pygame.image.load(os.path.join("assets", "ground_0.png")))
    GROUND2 = Animation(pygame.image.load(os.path.join("assets", "ground_1.png")))
    FLOWER  = Animation(FLOWER_SS, 0, 0, 32, 32, 2)
    MUSH    = Animation(pygame.image.load(os.path.join("assets", "mushroom.png")))
    GRASS   = Animation(pygame.image.load(os.path.join("assets", "grass.png")))
    TREE    = Animation(pygame.image.load(os.path.join("assets", "tree.png")))

class Entity:
    def __init__(self, x, y, width, height, entity_surface_type: EntitySurfaceType):
        self.x = x
        self.y = y
        self.width = width * TILE_SIZE
        self.height = height * TILE_SIZE

        self.type = entity_surface_type
        self.animation: Animation = self.type.value
        self.animation.scale_sprites(self.width, self.height)

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


# TODO: these coordinates are manually measured, this is sort of hard coded, 
# need a more generic way of loading sprite sheets
PLAYER_HEIGHT = 1.5 * TILE_SIZE
PLAYER_SHEET = pygame.image.load(os.path.join("assets", "player.png"))
PLAYER_FRONT_IMG = pygame.image.load(os.path.join("assets", "player-front-run.png"))
PLAYER_FRONT_SURFACE = Animation(PLAYER_FRONT_IMG, 0, 0, 48, 72, 4)
PLAYER_FRONT_SURFACE.scale_sprites(TILE_SIZE, PLAYER_HEIGHT)
PLAYER_BACK_SURFACE  = Animation(PLAYER_SHEET.subsurface(7, 34, 17, 25))
PLAYER_BACK_SURFACE.scale_sprites(TILE_SIZE, PLAYER_HEIGHT)
PLAYER_LEFT_SURFACE  = Animation(PLAYER_SHEET.subsurface(39, 33, 17, 25))
PLAYER_LEFT_SURFACE.scale_sprites(TILE_SIZE, PLAYER_HEIGHT)
PLAYER_RIGHT_SURFACE = Animation(PLAYER_SHEET.subsurface(39, 2, 17, 25))
PLAYER_RIGHT_SURFACE.scale_sprites(TILE_SIZE, PLAYER_HEIGHT)

class Player():
    def __init__(self):
        self.x = CAMREA_CENTER_X
        self.y = CAMREA_CENTER_Y
        self.next_x = CAMREA_CENTER_X
        self.next_y = CAMREA_CENTER_Y
        self.running: bool = False

        self.camera_x = 0
        self.camera_y = 0
        self.next_camera_x = 0
        self.next_camera_y = 0

        # sprites
        self.front_surface = PLAYER_FRONT_SURFACE
        self.back_surface = PLAYER_BACK_SURFACE
        self.left_surface = PLAYER_LEFT_SURFACE
        self.right_surface = PLAYER_RIGHT_SURFACE
        self.surface = self.front_surface

        # bounding boxes
        self.bounding_box = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self.top_bounding_box = pygame.Rect(self.x, self.y - TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.bottom_bounding_box = pygame.Rect(self.x, self.y + TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.left_bounding_box = pygame.Rect(self.x - TILE_SIZE, self.y, TILE_SIZE, TILE_SIZE)
        self.right_bounding_box = pygame.Rect(self.x + TILE_SIZE, self.y, TILE_SIZE, TILE_SIZE)

        self.party: PokemonParty = PokemonParty([Pokemon(1, 5)])
        self.encouter = False
        
    def draw(self, window):
        window.blit(self.surface.get_sprite(), (self.x, self.y - TILE_SIZE // 2))
        if DEBUG:
            pygame.draw.rect(window, RED, self.bounding_box, 1)