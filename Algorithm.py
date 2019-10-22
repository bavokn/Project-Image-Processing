# coding=utf-8
import cv2
import numpy as np

files = {}
contourData = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
coins = {0.01: 0, 0.02: 0, 0.05: 0, 0.1: 0, 0.2: 0, 0.5: 0, 1: 0, 2: 0}

kernel = np.ones((5, 5), np.uint8)
# 80,135,225
lower = np.array([0, 80, 100])
higher = np.array([255, 255, 255])
image = None

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 20
fontColor              = (255, 255, 255)
lineType               = 20

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
            print ("2")
            total += 2
        elif data > 160:
            print ("0.5")
            total += 0.5
        elif data > 152:
            print ("1")
            total += 1
        elif data > 145:
            print ("0.2")
            total += 0.2
        elif data > 138:
            print ("0.05")
            total += 0.05
        elif data > 127:
            print ("0.1")
            total += 0.1
        elif data > 122:
            print ("0.02")
            total += 0.02
        elif data > 100:
            print ("0.01")
            total += 0.01

    return total

for i in range(9):
    # create mask for the image , filtering out most of the blue
    orgImage = cv2.imread("./data/P1000" + str(697 + i) + "s.jpg")
    mask = cv2.inRange(orgImage, lower, higher)
    image = cv2.bitwise_and(orgImage, orgImage, mask=mask)

    # grey scale the image
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # set the treshold so that only coins are fully visible
    ret, thresh = cv2.threshold(greyscale, 90, 255, cv2.THRESH_BINARY)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # for creating less whitespaces
    erosion = cv2.erode(opening, kernel, iterations=6)

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
    for key in keypoints:
        tmp.append(key.size)
        tmp.sort()
        val = amount(tmp)
        x, y = key.pt
        bottomLeftCornerOfText = (int(round(x)), int(round(y)))
        contourData[i].append(key.size)
        files[i] = cv2.putText(orgImage, str(val), bottomLeftCornerOfText, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                               lineType=cv2.LINE_AA)
        tmp = []
    files[i] = cv2.drawKeypoints(orgImage, keypoints, blank, (0, 0, 255),
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

i = 0
for file in files:
    cv2.imshow("image : " + str(i), files[file])
    i += 1

for data in contourData:
    contourData[data].sort()
    print contourData[data]
    print amount(contourData[data])
    print ("----------------------------")

cv2.waitKey()
