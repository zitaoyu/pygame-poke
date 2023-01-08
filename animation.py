# from game import FPS

HALF_SEC_INTERVAL = 60 // 2

class Animation:
    def __init__(self, sprite_list, frame_interval=None):
        self.sprite_list = sprite_list
        self.frame_interval = frame_interval
        self.frame_count = 0
        self.sprite = sprite_list[0]

    def get_sprite(self):
        if len(self.sprite_list) == 1:
            return self.sprite_list[0]
        self.frame_count += 1
        index = self.frame_count // self.frame_interval % len(self.sprite_list)
        self.sprite = self.sprite_list[index]
        return self.sprite