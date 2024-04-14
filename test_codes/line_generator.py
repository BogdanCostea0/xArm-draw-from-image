# ======================[ GENERATE POINTS]============================
import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread("../test_files/floare.jpeg")

# convert to grayscale
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection
edges = cv2.Canny(grayscale, 50, 100)

# get the coordinates of the edges
y_coords, x_coords = np.where(edges > 0)

# edges to countours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# make image with contours
# image = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
lines = []
if(len(contours) > 0):
    # get x and y coordinates of the contours and create lines
    for contour in contours:
        for i in range(len(contour) - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            lines.append([[x1, y1, x2, y2]])

    # reduce the number of lines by merging lines that are close to each other into one line if the distance between them is less than 10 pixels

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break

    # reduce lines that are shorter than a variable named pixel
    pixel = 4
    lines = [line for line in lines if np.sqrt((line[0][0] - line[0][2]) ** 2 + (line[0][1] - line[0][3]) ** 2) > pixel]

    # unite lines that are close to each other

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break

    # make rounded lines with the coordinates of the lines that are close to each other and have the same slope
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            if np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) < 10:
                lines[i][0] = [x1, y1, x4, y4]
                lines.pop(j)
                break


    # draw lines
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)



print(len(lines))

plt.imshow(image)
plt.show()
