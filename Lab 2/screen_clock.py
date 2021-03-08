import time
import math
import random
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from datetime import datetime as dt
from datetime import date, timedelta

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
font1 = ImageFont.truetype("zawijasy.otf", 30)
font2 = ImageFont.truetype("BEECH___.TTF", 80)
font3 = ImageFont.truetype("CheerfulYellow.ttf", 30)
#font4 = ImageFont.truetype("Kind and Rich - Personal Use.otf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    if buttonA.value and buttonB.value:
        d = dt.now(tz=None)
        fri = 4 - d.weekday()
        time_change = timedelta(days=fri)
        now = dt.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        time_change_2 = timedelta(seconds=seconds_since_midnight)
        next_friday = time_change + d - time_change_2
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
        DATE = strftime("%m/%d/%Y %H:%M:%S")
        s0 = str(fri) + " days"
        s1 = str(math.trunc((next_friday - d).total_seconds()/60)) + " m"
        s2 = str(math.trunc((next_friday - d).total_seconds())) + " s"
    
        y = top
        draw.text((x, y), DATE, font=font, fill="#fab300")

        y += font.getsize(DATE)[1]
        y += font.getsize(DATE)[1]
        draw.text((x, y), "Days to Friday: ", font=font, fill="#fc7200")

        y += font.getsize(DATE)[1]
        draw.text((x, y), s0, font=font, fill="#eb4034")

        # y += font.getsize(DATE)[1]
        # draw.text((x, y), "Minutes to Friday: ", font=font, fill="#fc7200")
    
        # y += font.getsize(s0)[1]
        # draw.text((x, y), s1, font=font, fill="#fc7200")
        y += font.getsize(DATE)[1]
        draw.text((x, y), "Seconds to Friday: ", font=font, fill="#fc7200")
    
        y += font.getsize(s1)[1]
        draw.text((x, y), s2, font=font, fill="#eb4034")

    
        # Display image.
        disp.image(image, rotation)
        time.sleep(1)

    else:
        if buttonB.value and not buttonA.value:
            tasks = ["Cook Some Food!", "Go Hiking!", "Go Shopping!", "Watch a Movie!", "Watch YouTube!", "Read a book!", "Take a Nap!"]
            colors = ["#eb4034", "#ff7700", "#fffb00", "#bbff00", "#00ff84", "#00f7ff", "#ff00e6"]
            ri = random.randint(0,6)
            ri_2 = random.randint(0,6)

            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            y = top
            draw.text((x+15, y), "Random Tasks!", font=font1, fill=colors[random.randint(0,6)])
            y = top + 50
            draw.text((x+15, y), tasks[ri], font=font3, fill=colors[random.randint(0,6)])
            disp.image(image, rotation)
            time.sleep(1)
        if buttonA.value and not buttonB.value:
            ri_2 = random.randint(0,6)
            colors = ["#eb4034", "#ff7700", "#fffb00", "#bbff00", "#00ff84", "#00f7ff", "#ff00e6"]
            ri_3 = random.randint(1,6)

            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            y = top
            draw.text((x, y), "Roll Dice!", font=font3, fill=colors[random.randint(0,6)])
            y = top + 50
            draw.text((x+100, y), str(ri_3), font=font2, fill=colors[random.randint(0,6)])
            disp.image(image, rotation)
            time.sleep(1)

            
