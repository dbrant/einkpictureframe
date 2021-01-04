#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'waveshare/python/lib')
if os.path.exists(libpath):
    sys.path.append(libpath)

import logging
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

imageName = sys.argv[1]

try:
    logging.info("Loading image...")

    img = Image.open(imageName)
    img = img.convert(mode='1',dither=Image.FLOYDSTEINBERG)

    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()
    epd.Dev_exit()

except KeyboardInterrupt:    
    logging.info("ctrl-c")
    exit()
