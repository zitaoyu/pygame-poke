import os
import time

from pygame.locals import *
from entity import *
from battle_manager import *


# pygame surfaces
PATH = './assets/battle'
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(PATH + "/battlebacks", "grass_field_battleback_day.png")), (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
DIALOG_BOX_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "transparent_dialog_background.png")), (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT / 4 + 20))

DIALOG_BOX_IMAGE = pygame.image.load(os.path.join(PATH, "transparent_dialog_box.png"))
DIALOG_BOX  = pygame.transform.scale(DIALOG_BOX_IMAGE, (GAME_WINDOW_WIDTH, 92))
DIALOG_BOX_MAIN_MENU = pygame.transform.scale(DIALOG_BOX_IMAGE, (GAME_WINDOW_WIDTH - 260, 92))
CURSOR_COMMAND_IMAGE    = pygame.image.load(os.path.join(PATH, "cursor_command.png"))
FIGHT_COMMAND = CURSOR_COMMAND_IMAGE.subsurface(0, 0, 129, 45)
FIGHT_COMMAND           = CURSOR_COMMAND_IMAGE.subsurface(0, 0, 129, 45)
FIGHT_COMMAND_SELECT    = CURSOR_COMMAND_IMAGE.subsurface(130, 0, 129, 45)
POKEMON_COMMAND         = CURSOR_COMMAND_IMAGE.subsurface(0, 46, 129, 45)
POKEMON_COMMAND_SELECT  = CURSOR_COMMAND_IMAGE.subsurface(130, 46, 129, 45)
BAG_COMMAND             = CURSOR_COMMAND_IMAGE.subsurface(0, 92, 129, 45)
BAG_COMMAND_SELECT      = CURSOR_COMMAND_IMAGE.subsurface(130, 92, 129, 45)
RUN_COMMAND             = CURSOR_COMMAND_IMAGE.subsurface(0, 138, 129, 45)
RUN_COMMAND_SELECT      = CURSOR_COMMAND_IMAGE.subsurface(130, 138, 129, 45)

FIGHT_MENU = pygame.transform.scale(pygame.image.load(os.path.join(PATH, "overlay_fight.png")), (GAME_WINDOW_WIDTH, 92))
MOVE_BUTTON_IMAGE = pygame.image.load(os.path.join(PATH, "cursor_fight.png"))
MOVE_BUTTON_GHOST           = MOVE_BUTTON_IMAGE.subsurface(0, 0, 191, 47)
MOVE_BUTTON_GHOST_SELECT    = MOVE_BUTTON_IMAGE.subsurface(192, 0, 191, 47)
MOVE_BUTTON_FIGHTING        = MOVE_BUTTON_IMAGE.subsurface(0, 46, 191, 47)
MOVE_BUTTON_FIGHTING_SELECT = MOVE_BUTTON_IMAGE.subsurface(192, 46, 191, 47)
MOVE_BUTTON_WATER           = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 2, 191, 47)
MOVE_BUTTON_WATER_SELECT    = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 2, 191, 47)
MOVE_BUTTON_POISON          = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 3, 191, 47)
MOVE_BUTTON_POISON_SELECT   = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 3, 191, 47)
MOVE_BUTTON_ROCK            = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 4, 191, 47)
MOVE_BUTTON_ROCK_SELECT     = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 4, 191, 47)
MOVE_BUTTON_GROUND          = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 5, 191, 47)
MOVE_BUTTON_GROUND_SELECT   = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 5, 191, 47)
MOVE_BUTTON_BUG             = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 6, 191, 47)
MOVE_BUTTON_BUG_SELECT      = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 6, 191, 47)
MOVE_BUTTON_PHYCHIC         = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 7, 191, 47)
MOVE_BUTTON_PHYCHIC_SELECT  = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 7, 191, 47)
MOVE_BUTTON_NORMAL          = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 8, 191, 47)
MOVE_BUTTON_NORMAL_SELECT   = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 8, 191, 47)
MOVE_BUTTON_STEEL           = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 9, 191, 47)
MOVE_BUTTON_STEEL_SELECT    = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 9, 191, 47)
MOVE_BUTTON_FIRE            = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 10, 191, 47)
MOVE_BUTTON_FIRE_SELECT     = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 10, 191, 47)
MOVE_BUTTON_FLYING          = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 11, 191, 47)
MOVE_BUTTON_FLYING_SELECT   = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 11, 191, 47)
MOVE_BUTTON_GRASS           = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 12, 191, 47)
MOVE_BUTTON_GRASS_SELECT    = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 12, 191, 47)
MOVE_BUTTON_ELECTRIC        = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 13, 191, 47)
MOVE_BUTTON_ELECTRIC_SELECT = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 13, 191, 47)
MOVE_BUTTON_ICE             = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 14, 191, 47)
MOVE_BUTTON_ICE_SELECT      = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 14, 191, 47)
MOVE_BUTTON_DRAGON          = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 14, 191, 47)
MOVE_BUTTON_DRAGON_SELECT   = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 14, 191, 47)
MOVE_BUTTON_DARK            = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 14, 191, 47)
MOVE_BUTTON_DARK_SELECT     = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 14, 191, 47)
MOVE_BUTTON_FAIRY           = MOVE_BUTTON_IMAGE.subsurface(0, 46 * 14, 191, 47)
MOVE_BUTTON_FAIRY_SELECT    = MOVE_BUTTON_IMAGE.subsurface(192, 46 * 14, 191, 47)

