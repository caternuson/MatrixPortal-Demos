import time
import random
import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix

#--| User Config |-----------------------------------------
# matrix setup
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
# sprite setup
SPRITE_FILE = 'rain_sprite.bmp'
SPRITE_WIDTH = 2
SPRITE_HEIGHT = 3
# animation setup
DROP_COLOR = 0xADAF00
TAIL_COLOR = 0x00FF00
MAX_DROPS = 40
TAIL_SIZE = 10
FALL_RATE = 0.01
MAX_STEPS = 5
GAMMA = 0.1
#----------------------------------------------------------

FADE_STEPS = SPRITE_HEIGHT * TAIL_SIZE

# create matrix
matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=6)
display = matrix.display

# create groups
drops = displayio.Group()         # these fall and change sprite
tails = displayio.Group()         # these fade and disappear
main_group = displayio.Group()    # holds the drops and tails
main_group.append(tails)
main_group.append(drops)
display.show(main_group)

# load sprite sheet
sprite_sheet, _ = adafruit_imageload.load(SPRITE_FILE)
SPRITE_COUNT = sprite_sheet.width // SPRITE_WIDTH * sprite_sheet.height // SPRITE_HEIGHT

# palette for drop
drop_palette = displayio.Palette(2)
drop_palette[0] = 0x000000
drop_palette[1] = DROP_COLOR
drop_palette.make_transparent(0)

# palettes for fading tails
tail_palette = []
r = TAIL_COLOR >> 16 & 0xFF
g = TAIL_COLOR >> 8 & 0xFF
b = TAIL_COLOR & 0xFF
for fade_step in range(FADE_STEPS):
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = (round(r * (1 - (fade_step/FADE_STEPS)**GAMMA)),
                  round(g * (1 - (fade_step/FADE_STEPS)**GAMMA)),
                  round(b * (1 - (fade_step/FADE_STEPS)**GAMMA)))
    palette.make_transparent(0)
    tail_palette.append(palette)

def make_sprite(tile=random.randrange(SPRITE_COUNT), palette=drop_palette, x=0, y=0):
    '''Return a sprite from the sprite sheet.'''
    return displayio.TileGrid(sprite_sheet,
                            pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = SPRITE_WIDTH,
                            tile_height = SPRITE_HEIGHT,
                            default_tile = tile,
                            x = x,
                            y = y)

def update_drops():
    '''Move all the drop sprites.'''
    for drop in drops:
        drop.y += 1
        # if off screen, destroy
        if drop.y > MATRIX_HEIGHT + SPRITE_HEIGHT:
            drops.remove(drop)
            continue
        # if moved SPRITE_HEIGHT, add to tail
        if not drop.y % SPRITE_HEIGHT:
            tails.append(make_sprite(drop[0], tail_palette[0], drop.x, drop.y))
        # change the sprite
        drop[0] = random.randrange(SPRITE_COUNT)

def update_tails():
    '''Fade all the tail sprites.'''
    for tail in tails:
        current = tail_palette.index(tail.pixel_shader)
        # if done fading, destroy
        if current == FADE_STEPS - 1:
            tails.remove(tail)
            continue
        # next fade step
        tail.pixel_shader = tail_palette[current+1]

#====================
# MAIN LOOP
#====================
while True:
    # if there's room, add new drop
    if len(drops) < MAX_DROPS:
        new_drop = make_sprite(y=-SPRITE_HEIGHT, x=random.randrange(MATRIX_WIDTH))
        drops.append(new_drop)
    # fall a random number of steps
    for _ in range(random.randrange(MAX_STEPS)):
        display.auto_refresh = False
        update_drops()
        update_tails()
        display.auto_refresh = True
        time.sleep(FALL_RATE)
