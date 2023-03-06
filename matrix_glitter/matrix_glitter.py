import time
from random import randrange
import displayio
from adafruit_matrixportal.matrix import Matrix

SCALE = 2
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
BMP_WIDTH = MATRIX_WIDTH // SCALE
BMP_HEIGHT = MATRIX_HEIGHT // SCALE
COLOR_STEPS = 16
UPDATE_RATE = 0
CYCLES = 10 * COLOR_STEPS

matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=6)
display = matrix.display

bitmap = displayio.Bitmap(BMP_WIDTH, BMP_HEIGHT, COLOR_STEPS)
palette = displayio.Palette(COLOR_STEPS)
for i, c in enumerate(range(0, 0xFF, COLOR_STEPS)):
    palette[i] = 0xFF | c << 8
tg = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=SCALE)
group.append(tg)
display.show(group)

incrementer = [None]*(BMP_WIDTH*BMP_HEIGHT)

def init_matrix():
    display.auto_refresh = False
    for x in range(BMP_WIDTH):
        for y in range(BMP_HEIGHT):
            bitmap[x, y] = randrange(COLOR_STEPS)
            if bitmap[x, y] == 0:
                incrementer[x*BMP_HEIGHT + y] = -1
            else:
                incrementer[x*BMP_HEIGHT + y] = 1
    display.auto_refresh = True

while True:
    init_matrix()
    for _ in range(CYCLES):
        display.auto_refresh = False
        for x in range(BMP_WIDTH):
            for y in range(BMP_HEIGHT):
                if bitmap[x, y] in (0, COLOR_STEPS-1):
                    incrementer[x*BMP_HEIGHT + y] *= -1
                bitmap[x, y] += incrementer[x*BMP_HEIGHT + y]
        display.auto_refresh = True
        time.sleep(UPDATE_RATE)
