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
import json
import urllib.request
from PIL import Image,ImageDraw,ImageFont

# Before running, make sure Pillow is up to date:
# python3 -m pip install --upgrade Pillow
# ...or if running as root (i.e. on startup)
# sudo python3 -m pip install --upgrade Pillow

logging.basicConfig(level=logging.DEBUG)

selfPath = os.path.dirname(os.path.realpath(__file__))
imagepath = os.path.join(selfPath, 'images')

clockFont = ImageFont.truetype(os.path.join(selfPath, 'agenda.ttf'), 160)
tempFont = ImageFont.truetype(os.path.join(selfPath, 'agenda.ttf'), 64)

tmpImageName = "/tmp/pictureframe.png"
totalWidth = 800
totalHeight = 480
clockWidth = 400
clockHeight = 200
clockTextFormat = "%H:%M"
curClockText = ""
phase = 0

strokeWidth = 10
strokeColor = (255, 255, 255)

# --- Weather.gov API configuration ---
# Lexington, MA (zip 02421)
WEATHER_LAT = 42.4473
WEATHER_LON = -71.2272
WEATHER_STATION_URL = None   # resolved on first call
WEATHER_CACHE_SECONDS = 600  # refresh temperature every 10 minutes

cachedTemp = None
lastWeatherFetch = None

def get_observation_station_url():
    """Resolve lat/lon to the nearest observation station via weather.gov."""
    url = f"https://api.weather.gov/points/{WEATHER_LAT},{WEATHER_LON}"
    req = urllib.request.Request(url, headers={"User-Agent": "einkpictureframe/1.0", "Accept": "application/geo+json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    stations_url = data["properties"]["observationStations"]
    req2 = urllib.request.Request(stations_url, headers={"User-Agent": "einkpictureframe/1.0", "Accept": "application/geo+json"})
    with urllib.request.urlopen(req2, timeout=10) as resp2:
        stations = json.loads(resp2.read())
    station_id = stations["features"][0]["properties"]["stationIdentifier"]
    return f"https://api.weather.gov/stations/{station_id}/observations/latest"

def fetch_temperature():
    """Fetch the current temperature from weather.gov, using a cache."""
    global cachedTemp, lastWeatherFetch, WEATHER_STATION_URL
    now = time.time()
    if lastWeatherFetch is not None and (now - lastWeatherFetch) < WEATHER_CACHE_SECONDS:
        return cachedTemp
    try:
        if WEATHER_STATION_URL is None:
            WEATHER_STATION_URL = get_observation_station_url()
            logging.info("Resolved weather station: %s", WEATHER_STATION_URL)
        req = urllib.request.Request(WEATHER_STATION_URL, headers={"User-Agent": "einkpictureframe/1.0", "Accept": "application/geo+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            obs = json.loads(resp.read())
        temp_c = obs["properties"]["temperature"]["value"]
        if temp_c is not None:
            cachedTemp = round(temp_c * 9 / 5 + 32)
        else:
            logging.warning("Temperature value was None in observation")
        lastWeatherFetch = now
    except Exception:
        logging.exception("Failed to fetch temperature from weather.gov")
    return cachedTemp

try:
    while True:
        time.sleep(5)

        now = datetime.datetime.now()
        clockText = now.strftime(clockTextFormat)
        if clockText == curClockText:
            continue

        curClockText = clockText

        logging.info("Creating next image...")

        imageList = [f for f in listdir(imagepath) if isfile(join(imagepath, f))]
        img = Image.open(os.path.join(imagepath, random.choice(imageList)))
        draw = ImageDraw.Draw(img)

        # Fetch current temperature
        tempF = fetch_temperature()
        tempText = f"{tempF}°F" if tempF is not None else ""

        if phase == 0:
            draw.text((24, 0), clockText, font = clockFont, fill = 0, stroke_width = strokeWidth, stroke_fill = strokeColor)
            if tempText:
                draw.text((24, 160), tempText, font = tempFont, fill = 0, stroke_width = strokeWidth / 2, stroke_fill = strokeColor)
        elif phase == 1:
            draw.text((totalWidth - clockWidth, 0), clockText, font = clockFont, fill = 0, stroke_width = strokeWidth, stroke_fill = strokeColor)
            if tempText:
                draw.text((totalWidth - clockWidth, 160), tempText, font = tempFont, fill = 0, stroke_width = strokeWidth / 2, stroke_fill = strokeColor)
        elif phase == 2:
            draw.text((24, totalHeight - clockHeight), clockText, font = clockFont, fill = 0, stroke_width = strokeWidth, stroke_fill = strokeColor)
            if tempText:
                draw.text((24, totalHeight - clockHeight - 40), tempText, font = tempFont, fill = 0, stroke_width = strokeWidth / 2, stroke_fill = strokeColor)
        elif phase == 3:
            draw.text((totalWidth - clockWidth, totalHeight - clockHeight), clockText, font = clockFont, fill = 0, stroke_width = strokeWidth, stroke_fill = strokeColor)
            if tempText:
                draw.text((totalWidth - clockWidth, totalHeight - clockHeight - 40), tempText, font = tempFont, fill = 0, stroke_width = strokeWidth / 2, stroke_fill = strokeColor)

        img.save(tmpImageName, "PNG")
        subprocess.call(['python', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'displayimage.py'), tmpImageName])

        phase = phase + 1
        if phase > 3:
            phase = 0

except KeyboardInterrupt:
    logging.info("ctrl-c")
    exit()
