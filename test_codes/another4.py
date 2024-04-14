import cv2
import numpy as np
img = cv2.imread('../test_files/house.png')
gray = cv2.imread('../test_files/house.png',0)
img=np.uint8(img)

blank=np.zeros([768,1024,3],np.uint8)
cnts = cv2.findContours(255-gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(blank, [c], -1, (255, 255, 255), -1)
kernel = np.ones((3, 3), np.uint8)
erosion_image = cv2.erode(blank, kernel, iterations=2)

blank = np.uint8(erosion_image[:,:,0])
cnts = cv2.findContours(blank, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(img, [c], -1, (0, 255, 0), 1)

cv2.imwrite('output.png', img)