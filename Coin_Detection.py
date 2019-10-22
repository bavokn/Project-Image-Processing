#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unicodedata

import cv2
import numpy as np

try:
    if len(sys.argv) == 2:
        coin_file = str(sys.argv[1])
    else:
        raise IndexError
except IndexError:
    print "Please enter exactly one file."
    sys.exit()

contourData = {0: []}
coins = {0.01: 0, 0.02: 0, 0.05: 0, 0.1: 0, 0.2: 0, 0.5: 0, 1: 0, 2: 0}

lower = np.array([0, 0, 100])
higher = np.array([255, 255, 255])

# Set our filtering parameters
# Initialize parameter setting using cv2.SimpleBlobDetector
params = cv2.SimpleBlobDetector_Params()

# Set Area filtering parameters
params.filterByArea = True
params.minArea = 5000
params.maxArea = 300000

# Set Circularity filtering parameters
params.filterByCircularity = True
params.minCircularity = 0.8

# Set Convexity filtering parameters
params.filterByConvexity = True
params.minConvexity = 0.2

# Set inertia filtering parameters
params.filterByInertia = True
params.minInertiaRatio = 0.01


def amount(array):
    total = 0
    for data in array:
        if data > 165:
            total += 2
        elif data > 156:
            total += 0.5
        elif data > 149:
            total += 1
        elif data > 140:
            total += 0.2
        elif data > 134:
            total += 0.05
        elif data > 124:
            total += 0.1
        elif data > 120:
            total += 0.02
        elif data > 100:
            total += 0.01

    return total


# create mask for the image , filtering out most of the blue
try:
    orgImage = cv2.imread(coin_file)
    mask = cv2.inRange(orgImage, lower, higher)
    image = cv2.bitwise_and(orgImage, orgImage, mask=mask)
except Exception as ex:
    print "There was an error reading your provided image.\n" \
          "Please check if you entered an actual image."
    sys.exit()

# grey scale the image
greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# set the treshold so that only coins are fully visible
ret, thresh = cv2.threshold(greyscale, 85, 255, cv2.THRESH_BINARY)

# noise removal
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
# for creating less whitespaces
erosion = cv2.erode(opening, kernel, iterations=7)

# sure background area
dilate = cv2.dilate(erosion, kernel, iterations=1)

blur = cv2.blur(dilate, (3, 3))

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# invert image for blob detection
invert = cv2.bitwise_not(blur)
# Detect blobs
keypoints = detector.detect(invert)

# Draw blobs on our image as red circles
blank = np.zeros((1, 1))

tmp = []
coin_image = None
for key in keypoints:
    tmp.append(key.size)
    tmp.sort()
    val = amount(tmp)
    x, y = key.pt
    bottomLeftCornerOfText = (int(round(x)), int(round(y)))
    contourData[0].append(key.size)
    coin_image = cv2.putText(orgImage, str(val) + " ", bottomLeftCornerOfText, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                             lineType=cv2.LINE_AA)
    tmp = []

total_value = '{:,.2f} Euros'.format(amount(contourData.values()[0]))
coin_image_val = cv2.putText(coin_image, total_value, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                             (0, 0, 255), lineType=cv2.LINE_AA)

coin_image_circles = cv2.drawKeypoints(coin_image_val, keypoints, blank, (0, 0, 255),
                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Detected Coins", coin_image_circles)

cv2.waitKey()
