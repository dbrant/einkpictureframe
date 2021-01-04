#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from os import listdir
from os.path import isfile, join
import logging
import datetime
import random
import subprocess
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

selfPath = os.path.dirname(os.path.realpath(__file__))
imagepath = os.path.join(selfPath, 'images')

imageList = [f for f in listdir(imagepath) if isfile(join(imagepath, f))]

clockFont = ImageFont.truetype(os.path.join(selfPath, 'agenda.ttf'), 128)

tmpImageName = "/tmp/pictureframe.png"
totalWidth = 800
totalHeight = 480
clockWidth = 320
clockHeight = 150
clockTextFormat = "%H:%M"
curClockText = ""
phase = 0

try:
    while True:
        time.sleep(5)

        now = datetime.datetime.now()
        clockText = now.strftime(clockTextFormat)
        if clockText == curClockText:
            continue

        curClockText = clockText

        logging.info("Creating next image...")

        img = Image.open(os.path.join(imagepath, random.choice(imageList)))
        draw = ImageDraw.Draw(img)

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

        #img.save(tmpImageName, "PNG")
        subprocess.call([os.path.join(os.path.dirname(os.path.realpath(__file__)), 'displayimage.py'), tmpImageName])

        phase = phase + 1
        if phase > 3:
            phase = 0

except KeyboardInterrupt:    
    logging.info("ctrl-c")
    exit()