DATABOX = pygame.image.load(os.path.join(PATH, "databox_normal.png"))
OPPONENT_DATABOX = pygame.image.load(os.path.join(PATH, "databox_normal_foe.png"))

# coordnates
DIALOG_BOX_BACKGROUND_COORDINATES = (0, GAME_WINDOW_HEIGHT - 112)
DIALOG_BOX_COORDINATES = (0, GAME_WINDOW_HEIGHT - 92)
FIGHT_COMMAND_COORDINATES   = (GAME_WINDOW_WIDTH - 260, GAME_WINDOW_HEIGHT - 92)
BAG_COMMAND_COORDINATES     = (GAME_WINDOW_WIDTH - 130, GAME_WINDOW_HEIGHT - 92)
POKEMON_COMMAND_COORDINATES = (GAME_WINDOW_WIDTH - 260, GAME_WINDOW_HEIGHT - 46)
RUN_COMMAND_COORDINATES     = (GAME_WINDOW_WIDTH - 130, GAME_WINDOW_HEIGHT - 46)
OPPONENT_POKEMON_COORDINATES = (372, 220)
MY_POKEMON_COORDINATES = (40, 192)
DATABOX_COORDINATES = (GAME_WINDOW_WIDTH - DATABOX.get_width(), 280)
OPPONENT_DATABOX_COORDINATES = (0, 110)
MOVE_1_COORDINATES = (0, GAME_WINDOW_HEIGHT - 92)
MOVE_2_COORDINATES = (241, GAME_WINDOW_HEIGHT - 92)
MOVE_3_COORDINATES = (0, GAME_WINDOW_HEIGHT - 46)
MOVE_4_COORDINATES = (241, GAME_WINDOW_HEIGHT - 46)
MOVE_1_NAME_COORDINATES = (50, GAME_WINDOW_HEIGHT - 102)
MOVE_2_NAME_COORDINATES = (291, GAME_WINDOW_HEIGHT - 102)
MOVE_3_NAME_COORDINATES = (0, GAME_WINDOW_HEIGHT - 46)
MOVE_4_NAME_COORDINATES = (241, GAME_WINDOW_HEIGHT - 46)

Font = pygame.font.Font('./assets/fonts/power green.ttf', 24)

