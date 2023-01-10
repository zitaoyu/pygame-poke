import os
import time

import pygame
from pygame.locals import *

from entity import *
from pokemon import *
from sound_player import SoundPlayer


# temporary
BACKGROUND = pygame.image.load(os.path.join("assets", "battleBackground.png"))
DIALOGBOX  = pygame.image.load(os.path.join("assets", "dialogbox.png"))
MON_1      = pygame.image.load(os.path.join("assets/pokemon", "10195_front.png"))
MON_2      = pygame.image.load(os.path.join("assets/pokemon", "10195_back.png"))

DIALOGBOX_LOCATION = (0, 360)
MY_POKEMON_LOCATION = (368, 80)
OPPONENT_POKEMON_LOCATION = (64, 192)

class BattleScene:

    def __init__(self, window, my_pokemon_party: PokemonParty, opponent_pokemon_party: PokemonParty):
        self.window = window
        self.my_pokemon_party = my_pokemon_party
        self.opponent_pokemon_party = opponent_pokemon_party
        self.enter_battle_scene()

        self.my_battling_pokemon: Pokemon = self.my_pokemon_party.get_leading_pokemon()
        self.opponent_battling_pokemon: Pokemon = self.opponent_pokemon_party.get_leading_pokemon()

        MON_1 = pygame.image.load(os.path.join("assets/pokemon", str(self.my_battling_pokemon.id) + "_front.png"))
        MON_2 = pygame.image.load(os.path.join("assets/pokemon", str(self.opponent_battling_pokemon.id) + "_back.png"))
        mon1 = pygame.transform.scale(MON_1, (TILE_WIDTH * 6, TILE_WIDTH * 6))
        self.mon1 = mon1
        mon2 = pygame.transform.scale(MON_2, (TILE_WIDTH * 8, TILE_WIDTH * 8))
        self.mon2 = mon2

        self.sound_player = SoundPlayer()
        self.sound_player.play_track('./sounds/battle.mp3')

    def enter_battle_scene(self):
        s = pygame.Surface((640, 60), pygame.SRCALPHA)     # per-pixel alpha
        s.fill((0, 0, 0, 192))                             # notice the alpha value in the color
        l = [0, 7, 3, 5, 1, 6, 2, 4]
        for i in range(3):
            for j in l:
                self.window.blit(s, (0, j * 60))
                pygame.display.update()
                time.sleep(0.05)
        self.openSceneBox1 = pygame.Rect(0, 0, 640, 240)
        self.openSceneBox2 = pygame.Rect(0, 240, 640, 240)
        self.background = pygame.transform.scale(BACKGROUND.subsurface((0, 0, 240, 112)), (GAME_WINDOW_WIDTH, 360))
        self.dialog_box = pygame.transform.scale(DIALOGBOX.subsurface((0, 0, 252, 46)), (GAME_WINDOW_WIDTH, 120))

    def draw_entity_list(self):
        self.window.fill(WHITE)
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.mon1, MY_POKEMON_LOCATION)
        self.window.blit(self.mon2, OPPONENT_POKEMON_LOCATION)
        self.window.blit(self.dialog_box, DIALOGBOX_LOCATION)
        # entering battle scene
        if self.openSceneBox1 != None and self.openSceneBox2 != None:
            self.openSceneBox1.move_ip(0, -1)
            self.openSceneBox2.move_ip(0, 1)
            pygame.draw.rect(self.window, (0, 0, 0), self.openSceneBox1)
            pygame.draw.rect(self.window, (0, 0, 0), self.openSceneBox2)
            if self.openSceneBox1.y <= - GAME_WINDOW_HEIGHT / 2:
                self.openSceneBox1 = None
            if self.openSceneBox2.y >= GAME_WINDOW_HEIGHT:
                self.openSceneBox2 = None
        pygame.display.update()