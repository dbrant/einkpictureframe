#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'waveshare/python/lib')
if os.path.exists(libpath):
    sys.path.append(libpath)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd7in5_V2.EPD()
    logging.info("Initializing...")
    epd.init()

    #millis = int(round(time.time() * 1000))
    #logging.info("Clearing...")
    #epd.clear()
    #logging.info("That took " + str(int(round(time.time() * 1000)) - millis) + " ms")

    millis = int(round(time.time() * 1000))
    logging.info("Loading image...")
    img = Image.open(os.path.join(imagepath, 'db1.jpg'))
    img = img.convert(mode='1',dither=Image.FLOYDSTEINBERG)
    epd.display(epd.getbuffer(img))
    logging.info("That took " + str(int(round(time.time() * 1000)) - millis) + " ms")

    logging.info("Going to sleep...")
    epd.sleep()
    epd.dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
