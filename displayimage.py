#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import importlib.util
import logging
from PIL import Image,ImageDraw,ImageFont

_epd_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'waveshare', 'python', 'lib', 'waveshare_epd', 'epd7in5_V2.py')
_spec = importlib.util.spec_from_file_location('epd7in5_V2', _epd_path)
epd7in5_V2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(epd7in5_V2)

import logging
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

def display_image(image_path):
    """Load an image file, dither it, and display it on the e-ink display."""
    logging.info("Loading image...")

    img = Image.open(image_path)
    img = img.convert(mode='1', dither=Image.FLOYDSTEINBERG)

    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()

if __name__ == '__main__':
    try:
        display_image(sys.argv[1])
    except KeyboardInterrupt:
        logging.info("ctrl-c")
        exit()