def get_move_button(type: Type, is_select: bool):
    if type == Type.GHOST:
        if is_select:
            return MOVE_BUTTON_GHOST_SELECT
        else:
            return MOVE_BUTTON_GHOST
    elif type == Type.FIGHTING:
        if is_select:
            return MOVE_BUTTON_FIGHTING_SELECT
        else:
            return MOVE_BUTTON_FIGHTING
    elif type == Type.WATER:
        if is_select:
            return MOVE_BUTTON_WATER_SELECT
        else:
            return MOVE_BUTTON_WATER
    elif type == Type.POISON:
        if is_select:
            return MOVE_BUTTON_POISON_SELECT
        else:
            return MOVE_BUTTON_POISON
    elif type == Type.ROCK:
        if is_select:
            return MOVE_BUTTON_ROCK_SELECT
        else:
            return MOVE_BUTTON_ROCK
    elif type == Type.GROUND:
        if is_select:
            return MOVE_BUTTON_GROUND_SELECT
        else:
            return MOVE_BUTTON_GROUND
    elif type == Type.BUG:
        if is_select:
            return MOVE_BUTTON_BUG_SELECT
        else:
            return MOVE_BUTTON_BUG
    elif type == Type.PSYCHIC:
        if is_select:
            return MOVE_BUTTON_PHYCHIC_SELECT
        else:
            return MOVE_BUTTON_PHYCHIC
    elif type == Type.NORMAL:
        if is_select:
            return MOVE_BUTTON_NORMAL_SELECT
        else:
            return MOVE_BUTTON_NORMAL
    elif type == Type.STEEL:
        if is_select:
            return MOVE_BUTTON_STEEL_SELECT
        else:
            return MOVE_BUTTON_STEEL
    elif type == Type.FIRE:
        if is_select:
            return MOVE_BUTTON_FIRE_SELECT
        else:
            return MOVE_BUTTON_FIRE
    elif type == Type.FLYING:
        if is_select:
            return MOVE_BUTTON_FLYING_SELECT
        else:
            return MOVE_BUTTON_FLYING
    elif type == Type.GRASS:
        if is_select:
            return MOVE_BUTTON_GRASS_SELECT
        else:
            return MOVE_BUTTON_GRASS
    elif type == Type.ELECTRIC:
        if is_select:
            return MOVE_BUTTON_ELECTRIC_SELECT
        else:
            return MOVE_BUTTON_ELECTRIC
    elif type == Type.DRAGON:
        if is_select:
            return MOVE_BUTTON_DRAGON_SELECT
        else:
            return MOVE_BUTTON_DRAGON
    elif type == Type.DARK:
        if is_select:
            return MOVE_BUTTON_DARK_SELECT
        else:
            return MOVE_BUTTON_DARK
    elif type == Type.FAIRY:
        if is_select:
            return MOVE_BUTTON_FAIRY_SELECT
        else:
            return MOVE_BUTTON_FAIRY

class Menu(Enum):
    MAIN = "main"
    FIGHT = "fight"
    BAG = "bag"
    POKEMON = "pokemon"

