from enum import Enum
import pygame
import os

DEBUG = 1
RED = (255, 0, 0)
TILE_WIDTH      = 32
PLAYER_HEIGHT   = 48
PLAYER_FRONT_CROP = (7, 2, 17, 25)
PLAYER_BACK_CROP  = (7, 34, 17, 25)
PLAYER_LEFT_CROP  = (39, 33, 17, 25)
PLAYER_RIGHT_CROP = (39, 2, 17, 25)
PLAYER_SHEET    = pygame.image.load(os.path.join("assets", "player.png"))
TILE_SHEET      = pygame.image.load(os.path.join("assets", "tileset.png"))

class TileType(Enum):
    GROUND = (0, 32, 16, 16)
    GROUND2 = (16, 32, 16, 16)
    FLOWER = (32, 32, 16, 16)
    MUSH = (48, 32, 16, 16)
    GRASS = (64, 32, 16, 16)

class Tile:
    def __init__(self, x, y, tileType = None):
        self.x = x
        self.y = y
        self.boudingBox = pygame.Rect(x, y, TILE_WIDTH, TILE_WIDTH)

        if tileType != None:
            self.tileType = tileType
            tileSurface = TILE_SHEET.subsurface(tileType.value)
            self.surface = pygame.transform.scale(tileSurface, (TILE_WIDTH, TILE_WIDTH))

    def update(self, window):
        if self.surface != None:
            window.blit(self.surface, (self.x, self.y))
            if DEBUG:
                pygame.draw.rect(window, (255, 0, 0), self.boudingBox, 1)

class Player(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nextX = self.x
        self.nextY = self.y

        self.front = PLAYER_SHEET.subsurface(PLAYER_FRONT_CROP)
        self.back = PLAYER_SHEET.subsurface(PLAYER_BACK_CROP)
        self.left = PLAYER_SHEET.subsurface(PLAYER_LEFT_CROP)
        self.right = PLAYER_SHEET.subsurface(PLAYER_RIGHT_CROP)
        self.surface = pygame.transform.scale(self.front, (TILE_WIDTH, PLAYER_HEIGHT))

        self.running = False
    
    def update(self, window):
        self.move()
        window.blit(self.surface, (self.x, self.y - 16))
        if DEBUG:
            pygame.draw.rect(window, (255, 0, 0), self.boudingBox, 1)

    def move(self):
        if self.x == self.nextX and self.y == self.nextY:
            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_a]:
                self.nextX =  self.x - TILE_WIDTH
                self.surface = pygame.transform.scale(self.left, (TILE_WIDTH, PLAYER_HEIGHT))
            elif keysPressed[pygame.K_d]:
                self.nextX =  self.x + TILE_WIDTH
                self.surface = pygame.transform.scale(self.right, (TILE_WIDTH, PLAYER_HEIGHT))
            elif keysPressed[pygame.K_w]:
                self.nextY = self.y - TILE_WIDTH
                self.surface = pygame.transform.scale(self.back, (TILE_WIDTH, PLAYER_HEIGHT))
            elif keysPressed[pygame.K_s]:
                self.nextY = self.y + TILE_WIDTH
                self.surface = pygame.transform.scale(self.front, (TILE_WIDTH, PLAYER_HEIGHT))
            if keysPressed[pygame.K_k]:
                self.running = True
            else:
                self.running = False
        else:
            if self.running:
                velocity = 4
            else:
                velocity = 2
            if self.x < self.nextX:
                self.x += velocity
                self.boudingBox.move_ip(velocity, 0)
            elif self.x > self.nextX:
                self.x -= velocity
                self.boudingBox.move_ip(-velocity, 0)
            if self.y < self.nextY:
                self.y += velocity
                self.boudingBox.move_ip(0, velocity)
            elif self.y > self.nextY:
                self.y -= velocity
                self.boudingBox.move_ip(0, -velocity)