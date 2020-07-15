import cv2
import numpy as np
import math

# Отображает на экране изображение заданное в формате OpenCV
def show(image, window_title='image', size_max=None):
    if size_max:
        scale = float(size_max) / float(max([image.shape[0], image.shape[1]]))
        show_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(window_title, show_image)
    else:
        cv2.imshow(window_title, image)
    cv2.waitKey(0)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb_color = []
    for color in(0, 2, 4):
        current_color = hex_color[color:color+2]
        rgb_color.append(int(current_color, 16))
    rgb_color = np.array(rgb_color)
    return rgb_color

def plot_colors(new_main_colors):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in new_main_colors:
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

def union_same_colors(main_colors):
    new_main_colors = []
    for color in main_colors:
        is_find = False
        for index, new_color in enumerate(new_main_colors):
            dist = math.sqrt(np.sum(
                (np.array(color[1]) - np.array(new_color[1])) ** 2))
            #print(dist)

            if dist < 5:
                is_find = True
                mixed_color = (np.array(new_main_colors[index][1]) * new_main_colors[index][0] + \
                               np.array(color[1]) * color[0]) / (new_main_colors[index][0] + color[0])

                new_main_colors[index][0] += color[0]
                new_main_colors[index][1] = mixed_color
        if not is_find:
            new_main_colors.append([color[0], color[1]])

    new_main_colors = sorted(new_main_colors, key=lambda x: x[0], reverse=True)
    return new_main_colors