import os
from typing import Any, Dict

import cv2
import imutils
import matplotlib.pyplot as plt
from imutils import contours
from imutils.perspective import four_point_transform
from PIL import Image


def extracting_ocr(scrapping_params: Dict[str, Any]):

    import numpy as np

    image_folder = scrapping_params["image_folder"]
    image_path = os.path.join(image_folder, "marathon_39.png")

    ## Read
    img = cv2.imread(image_path)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (100, 23.9, 23.9), (130, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save
    cv2.imwrite("green.png", green)

    image_folder = scrapping_params["image_folder"]
    image_path = os.path.join(image_folder, "marathon_39.png")

    image = cv2.imread(image_path)

    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    fig, axs = plt.subplots(figsize=(10, 10))
    axs.imshow(edged)
    fig.savefig("./test.png")

    # find contours in the edge map, then sort them by their
    # size in descending order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has four vertices, then we have found
        # the thermostat display
        if len(approx) == 4:
            displayCnt = approx
            break

    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    output = four_point_transform(image, displayCnt.reshape(4, 2))

    fig, axs = plt.subplots(figsize=(10, 10))
    axs.imshow(output)
    fig.savefig("./test2.png")
