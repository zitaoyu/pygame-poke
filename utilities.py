TILE_WIDTH = 32
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return (self.x, self.y)

class EntitySize:
    def __init__(self, num_of_tile_width, num_of_tile_height):
        self.width = TILE_WIDTH * num_of_tile_width
        self.height = TILE_WIDTH * num_of_tile_height

    def get_size(self):
        return (self.width, self.height)