class BattleScene:

    def __init__(self, window: Surface, battle_manager: BattleManager):
        self.window = window
        self.battle_manager = battle_manager
        self.menu: Menu = Menu.MAIN
        self.menu_select = 0
        self.move_select = 0
        self.move_size = self.battle_manager.my_battling_pokemon.move_set.get_size()
        self.background = BACKGROUND
        self.input_cooldown = 0
        # self._enter_battle_scene()
        self.open_scene = False
        self.__update_battling_pokemons_sprites()
        self.sound_player = SoundPlayer()
        self.sound_player.play_track('./sounds/battle.mp3')

    def __update_battling_pokemons_sprites(self):
        my_battling_pokemon_sprite_path = os.path.join("assets/pokemon", str(self.battle_manager.my_battling_pokemon.id) + "_back.png")
        opponent_battling_pokemon_sprite_path = os.path.join("assets/pokemon", str(self.battle_manager.opponent_battling_pokemon.id) + "_front.png")
        surface_1 = pygame.image.load(my_battling_pokemon_sprite_path)
        surface_2 = pygame.image.load(opponent_battling_pokemon_sprite_path)
        self.my_battling_pokemon_sprite = pygame.transform.scale(surface_1, (TILE_WIDTH * 8, TILE_WIDTH * 8))
        self.opponent_battling_pokemon_sprite = pygame.transform.scale(surface_2, (TILE_WIDTH * 6, TILE_WIDTH * 6))

        offset = find_lowest_pixel_in_transparent_image(opponent_battling_pokemon_sprite_path)
        self.opponent_battling_pokemon_sprite_coordinates = (372, 220 - offset * 2)


        
    def __check_input(self):
        inputs = check_input()
        old_menu = self.menu
        old_select = self.menu_select
        old_select_move = self.move_select
        if len(inputs) > 0:
            input = inputs[0]
            if self.menu == Menu.MAIN:
                    if self.menu_select == 0:
                        if input == INPUT.SELECT:
                            self.menu = Menu.FIGHT
                            self.move_select = 0
                        elif input == INPUT.RIGHT:
                            self.menu_select = 1
                        elif input == INPUT.DOWN and self.move_size >= 3:
                            self.menu_select = 2
                    elif self.menu_select == 1:
                        if input == INPUT.SELECT:
                            self.menu = Menu.BAG
                        elif input == INPUT.LEFT:
                            self.menu_select = 0
                        elif input == INPUT.DOWN and self.move_size == 4:
                            self.menu_select = 3
                    elif self.menu_select == 2:
                        if input == INPUT.SELECT:
                            self.menu = Menu.POKEMON
                        elif input == INPUT.RIGHT and self.move_size == 4:
                            self.menu_select = 3
                        elif input == INPUT.UP:
                            self.menu_select = 0
                    elif self.menu_select == 3:
                        if input == INPUT.SELECT:
                            # run
                            pass
                        elif input == INPUT.LEFT:
                            self.menu_select = 2
                        elif input == INPUT.UP:
                            self.menu_select = 1
            elif self.menu == Menu.FIGHT:
                if input == INPUT.LEFT:
                    if self.move_select == 1:
                        self.move_select = 0
                    elif self.move_select == 3:
                        self.move_select = 2
                elif input == INPUT.RIGHT:
                    if self.move_select == 0 and self.move_size >= 2:
                        self.move_select = 1
                    elif self.move_select == 2 and self.move_size == 4:
                        self.move_select = 3
                elif input == INPUT.UP:
                    if self.move_select == 2:
                        self.move_select = 0
                    elif self.move_select == 3:
                        self.move_select = 1
                elif input == INPUT.DOWN:
                    if self.move_select == 0 and self.move_size >= 3:
                        self.move_select = 2
                    elif self.move_select == 1 and self.move_size == 4:
                        self.move_select = 3
                elif input == INPUT.SELECT:
                    self.battle_manager.my_battling_pokemon_use_move(self.move_select)
                    self.input_cooldown = 10
                elif input == INPUT.BACK:
                    self.menu = Menu.MAIN
                    self.input_cooldown = 10
        
        if old_menu != self.menu or old_select != self.menu_select or old_select_move != self.move_select:
                self.input_cooldown = 10

    def _enter_battle_scene(self):
        s = pygame.Surface((640, 60), pygame.SRCALPHA)     # per-pixel alpha
        s.fill((0, 0, 0, 192))                             # notice the alpha value in the color
        l = [0, 7, 3, 5, 1, 6, 2, 4]
        for i in range(3):
            for j in l:
                self.window.blit(s, (0, j * 60))
                pygame.display.update()
                time.sleep(0.05)
        self.open_scene_box_1 = pygame.Rect(0, 0, 640, 240)
        self.open_scene_box_2 = pygame.Rect(0, 240, 640, 240)

    def draw_entity_list(self):
        self.window.fill(WHITE)
        # background:
        self.window.blit(self.background, (0, 0))
        # pokemon sprites:
        self.window.blit(self.my_battling_pokemon_sprite, MY_POKEMON_COORDINATES)
        self.window.blit(self.opponent_battling_pokemon_sprite, self.opponent_battling_pokemon_sprite_coordinates)
        # data box:
        self.window.blit(DATABOX, DATABOX_COORDINATES)
        self.window.blit(OPPONENT_DATABOX, OPPONENT_DATABOX_COORDINATES)
        # menu:
        self.window.blit(DIALOG_BOX_BACKGROUND, DIALOG_BOX_BACKGROUND_COORDINATES)
        self.input_cooldown -= 1
        if self.input_cooldown < 0:
            self.__check_input()
        if self.menu == Menu.MAIN:
            self.window.blit(DIALOG_BOX_MAIN_MENU, DIALOG_BOX_COORDINATES)
            self.window.blit(FIGHT_COMMAND, FIGHT_COMMAND_COORDINATES)
            self.window.blit(BAG_COMMAND, BAG_COMMAND_COORDINATES)
            self.window.blit(POKEMON_COMMAND, POKEMON_COMMAND_COORDINATES)
            self.window.blit(RUN_COMMAND, RUN_COMMAND_COORDINATES)
            if self.menu_select == 0:
                self.window.blit(FIGHT_COMMAND_SELECT, FIGHT_COMMAND_COORDINATES)
            elif self.menu_select == 1:
                self.window.blit(BAG_COMMAND_SELECT, BAG_COMMAND_COORDINATES)
            elif self.menu_select == 2:
                self.window.blit(POKEMON_COMMAND_SELECT, POKEMON_COMMAND_COORDINATES)
            elif self.menu_select == 3:
                self.window.blit(RUN_COMMAND_SELECT, RUN_COMMAND_COORDINATES)
        elif self.menu == Menu.FIGHT:
            self.window.blit(FIGHT_MENU, DIALOG_BOX_COORDINATES)

            move_set = self.battle_manager.my_battling_pokemon.move_set
            for i in range(4):
                move = move_set.get_move_with_index(i)
                if move != None:
                    name = Font.render(move.name, False, (0, 0, 0))
                    coordinates = MOVE_1_COORDINATES
                    move_button = get_move_button(move.type, i == self.move_select)
                    MOVE_BUTTON_GHOST
                    if i == 1:
                        coordinates = MOVE_2_COORDINATES
                    elif i == 2:
                        coordinates = MOVE_3_COORDINATES
                    elif i == 3:
                        coordinates = MOVE_4_COORDINATES
                    self.window.blit(pygame.transform.scale(move_button, (241, 46)), coordinates)
                    self.window.blit(name, (int(coordinates[0]) + 40, int(coordinates[1]) + 5))
        elif self.menu == Menu.BAG:
            pass

        # entering battle scene
        if self.open_scene:
            self.open_scene_box_1.move_ip(0, -1)
            self.open_scene_box_2.move_ip(0, 1)
            pygame.draw.rect(self.window, (0, 0, 0), self.open_scene_box_1)
            pygame.draw.rect(self.window, (0, 0, 0), self.open_scene_box_2)
            if self.open_scene_box_1.y <= - GAME_WINDOW_HEIGHT / 2:
                self.open_scene = False
        pygame.display.update()

def draw_pokemon_sprite_bounding_box():
    # opponent_pokemon_box = pygame.Surface((TILE_WIDTH * 8, TILE_WIDTH * 8), pygame.SRCALPHA)
    # opponent_pokemon_box.fill((0, 0, 0, 192))
    # self.window.blit(opponent_pokemon_box, MY_POKEMON_COORDINATES)
    pass