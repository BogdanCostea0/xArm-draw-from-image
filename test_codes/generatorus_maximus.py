import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image using OpenCV.
# im = plt.imread("../test_files/test.png")
im_cv = cv2.imread("../test_files/test.png", cv2.IMREAD_GRAYSCALE)

# Use morphological operations to clean up the edges and reduce double lines to single lines.

# Apply GaussianBlur to reduce noise and improve edge detection.
blurred = cv2.GaussianBlur(im_cv, (5, 5), 0)

# Use a threshold to clean the image further before edge detection.
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Increase the size of the kernel for more aggressive dilation and erosion to merge lines closer together.
kernel = np.ones((3, 3), np.uint8)  # Increase kernel size for more aggressive morphological operations.
dilated = cv2.dilate(thresh, kernel, iterations=2)  # Increase iterations if needed.
eroded = cv2.erode(dilated, kernel, iterations=1)  # Possibly reduce iterations to avoid over-thinning.


# Detect edges again using the Canny algorithm after morphological operations.
edges_optimized = cv2.Canny(eroded, threshold1=150, threshold2=250)


# Find coordinates of these edges.
y_coords_optimized, x_coords_optimized = np.where(edges_optimized > 0)

# formula to get distance from a point to another point

# Plot the result with y-coordinates in the correct order.
plt.figure(figsize=(12, 7))
plt.scatter(x_coords_optimized, y_coords_optimized, s=1)
plt.axis('equal')
plt.gca().invert_yaxis()  # Ensure the image is not flipped vertically.
plt.axis('off')  # Turn off the axis for a clean image of the drawing.
plt.show(), edges_optimized  # Return the processed edge image for visualization.
