import cv2
import numpy as np
from skimage import segmentation, color
from skimage.future import graph
import math
from ImageLib import *
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class DetermineColor:
    def __init__(self):
        self.colors_map = {
                "red": {
                    "red": "#FF0000",
                    "maroon": "#800000",
                    "dark red": "#8B0000",
                },
                "pink": {
                    "light coral": "#F08080",
                     "salmon": "#FA8072",
                     "deep pink": "#FF1493",
                     "hot pink": "#FF69B4",
                     "light pink": "#FFB6C1",
                     "pink": "#FFC0CB",
                },
                "green": {
                    "lime": "#00FF00",
                    "green": "#008000",
                    "olive": "#808000",
                    "yellow green": "#9ACD32",
                    "dark olive green": "#556B2F",
                    "olive drab": "#6B8E23",
                    "lawn green": "#7CFC00",
                    "chart reuse": "#7FFF00",
                    "green yellow": "#ADFF2F",
                    "dark green": "#006400",
                    "forest green": "#228B22",
                    "lime green": "#32CD32",
                    "light green": "#90EE90",
                    "pale green": "#98FB98",
                    "spring green": "#00FF7F",
                    "sea green": "#2E8B57",
                    "dark sea green": "#8FBC8F",
                    "medium sea green": "#3CB371",
                },
                "grey": {
                    "dim grey": "#696969",
                    "grey": "#808080",
                    "dark grey": "#A9A9A9",
                    "silver": "#C0C0C0",
                    "light grey": "#D3D3D3",
                    "gainsboro":    "#DCDCDC"
                },
                "blue": {
                    "blue": "#0000FF", # 0, 0, 255
                    "royal blue": "#4169E1",
                    "medium blue": "#0000CD",
                    "dark blue": "#00008B",
                    "navy": "#000080",
                    "midnight blue": "#191970",
                    "light sky blue": "#87CEFA",
                    "sky blue": "#87CEEB",
                    "light blue": "#ADD8E6",
                    "dodger blue": "#1E90FF",
                    "deep sky blue": "#00BFFF",
                    "corn flower blue": "#6495ED",
                    "steel blue": "#4682B4",
                    "cadet blue": "#5F9EA0",
                    "powder blue": "#B0E0E6"
                },
                "turquoise": {
                    "dark turquoise": "#00CED1",
                    "turquoise": "#40E0D0",
                    "medium turquoise": "#48D1CC",
                    "aqua marine": "#7FFFD4",
                    "aqua": "#00FFFF",
                    "cyan": "#00FFFF"
                },
                "brown": {
                    "dark brown": "#331900",
                    "brown": "#663300",
                    "medium brown": "#994C00",
                    "light brown": "#CC6600",
                },
                "white": {
                    "white": "#FFFFFF",
                    "white smoke": "#F5F5F5",
                    "snow": "#FFFAFA"
                },
                "black": {
                    "black": "#000000"
                },
                "beige": {
                    "beige": "#F5F5DC",
                    "antique white": "#FAEBD7",
                    "bisque": "#FFE4C4",
                    "blanched almond": "#FFEBCD",
                    "wheat": "#F5DEB3",
                    "lemon chiffon": "#FFFACD",
                    "light golden rod yellow": "#FAFAD2",
                    "light yellow": "#FFFFE0",
                    "moccasin": "#FFE4B5",
                    "peach puff": "#FFDAB9",
                    "papaya whip": "#FFEFD5",
                    "pale golden rod": "#EEE8AA",
                    "khaki": "#F0E68C"
                },
                "purple": {
                    "indigo": "#4B0082",
                    "medium purple": "#9370DB",
                    "dark magenta": "#8B008B",
                    "purple": "#800080",
                    "medium orchid": "#BA55D3",
                    "dark orchid": "#9932CC",
                },
                "violet": {
                    "blue violet": "#8A2BE2",
                    "indigo": "#4B0082",
                    "slate blue": "#6A5ACD",
                    "medium slate blue": "#7B68EE",
                    "medium purple": "#9370DB",
                    "dark magenta": "#8B008B",
                    "dark violet": "#9400D3",
                    "dark orchid": "#9932CC",
                    "medium orchid": "#BA55D3",
                    "purple": "#800080",
                    "violet": "#EE82EE",
                    "magenta / fuchsia": "#FF00FF",
                    "orchid": "#DA70D6",
                    "medium violet red": "#C71585",
                    "pale violet red": "DB7093",
                },
                "orange": {
                    "chocolate": "#D2691E",
                    "peru": "#CD853F",
                    "sandy brown": "#F4A460",
                    "burly wood": "#DEB887",
                }
            }

    def run(self, file_name):
        image = cv2.imread(file_name)
        h = image.shape[0]
        w = image.shape[1]

        left_column = image[:, 0, :]
        rigth_column = image[:, -1, :]
        top_row = image[0, :, :]
        bottom_row = image[-1, :, :]

        edge_pixels = np.concatenate((left_column, rigth_column,
                                      top_row, bottom_row), axis=0)

        edge_pixels = edge_pixels.reshape(edge_pixels.shape[0]//2, 2, 3)

        main_colors = self.rag_merge(edge_pixels)
        new_main_colors = []
        for color in main_colors:
            is_find = False
            for index, new_color in enumerate(new_main_colors):
                dist = math.sqrt(np.sum(
                    (np.array(color[1]) - np.array(new_color[1])) ** 2))

                if dist < 5:
                    is_find = True
                    new_main_colors[index][0] += color[0]
            if not is_find:
                new_main_colors.append([color[0], color[1]])

        color = main_colors[0][1]

        tolerance = 20
        background_mask = cv2.inRange(image, (color[2] - tolerance, color[1] - tolerance, color[0] - tolerance),
                    (color[2] + tolerance, color[1] + tolerance, color[0] + tolerance))

        background_mask = cv2.bitwise_not(background_mask)
        contours, hierarchy = cv2.findContours(background_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        areas = [(cv2.contourArea(x), x) for x in contours]
        areas = sorted(areas, key=lambda x: x[0], reverse=True)
        if len(areas) > 1:
            for area in areas[1:]:
                contour = area[1]
                cv2.drawContours(background_mask, [contour], -1, (0), 3)

        kernel = np.ones((10, 10), np.uint8)
        closing = cv2.morphologyEx(background_mask, cv2.MORPH_CLOSE, kernel)
        closing = closing.astype(dtype=bool)

        colors = self.rag_main_colors(image)
        # Содержит все цвета на картинке с количеством пикселей данного цвета
        current_image_colors_map = {}

        for color in colors:

            nearest_color, nearest_color_pallete, nearest_color_in_dict, nearest_distance = self.get_nearest_color(
                color[1])

            if nearest_color_pallete in current_image_colors_map:

                color_m1 = current_image_colors_map[nearest_color_pallete]["average"] * \
                    current_image_colors_map[nearest_color_pallete]["value"]
                color_m2 = color[0] * color[1]

                current_image_colors_map[nearest_color_pallete]["value"] += color[0]

                current_image_colors_map[nearest_color_pallete]["average"] = (color_m1 + color_m2) / \
                                            current_image_colors_map[nearest_color_pallete]["value"]

            else:
                current_image_colors_map[nearest_color_pallete] = {}
                current_image_colors_map[nearest_color_pallete]["value"] = color[0]

                current_image_colors_map[nearest_color_pallete]["colors"] = []
                current_image_colors_map[nearest_color_pallete]["average"] = color[1]

            current_image_colors_map[nearest_color_pallete]["colors"].append(color)


        print(current_image_colors_map)
        print("test")

        return current_image_colors_map

    def rag_merge(self, image, mask=None, with_background=False):
        # opencv bgr <->  rgb
        img = image[:, :, ::-1]

        if mask is None:
            labels = segmentation.slic(img, compactness=200, n_segments=4)

            g = graph.rag_mean_color(img, labels)
            colors_list = g.nodes._nodes.values()
            main_colors = [(x["pixel count"], x["mean color"]) for x in colors_list]
            main_colors = sorted(main_colors, key=lambda x: x[0], reverse=True)
            return main_colors
        else:
            labels = segmentation.slic(img, compactness=150, n_segments=300, mask=mask)
            mask_uin8 = mask.astype(dtype="uint8")
            mask_uin8[mask_uin8 > 0] = 255



        return current_image_colors_map

    def k_mean_main_colors(self, image):
        def centroid_histogram(clt):
            # grab the number of different clusters and create a histogram
            # based on the number of pixels assigned to each cluster
            numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
            (hist, _) = np.histogram(clt.labels_, bins=numLabels)
            # normalize the histogram, such that it sums to one
            hist = hist.astype("float")
            hist /= hist.sum()
            # return the histogram
            return hist

        img = image[:, :, ::-1].copy()
        image_1d = img.reshape((img.shape[0] * img.shape[1], 3))
        clt = KMeans(n_clusters=100, max_iter=100)
        clt.fit(image_1d)

        hist = centroid_histogram(clt)

        main_colors = list(zip(hist, clt.cluster_centers_))
        return union_same_colors(main_colors)

    def rag_main_colors(self, image):
        img = image[:, :, ::-1]
        labels = segmentation.slic(img, compactness=30, n_segments=400, start_label=1)
        out1 = color.label2rgb(labels, img, kind='avg', bg_label=0)
        #show(out1[:, :, ::-1].copy())

        g = graph.rag_mean_color(img, labels)
        labels2 = graph.cut_threshold(labels, g, 29)
        out2 = color.label2rgb(labels2, img, kind='avg', bg_label=1)

        #show(out2[:, :, ::-1].copy())

        g = graph.rag_mean_color(out2, labels2)
        colors_list = g.nodes._nodes.values()
        main_colors = [[x["pixel count"], x["mean color"]] for x in colors_list]
        summ = sum([x[0] for x in main_colors ])
        for i in range(len(main_colors)):
            main_colors[i][0] /= summ

        return union_same_colors(main_colors)

    def get_nearest_color(self, process_color):

        hsv_process_color = np.uint8([[list(process_color)]])
        hsv_process_color = cv2.cvtColor(hsv_process_color, cv2.COLOR_RGB2HSV)
        hsv_process_color = hsv_process_color.astype("int32")
        hsv_process_color = hsv_process_color[0][0]

        nearest_distance = 1000000000
        nearest_color = None
        nearest_color_pallete = None
        nearest_color_in_dict = None

        for color_pallete in self.colors_map:
            for color in self.colors_map[color_pallete]:
                color_in_hex = self.colors_map[color_pallete][color]
                color_in_map = hex_to_rgb(color_in_hex)

                hsv_color_in_map = np.uint8([[list(color_in_map)]])
                hsv_color_in_map = cv2.cvtColor(hsv_color_in_map, cv2.COLOR_RGB2HSV)
                hsv_color_in_map = hsv_color_in_map.astype("int32")
                hsv_color_in_map = hsv_color_in_map[0][0]

                grad1 = hsv_color_in_map[0] * 2
                grad2 = hsv_process_color[0] * 2

                grad3 = abs(grad2 - grad1)
                if grad3 > 180:
                    grad3 = 360 - grad3

                # Если цвет не насыщенный
                if hsv_process_color[1] < 50:
                    if hsv_process_color[2] < 60:
                        # Мы считаем что цвет черный
                        nearest_distance = None
                        nearest_color = "black"
                        nearest_color_pallete = "black"
                        nearest_color_in_dict = "black"
                    elif hsv_process_color[2] > 195:
                        # Мы считаем что цвет белый
                        nearest_distance = None
                        nearest_color = "white"
                        nearest_color_pallete = "white"
                        nearest_color_in_dict = "white"
                    else:
                        # Мы считаем что цвет серый
                        nearest_distance = None
                        nearest_color = "grey"
                        nearest_color_pallete = "grey"
                        nearest_color_in_dict = "grey"
                    return nearest_color, nearest_color_pallete, nearest_color_in_dict, nearest_distance

                saturation_distance = (hsv_color_in_map[1] - hsv_process_color[1]) ** 2
                value_distance = (hsv_color_in_map[2] - hsv_process_color[2]) ** 2
                new_grad = (grad3 * 255 / 180) ** 2
                current_distance = 2.5 * new_grad + value_distance + saturation_distance

                if current_distance < nearest_distance:
                    nearest_distance = current_distance
                    nearest_color = color_in_map
                    nearest_color_pallete = color_pallete
                    nearest_color_in_dict = color

        return nearest_color, nearest_color_pallete, nearest_color_in_dict, nearest_distance



