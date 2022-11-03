from pygame.locals import *
from sound_player import SoundPlayer
from entity import Tile, TileType, Player, TILE_WIDTH
from battlescene import *
import pygame
import json
import time

class OpenWorld:
    def __init__(self):
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
                    self.__add_entity(Tile(x, y, TileType.GROUND))
                elif tile == 1:
                    self.__add_entity(Tile(x, y, TileType.GROUND2))
                elif tile == 2:
                    self.__add_entity(Tile(x, y, TileType.FLOWER))
                elif tile == 3:
                    self.__add_entity(Tile(x, y, TileType.MUSH))
                elif tile == 4:
                    self.__add_entity(Tile(x, y, TileType.GRASS))
                x += TILE_WIDTH
            y += TILE_WIDTH

class Game:

    FPS = 60
    WHITE = (255, 255, 255)
    WIDTH = 640
    HEIGHT = 480
    NAME = "Pokemon Light"

    def __init__(self):
        self.window = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        pygame.display.set_caption(Game.NAME)
        self.open_world = OpenWorld()
        self.player = Player(64, 64)

    def draw_window(self):
        self.window.fill(Game.WHITE)
        for entity in self.open_world.entity_list:
            entity.update(self.window)
        self.player.update(self.window)
        self.check_player_collision()
        pygame.display.update()

    def run(self):
        print("Game lauched.")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(Game.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_window()
        pygame.quit()

    def check_player_collision(self):
        x = self.player.x
        y = self.player.y
        nextX = self.player.nextX
        nextY = self.player.nextY

        if x != nextX or y != nextY:
            collide_tile = None
            for entity in self.open_world.entity_list:
                if entity.x == nextX and entity.y == nextY:
                    collide_tile = entity
                    break
            if collide_tile:
                if collide_tile.tileType == TileType.MUSH:
                    if x < nextX:
                        nextX -= TILE_WIDTH
                    elif x > nextX:
                        nextX += TILE_WIDTH
                    elif y < nextY:
                        nextY -= TILE_WIDTH
                    elif y > nextY:
                        nextY += TILE_WIDTH
                    self.player.nextX = nextX
                    self.player.x = self.player.nextX
                    self.player.nextY = nextY
                    self.player.y = self.player.nextY
                elif collide_tile.tileType == TileType.GRASS:
                    if (int) (time.time()) % 4 == 0:
                        print("Encounter!")

def main():
    Game().run()

if __name__ == "__main__":
    main()