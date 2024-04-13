from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

im = plt.imread("../test_files/test.png")


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


grey = rgb2gray(im)
coordinates_np = np.argwhere(grey < 0.99)
coordinates = coordinates_np.tolist()
# print(type(coordinates))

# print(coordinates_np[:, 0], coordinates_np[:, 1])
# for each in coordinates:
#     print(each)



sorted_coordinates = pd.DataFrame({'x': coordinates_np[:, 1], 'y': coordinates_np[:, 0]})

# print(sorted_coordinates)

plt.plot(sorted_coordinates['y'], sorted_coordinates['x'])
plt.show()


# for each in coordinates:
#     print(each)
#
# sorted(coordinates, key=lambda x: x[0])
# print(sorted)

#
# sorted_coordinates = pd.DataFrame({'x': coordinates_np[:, 1], 'y': coordinates_np[:, 0]})
# sorted_coordinates.sort_values('x', inplace=True)

#
#
# plt.plot(sorted_coordinates['x'], sorted_coordinates['y'])
# plt.show()
