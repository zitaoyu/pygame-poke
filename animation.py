from util import *
from pygame import Surface


class Animation:
    def __init__(self, sprite: Surface, x=0, y=0, x_2=0, y_2=0, num_of_frames=1, padding=0,
                 frame_interval_by_sec=0.5, horizontal=True):
        self.sprite_list = []
        if x == 0 and y == 0 and x_2 == 0 and y_2 == 0:
            self.sprite_list.append(sprite)
        else:
            x_increment = 0
            y_increment = 0
            for i in range(num_of_frames):
                self.sprite_list.append(sprite.subsurface(x + x_increment, y + y_increment, x_2, y_2))
                if horizontal:
                    x_increment += x_2
                else:
                    y_increment += y_2
        self.frame_interval = int(frame_interval_by_sec * FPS)
        self.frame_count = 0
        self.sprite = self.sprite_list[0]

    def scale_sprites(self, width, height):
        for i in range(len(self.sprite_list)):
            self.sprite_list[i] = pygame.transform.scale(self.sprite_list[i], (width, height))

    def get_sprite(self):
        if len(self.sprite_list) == 1:
            return self.sprite_list[0]
        self.frame_count += 1
        index = self.frame_count // self.frame_interval % len(self.sprite_list)
        self.sprite = self.sprite_list[index]
        return self.sprite
