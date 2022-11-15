# Raspberry Pi Pico: http://educ8s.tv/part/RaspberryPiPico
# OLED DISPLAY: https://educ8s.tv/part/OLED096

import board, busio, displayio, time
import adafruit_displayio_ssd1306
import adafruit_imageload

IMAGE_FILE = "youtube.bmp"
SPRITE_SIZE = (64, 64)
FRAMES = 28

def invert_colors():
    temp = icon_pal[0]
    icon_pal[0] = icon_pal[1]
    icon_pal[1] = temp

displayio.release_displays()

sda, scl = board.GP0, board.GP1
i2c = busio.I2C(scl, sda)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

group = displayio.Group()

#  load the spritesheet
icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE,
                                                 bitmap=displayio.Bitmap,
                                                 palette=displayio.Palette)
invert_colors()

icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal,
                                 width=1, height=1,
                                 tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0],
                                 default_tile=0,
                                 x=32, y=0)

group.append(icon_grid)

display.show(group)

timer = 0
pointer = 0

while True:
  if (timer + 0.1) < time.monotonic():
    icon_grid[0] = pointer
    pointer += 1
    timer = time.monotonic()
    if pointer > FRAMES-1:
      pointer = 0
