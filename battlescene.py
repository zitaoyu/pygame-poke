import os
import time

import pygame
from pygame.locals import *

from entity import TILE_WIDTH
from game import Game

# temporary
BACKGROUND = pygame.image.load(os.path.join("Assets", "battleBackground.png"))
DIALOGBOX  = pygame.image.load(os.path.join("Assets", "dialogbox.png"))
MON_1      = pygame.image.load(os.path.join("Assets", "bulbasaur.png"))
MON_2      = pygame.image.load(os.path.join("Assets", "charmander.png"))

DIALOGBOX_LOCATION = (0, 360)
MON1_LOCATION = (380, 70)
MON2_LOCATION = (100, 210)


class BattleScene:

    def __init__(self, window, player, opponent_pokemon):
        self.window = window
        # self.pokemon = player.pokemons
        # self.opponent_pokemon = opponent_pokemon
        self.enterBattleScene()
        self.openSceneBox1 = pygame.Rect(0, 0, 640, 240)
        self.openSceneBox2 = pygame.Rect(0, 240, 640, 240)
        self.background = pygame.transform.scale(BACKGROUND.subsurface((0, 0, 240, 112)), (Game.WIDTH, 360))
        self.dialog_box = pygame.transform.scale(DIALOGBOX.subsurface((0, 0, 252, 46)), (Game.WIDTH, 120))

        # pokemons (temporary)
        mon1 = pygame.transform.scale(MON_1, (TILE_WIDTH * 6, TILE_WIDTH * 6))
        self.mon1 = mon1
        mon2 = pygame.transform.scale(MON_2, (TILE_WIDTH * 6, TILE_WIDTH * 6))
        self.mon2 = mon2

    def enterBattleScene(self):
        s = pygame.Surface((640, 60), pygame.SRCALPHA)     # per-pixel alpha
        s.fill((0, 0, 0, 192))                             # notice the alpha value in the color
        l = [0, 7, 3, 5, 1, 6, 2, 4]
        for i in range(3):
            for j in l:
                self.window.blit(s, (0, j * 60))
                pygame.display.update()
                time.sleep(0.05)

    def drawWindow(self):
        self.window.fill(Game.WHITE)
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.dialog_box, DIALOGBOX_LOCATION)
        self.window.blit(self.mon1, MON1_LOCATION)
        self.window.blit(self.mon2, MON2_LOCATION)
        # entering battle scene
        if self.openSceneBox1 != None and self.openSceneBox2 != None:
            self.openSceneBox1.move_ip(0, -1)
            self.openSceneBox2.move_ip(0, 1)
            pygame.draw.rect(self.window, (0, 0, 0), self.openSceneBox1)
            pygame.draw.rect(self.window, (0, 0, 0), self.openSceneBox2)
            if self.openSceneBox1.y <= - Game.HEIGHT / 2:
                self.openSceneBox1 = None
            if self.openSceneBox2.y >= Game.HEIGHT:
                self.openSceneBox2 = None
        pygame.display.update()