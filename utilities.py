FPS = 60
TILE_WIDTH = 32
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GAME_WINDOW_WIDTH = 640
GAME_WINDOW_HEIGHT = 480
GAME_NAME = "PyEmerald"

def find_lowest_pixel_in_transparent_image(image_path):
    import numpy as np
    from PIL import Image
    img = Image.open(image_path)
    img = img.convert("RGBA")
    arr = np.array(img)
    for row_num in range(len(arr) - 1, 0, -1):
        for pixel in arr[row_num]:
            if any(pixel):
                return row_num
    return -1