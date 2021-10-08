import time
from random import randrange
import displayio
from adafruit_matrixportal.matrix import Matrix

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32

matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=3)
display = matrix.display
bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xadaf00
tg = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tg)
display.show(group)

while True:
    bitmap.fill(0)
    for _ in range(100):
        bitmap[randrange(MATRIX_WIDTH), randrange(MATRIX_HEIGHT)] = 1
        time.sleep(0.01)
