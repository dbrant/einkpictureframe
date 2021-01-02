#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'waveshare/python/lib')
if os.path.exists(libpath):
    sys.path.append(libpath)

import logging
import datetime
import random
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

epd = epd7in5_V2.EPD()

imageList = [ 'db1.jpg', 'bissel3.jpg', 'db2.jpg', 'bissel2.jpg' ]

totalWidth = 800
totalHeight = 480
clockWidth = 320
clockHeight = 150
phase = 0

try:
    logging.info("Initializing...")
    epd.init()

    #millis = int(round(time.time() * 1000))
    #logging.info("Clearing...")
    #epd.Clear()
    #logging.info("That took " + str(int(round(time.time() * 1000)) - millis) + " ms")

    while True:
        logging.info("Loading next image...")

        imageName = random.choice(imageList)

        now = datetime.datetime.now()
        img = Image.open(os.path.join(imagepath, imageName))

        draw = ImageDraw.Draw(img)
        clockFont = ImageFont.truetype('agenda.ttf', 128)
        clockText = now.strftime("%H:%M")

        if phase == 0:
            draw.rectangle((0, 0, clockWidth, clockHeight), fill = 'white')
            draw.text((24, 0), clockText, font = clockFont, fill = 0)
        elif phase == 1:
            draw.rectangle((totalWidth - clockWidth, 0, totalWidth, clockHeight), fill = 'white')
            draw.text((totalWidth - clockWidth + 24, 0), clockText, font = clockFont, fill = 0)
        elif phase == 2:
            draw.rectangle((0, totalHeight - clockHeight, clockWidth, totalHeight), fill = 'white')
            draw.text((24, totalHeight - clockHeight), clockText, font = clockFont, fill = 0)
        elif phase == 3:
            draw.rectangle((totalWidth - clockWidth, totalHeight - clockHeight, totalWidth, totalHeight), fill = 'white')
            draw.text((totalWidth - clockWidth + 24, totalHeight - clockHeight), clockText, font = clockFont, fill = 0)

        img = img.convert(mode='1',dither=Image.FLOYDSTEINBERG)

        img.save("foo.png", "PNG")

        img = img.convert(mode='1',dither=Image.FLOYDSTEINBERG)
        epd.display(epd.getbuffer(img))

        epd.sleep()

        time.sleep(60)

        phase = phase + 1
        if phase > 3:
            phase = 0

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.Dev_exit()
    epd7in5_V2.epdconfig.module_exit()
    exit()
