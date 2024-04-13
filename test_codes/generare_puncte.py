from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
import math

im = plt.imread("test.png")
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
grey = rgb2gray(im)
coordinates_np = np.argwhere(grey < 0.99)
coordinates = coordinates_np.tolist()

def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def find_closest_neighbor(point, unvisited_points):
    min_distance = float('inf')
    closest_neighbor = None
    for neighbor in unvisited_points:
        if neighbor != point:
            dist = distance(point, neighbor)
            if dist < min_distance:
                min_distance = dist
                closest_neighbor = neighbor
    return closest_neighbor

def trajectory_angle(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)

def sort_by_trajectory_with_priority(coordinates):
    sorted_coordinates = [coordinates[0]] 
    unvisited_points = set(map(tuple, coordinates[1:]))  
    current_point = coordinates[0]

    while unvisited_points:
        closest_neighbor = find_closest_neighbor(current_point, unvisited_points)
        if closest_neighbor is None:
            break
        sorted_coordinates.append(closest_neighbor)
        unvisited_points.remove(closest_neighbor)
        current_point = closest_neighbor

    return sorted_coordinates


sorted_coordinates = sort_by_trajectory_with_priority(coordinates)
#print(sorted_coordinates)


print(sorte)
# dexter_list = []
# for i in range(0,len(sorted_coordinates),30):
#     dexter_list.append(i)

# nr_coordonate = 0
# for i in dexter_list:
#     nr_coordonate += 1

# print(nr_coordonate)

# for i in dexter_list


# x_values = [sorted_coordinates[i][1] for i in dexter_list]  
# y_values = [sorted_coordinates[i][0] for i in dexter_list]




plt.plot(x_values, y_values)
plt.show()