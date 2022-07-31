#!/usr/bin/python
# -*- coding:utf-8 -*-

# Screen test based on epd_7in5_V2_test.py

import sys
import os

import numpy

contentDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testcontent')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#    sys.path.append(libdir)

import logging
# TODO: refactor with omni-epd https://github.com/robweber/omni-epd
from waveshare_epd import epd7in5_V2
import time
# TODO: remove ImageShow testing once ready for SIT
from PIL import Image, ImageDraw, ImageFont, ImageShow
import traceback


# Takes an array of tuples and returns the largest area within them
# (a, b, c, d) - will return the smallest value for a,b and largest value for c,d
def maxArea(areaList):
    # initialise
    a, b, c, d = areaList[0]

    # find max for each element
    for t in areaList:
        at, bt, ct, dt = t
        a = min(a, at)
        b = min(b, bt)
        c = max(c, ct)
        d = max(d, dt)
    tup = (a, b, c, d)
    return tup


logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("pycasso test image display")
    epd = epd7in5_V2.EPD()

    logging.info("init and clear")
    epd.init()
    epd.Clear()

    # temp logging to understand how content directory is being handled
    logging.info(os.path.join(contentDirectory))

    font24 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(contentDirectory, 'Font.ttc'), 18)

    logging.info("Displaying Test Image")
    imageBase = Image.open(os.path.join(contentDirectory, 'test.png'))
    logging.info(imageBase.width)

    # Resize to thumbnail size based on epd resolution
    epdResolution = (epd.width, epd.height)
    logging.info(epdResolution)
    imageBase.thumbnail(epdResolution)

    # Make sure image is correct size and centered after thumbnail set
    # Define locations and crop settings
    widthDiff = (epd.width - imageBase.width) / 2
    heightDiff = (epd.height - imageBase.height) / 2
    leftPixel = 0 - widthDiff
    topPixel = 0 - heightDiff
    rightPixel = imageBase.width + widthDiff
    bottomPixel = imageBase.height + heightDiff
    imageCrop = (leftPixel, topPixel, rightPixel, bottomPixel)

    # Crop and prepare image
    imageBase = imageBase.crop(imageCrop)
    logging.info(imageBase.width)
    logging.info(imageBase.height)
    draw = ImageDraw.Draw(imageBase, 'RGBA')

    # Add text to image
    artistText = 'Lichtenstein'
    titleText = 'Cool Bird Wearing Glasses'
    artistLoc = 15
    titleLoc = 35
    # TODO: config variable for padding
    padding = 5

    artistBox = draw.textbbox((epd.width / 2, epd.height - artistLoc), artistText, font=font18, anchor='mb')
    titleBox = draw.textbbox((epd.width / 2, epd.height - titleLoc), titleText, font=font24, anchor='mb')
    drawBox = maxArea([artistBox, titleBox])

    # TODO: create option to draw box across whole image width or all the way down
    drawBox = tuple(numpy.add(drawBox, (-padding, -padding, padding, padding)))

    opacity = 150
    draw.rectangle(drawBox, fill=(255, 255, 255, opacity))
    draw.text((epd.width / 2, epd.height - artistLoc), artistText, font=font18, anchor='mb', fill=0)
    draw.text((epd.width / 2, epd.height - titleLoc), titleText, font=font24, anchor='mb', fill=0)

    epd.display(epd.getbuffer(imageBase))

    # TODO: remove image test or config it out
    ImageShow.show(imageBase)
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
