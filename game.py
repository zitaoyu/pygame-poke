import pygame
from pygame.locals import *

from battlescene import *
from entity import *
from openworld import *
from battlescene import *

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.player = Player()
        # self.open_world = OpenWorld(self.window, self.player)
        self.battle_scene = BattleScene(self.window, self.player, None)

    def draw_window(self):
        # self.open_world.draw_entity_list()
        self.battle_scene.draw_entity_list()
        pygame.display.update()

    def run(self):
        print("Game lauched.")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_window()
        pygame.quit()

def main():
    Game().run()

if __name__ == "__main__":
    main()