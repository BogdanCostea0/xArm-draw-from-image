from __future__ import division
import cv2
import numpy as np
from time import sleep
import sys

from matplotlib import pyplot as plt

'''
Pixel order is determined by its surrounding black pixels, which is found recursively.
To make sure decently complex images work as well, the recursion limit of python (which
was fairly conservative to begin with) was increased to a relatively safe number of 3000
'''
sys.setrecursionlimit(5000)

# GLOBAL VARIABLE DECLARATIONS
global imgSizeX
global imgSizeY

# IMAGE PROCESSING
# resize image such that it fits within number of motor steps
im_original = cv2.imread('../../test_files/house.png')
imgSizeY, imgSizeX = im_original.shape[:2]

if (imgSizeX > imgSizeY):
    rescaleFactor = 200 / imgSizeX
else:
    rescaleFactor = 200 / imgSizeY

imgResized = cv2.resize(im_original, (0, 0), fx=rescaleFactor, fy=rescaleFactor,
                        interpolation=cv2.INTER_AREA)  # common interpolation for shrinking
cv2.imwrite('img_resize.jpeg', imgResized)

imgSizeY, imgSizeX = imgResized.shape[:2]

# adds border to prevent loss of relevant pixels on edges
'''
borderSize = 3
imgResized = cv2.copyMakeBorder(imgResized, top=borderSize, bottom=borderSize, left=borderSize, right=borderSize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0])

imgSizeY, imgSizeX = imgResized.shape[:2]
'''

