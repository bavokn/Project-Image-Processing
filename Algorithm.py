import cv2
import numpy as np

files = {}
contourData = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
coins = {0.01: 0,  0.02: 0, 0.05: 0, 0.1: 0, 0.2: 0, 0.5: 0, 1: 0, 2: 0}

kernel = np.ones((5, 5), np.uint8)
#80,135,225
lower = np.array([50, 100, 150])
higher = np.array([255, 255, 255])
image = None

for i in range(9):
    #create mask for the image , filtering out most of the blue
    image = cv2.imread("./data/P1000" + str(697 + i) + "s.jpg")
    mask = cv2.inRange(image, lower, higher)
    image = cv2.bitwise_and(image, image, mask=mask)

    #grey scale the image
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #set the treshold so that only coins are fully visible
    ret, thresh = cv2.threshold(greyscale, 95, 255, cv2.THRESH_BINARY)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    dilate = cv2.dilate(opening, kernel, iterations=3)

    #blur the image so that there a less whitespaces
    blur = cv2.blur(thresh, (4, 4))

    #for creating less whitespaces
    erosion = cv2.erode(blur, kernel, iterations=5)
    #find the contours on the coints
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    #loop over the coints and check if the contours are larger than 5000, if so draw an ellipse over the coin
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000 :
            ellipse = cv2.fitEllipse(c)
            files[i] = cv2.ellipse(image, ellipse, (0, 255, 0), 2)
            files[i] = cv2.drawContours(image, c, -1, (255, 0, 0), 3)
            contourData[i].append(area)

cv2.imshow("test", files[5])
#
# for i in files:
#     cv2.imshow(str(i), files[i])


def amount(array):
    total = 0
    for data in array:
        if data > 21000:
            print ("2")
            total += 2
        elif data > 20000:
            print ("0.5")
            total += 0.5
        elif data > 18000:
            print ("1")
            total += 1
        elif data > 16000:
            print ("0.2")
            total += 0.2
        elif data > 15000:
            print ("0.05")
            total += 0.05
        elif data > 13000:
            print ("0.1")
            total += 0.1
        elif data > 12000:
            print ("0.02")
            total += 0.02
        elif data > 8500:
            print ("0.01")
            total += 0.01

    return total

for data in contourData:
    contourData[data].sort()
    print contourData[data]
    print amount(contourData[data])
    print ("----------------------------")



#draw all the original images with the ellipses
# for i in files:
#     cv2.imshow("test" + str(i), files[i])

cv2.waitKey()

# for i in range(9):
#     # create mask for the image , filtering out most of the blue
#     image = cv2.imread("./data/P1000" + str(697 + i) + "s.jpg")
#     mask = cv2.inRange(image, lower, higher)
#     image = cv2.bitwise_and(image, image, mask=mask)
#
#     # grey scale the image
#     greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # set the treshold so that only coins are fully visible
#     # ret, tresh = cv2.threshold(greyscale, 95, 255, cv2.THRESH_BINARY)
#     ret, thresh = cv2.threshold(greyscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     # noise removal
#     kernel = np.ones((3, 3), np.uint8)
#     opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
#     # sure background area
#     sure_bg = cv2.dilate(opening, kernel, iterations=3)
#     # Finding sure foreground area
#     dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
#     ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
#     # Finding unknown region
#     sure_fg = np.uint8(sure_fg)
#     unknown = cv2.subtract(sure_bg, sure_fg)
#     # Marker labelling
#     ret, markers = cv2.connectedComponents(sure_fg)
#
#     # Add one to all labels so that sure background is not 0, but 1
#     markers = markers + 1
#     # Now, mark the region of unknown with zero
#     markers[unknown == 255] = 0
#
#     markers = cv2.watershed(image, markers)
#     image[markers == -1] = [255, 0, 0]
