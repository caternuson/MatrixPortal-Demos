# simple Jacob's Ladder simulator
# written a long time ago by T.C. Broonsie
import time
import random
import displayio
from adafruit_matrixportal.matrix import Matrix

#--| User Config |-----------------------------------------
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
BACK_COLOR = 0x000000
BOLT_COLOR = 0xFFFFFF
BOLT_WIDTH = 5
DELAY = 0.05
#----------------------------------------------------------

# create matrix
matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=6)
display = matrix.display

# create group
splash = displayio.Group()
display.show(splash)

# create bitmap
bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, 2)
palette = displayio.Palette(2)
palette[0] = BACK_COLOR
palette[1] = BOLT_COLOR

# create tile grid
tg = displayio.TileGrid(bitmap, pixel_shader=palette)
splash.append(tg)

def draw_bolt(location):
    '''Draw random zig-zag bolt across display.'''
    x = location
    if random.choice([True, False]):
        # left to right
        y_range = range(0, MATRIX_HEIGHT)
    else:
        # right to left
        y_range = range(MATRIX_HEIGHT - 1, -1, -1)
    for y in y_range:
        try:
            bitmap[x, y] = 1
        except:
            # just don't draw it
            pass
        dx = x - location
        if abs(dx) < BOLT_WIDTH:
            # if we have room, move random direction
            x += random.choice([-1,1])
        else:
            # otherwise, force back toward center
            x += 1 if dx < 0 else -1

# loop forever
while True:
    # start at bottom
    xpos = 0
    # loop until we receach the top
    while xpos < MATRIX_WIDTH:
        # update display
        display.auto_refresh = False
        bitmap.fill(0)
        draw_bolt(xpos)
        display.auto_refresh = True
        # move up random amount
        xpos += random.randrange(BOLT_WIDTH)
        # zzzzzzz
        time.sleep(DELAY)