# loading images, cvtColor converts to grayscale, interpolation choices based on OpenCV documentation
imgColour = imgResized
imgGrayscale = cv2.cvtColor(imgColour, cv2.COLOR_BGR2GRAY)
(thresh, imgBlackWhite) = cv2.threshold(imgGrayscale, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
imgBlackWhite = cv2.threshold(imgGrayscale, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('img_bw.jpeg', imgBlackWhite)

# edge detection
imgBlurredColour = cv2.GaussianBlur(imgColour, (7, 7), 0)  # blurs to soften edges, really sure how effetive this is yet
imgBlurredBlackWhite = cv2.GaussianBlur(imgBlackWhite, (7, 7), 0)

imgOutlinedColour = cv2.Canny(imgBlurredColour, 100, 200)  # for colour
# processes and outputs an image, 100 200 is the ratio for acceptable edge gradation
imgOutlinedBlackWhite = cv2.Canny(imgBlurredBlackWhite, 100, 200)  # for black and white
imgOutlinedGrayscale = cv2.Canny(imgGrayscale, 100, 200)
# so that we can merge all three together to get better acuracy of the image

imgOutlinedTemp = cv2.addWeighted(imgOutlinedBlackWhite, 1, imgOutlinedColour, 1, 0)  # merges two photos together
imgOutlined = cv2.addWeighted(imgOutlinedTemp, 1, imgOutlinedGrayscale, 1, 0)  # merges a third to it

# invert colours for usable black outlines
imgOutlined = cv2.bitwise_not(imgOutlined)
cv2.imwrite('img_outline.jpeg', imgOutlined)
# print("done converting")
# cv2.imshow("window with bord", imgOutlined)
# cv2.waitKey(0)


# ORDERED DETECTION OF RELEVANT PIXELS
global coordsX
coordsX = []
global coordsY
coordsY = []
global coordsCount
coordsCount = 0;

# for debugging purposes
outputFile = open('coordinatesIMG.txt', 'w')

'''
wentTo is a 2D array which remembers which coordinates have been checked already, as to not repeatedly
save the same pixels. Repeats the value 0, imgSizeY times, inside an array of size imgSizeX
'''
global wentTo
# wentTo = [[0 for xcoord in range (imgSizeX+3*borderSize)] for k in range (imgSizeY+ 3*borderSize)]
wentTo = [[0 for xcoord in range(imgSizeX)] for k in range(imgSizeY)]


'''
Function that checks all 8 directions around the point that was just passed in
'''


def checkAroundCurrentPoint(xcoord, ycoord):
    # make sure global gets changed
    global coordsX
    global coordsY
    global wentTo
    global coordsCount

    newXCoord = xcoord - 1
    newYCoord = ycoord
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord - 1
    newYCoord = ycoord + 1
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord
    newYCoord = ycoord + 1
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord + 1
    newYCoord = ycoord + 1
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord + 1
    newYCoord = ycoord
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord + 1
    newYCoord = ycoord - 1
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord
    newYCoord = ycoord - 1
    checkIfBlack(newXCoord, newYCoord);

    newXCoord = xcoord - 1
    newYCoord = ycoord - 1
    checkIfBlack(newXCoord, newYCoord);


'''
Helper function that gets called to make sure that:
1. it's a valid point
2. it hasn't been checked yet
3. it's a black pixel
--> If so, save into outputFile
'''


def checkIfBlack(newXCoord, newYCoord):
    # make sure global gets changed
    global coordsX
    global coordsY
    global wentTo
    global coordsCount

    if (0 <= newXCoord < imgOutlined.shape[0]) and (0 <= newYCoord < imgOutlined.shape[1]):
        if wentTo[newXCoord][newYCoord] == 0:
            if imgOutlined[newXCoord][newYCoord] == 0:
                coordsX = np.append(coordsX, newXCoord)
                coordsY = np.append(coordsY, newYCoord)
                #write to file
                outputFile.write(str(newXCoord) + " " + str(newYCoord) + "\n")

                # print(newXCoord, newYCoord)
                # coordsCount+=1
                wentTo[newXCoord][newYCoord] = 1
                checkAroundCurrentPoint(newXCoord, newYCoord)
            wentTo[newXCoord][newYCoord] = 1


'''
IMAGE'S PIXEL DETECTION
1. Iterates through all the pixels of the image, if a black pixel is found, check
around to make sure if it forms a continuous line. Recusively check until the 
line ends.
2. Goes through all points to make sure all relevant pixels are found

'''
for xcoord in range(imgOutlined.shape[0]):
    for ycoord in range(imgOutlined.shape[1]):
        if 0 <= xcoord < imgSizeX and 0 <= ycoord < imgSizeY:
            if imgOutlined[xcoord][ycoord] == 0:
                if wentTo[xcoord][ycoord] == 0:
                    coordsX = np.append(coordsX, xcoord)
                    coordsY = np.append(coordsY, ycoord)
                    # write to file
                    outputFile.write(str(xcoord) + " " + str(ycoord) + "\n")
                    # print (xcoord, ycoord)
                    coordsCount += 1
                    wentTo[xcoord][ycoord] = 1
                    checkAroundCurrentPoint(xcoord, ycoord)
                wentTo[xcoord][ycoord] = 1

# "!" character indicates end of file, for serial parsing purposes
# print >> outputFile, "!"


# passes in number of coordinates in element, for imageDraw.ino's for loop purposes
# does not need a "@GetNext" command, assumes imageDraw.ino needs it
numElements = len(coordsX)

sleep(3)
print("sending in numElements")
print(str(numElements))


print("done")

'''
IMAGE'S PIXEL PARSING
Serial continuously reads line, awaiting instructions from arduino's imageDraw.ino
When instructions to send more pixels are received, python's Serial sends in a batch
of 50, or as many as possible, then keeps waiting for further instructions
'''

for i in range(numElements):
    # print("sending in from python: " + str(coordsX[i]) + " " + str(coordsY[i]))
    # make list of coordinates
    coordinates = [coordsX[i], coordsY[i]]
    # print(coordinates)

# make plote
sortie = open('coordinatesIMG.txt', 'r')
lines = sortie.readlines()
for line in lines:
    x, y = line.split()
    x = int(x)
    y = int(y)
    cv2.circle(imgColour, (x, y), 1, (0, 0, 255), -1)

print(len(lines))
plt.imshow(imgColour)
plt.show()

# arduinoMessage = "NOT @GetNext!"
#
# arduinoMessage = "get next"
# # loop so that the python program does quit
# for i in range(numElements):
#     while (arduinoMessage != "@GetNext"):
#         # read in a non-relevant line i.e. Sleep
#         print("from python: waiting")
#         # check for next line
#         arduinoMessage = ser.readline()
#
#         print(str(i) + "from arduino, arduinoMessage:" + arduinoMessage)
#     # is @GetNext, give it next
#     print("sending in from python: " + str(coordsX[i]) + " " + str(coordsY[i]))
#     ser.write(str(coordsX[i]))
#     ser.write(" ")
#     ser.write(str(coordsY[i]))
#     ser.write("\n")
#     ser.flush()
#
#     arduinoMessage = "arduinoMessage get >:("
