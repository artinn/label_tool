from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QWidget, QGridLayout, \
    QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QSpinBox, QLineEdit, QPushButton, QButtonGroup
from PyQt5.QtWidgets import QLabel
import sys
from PyQt5.QtGui import QIcon, QPixmap
import os
from QtImageViewer import QtImageViewer
import json
from functools import partial

from DetermineColor import DetermineColor
from matplotlib import pyplot as plt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main.ui", self)
        self.showMaximized()
        self.setWindowTitle('Label tool')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.toolbar = self.addToolBar('Open')
        open_action = QAction(QIcon('images/open.png'), '  &Open', self)
        open_action.setStatusTip('Open file')

        self.image_viewer = QtImageViewer()
        self.image_layout.addWidget(self.image_viewer)
        self.image_viewer.show()
        self.toolbar.addAction(open_action)
        open_action.triggered.connect(self.open_files_dialog)

        self.next_button.clicked.connect(self.show_next)
        self.previous_button.clicked.connect(self.show_previous)
        self.save_button.clicked.connect(self.save)
        self.delete_button.clicked.connect(self.delete_image)
        self.determine_color_button.clicked.connect(self.determine_color)

        self.current_image_index = None
        self.image_list = []

        self.check_boxes = {}
        self.radio_buttons = {}
        self.spin_boxes = {}
        self.line_edits = {}
        self.widgets = {}

        self.color_determiner = DetermineColor()
        self.label_dict = {
            "AGE": {
                "type": "check_boxes",
                "values":  {0: '0_2', 1: '2_8', 2: '9_14', 3: '15_24', 4: '25_34', 5: '35_44', 6: '45_54', 7: '55+'},
            },

            "SHAPE": {
                "type": "check_boxes",
                "values": {0: 'Column', 1: 'Hour-glass', 2: 'Pear', 3: 'Apple', 4: 'Full hour-glass', 5: 'Full pear'}
            },

            "OCCASION": {
                "type": "check_boxes",
                "values": {0: 'Casual', 1: 'Smart Office Attire', 2: 'Tea-party / Summer party / Day-time occasion',
                              3: 'Black tie', 4: 'Smart-Casual / Creative', 5: 'Beach', 6: 'Sport'}
            },

            "SEASON": {
                "type": "check_boxes",
                "values": {0: "summer", 1: "autumn", 2: "winter", 3: "spring"}
            },

            "PATTERN": {
                "type": "check_boxes",
                "values": {0: "yes"}
            },

            "SHADE": {
                "type": "radio_buttons",
                "values": {0: "light", 1: "true", 2: "dark", 3: "neon"}
            },

            "COLOR": {
                "type": "soft_select",
                "depend_on": "SHADE",
                "map": {
                    "light": {0: "red", 1: "pink", 2: "green", 3: "grey", 4:"blue", 5:"turquoise", 6:"brown", 7:"white", 8:"black", 9:"beige", 10:"purple", 11:"violet", 12:"orange"},
                    "true": {0: "red", 1: "pink", 2: "green", 3: "grey", 4:"blue", 5:"turquoise", 6:"brown", 7:"white", 8:"black", 9:"beige", 10:"purple", 11:"violet", 12:"orange"},
                    "dark": {0: "red", 1: "pink", 2: "green", 3: "grey", 4:"blue", 5:"turquoise", 6:"brown", 7:"white", 8:"black", 9:"beige", 10:"purple", 11:"violet", 12:"orange"},
                    "neon": {0: "red", 1: "pink", 2: "green", 4: "blue", 5: "turquoise", 10: "purple", 11: "violet", 12: "orange"}                    }
            },


            "GENDER": {
                "type": "radio_buttons",
                "values": {0: "male", 1: "female", 2: "unisex"}
            },

            "CATEGORIES": {
                "type": "radio_buttons",
                "values": {0: "Accessories", 1: "Tops", 2: "Trousers/Pants", 3: "Skirts", 4: "Dresses", 5: "Jeans",
                           6: "Jumpsuit", 7: "Sweaters/Jumpers", 8: "Cardigans", 9: "Bags", 10: "Shoes", 11: "Coats",
                           12: "Jackets", 13: "Blazers", 14: "Shorts", 15: "Underwear", 16: "Sarong", 17: "Coverups",
                           18: "Swimwear"}
            },

            "SUBCATEGORIES": {
                "type": "radio_buttons",
                "depend_on": "CATEGORIES",
                "map": {
                    "Accessories": {0: "earrings", 1: "rings", 2: "sunglasses", 3: "necklaces", 4: "hair accessories",
                                    5: "gloves", 6: "scarves", 7: "socks", 8: "tights", 9: "brooches", 10: "belts",
                                    11: "bracelet"},
                    "Tops": {0: "empty"},
                    "Trousers/Pants": {0: "empty"},
                    "Skirts": {0: "mini", 1: "midi", 2: "maxi"},
                    "Dresses": {0: "mini", 1: "midi", 2: "maxi"},
                    "Jeans": {0: "empty"},
                    "Jumpsuit": {0: "empty"},
                    "Sweaters/Jumpers": {0: "empty"},
                    "Cardigans": {0: "empty"},
                    "Bags": {0: "shoulder", 1: "clutch"},
                    "Shoes": {0: "boots", 1: "pumps", 2: "flip-flops", 3: "sneakers", 4: "over-the-knee boots"},
                    "Coats": {0: "empty"},
                    "Jackets": {0: "empty"},
                    "Blazers": {0: "empty"},
                    "Shorts": {0: "empty"},
                    "Underwear": {0: "bikini tops", 1: "bikini bottoms", 3: "one-piece"},
                    "Sarong": {0: "empty"},
                    "Coverups": {0: "empty"},
                    "Swimwear": {0: "bikini tops", 1: "bikini bottoms", 3: "one-piece"}
                }
            },

            "MERCHANT_INFO": {
                "type": "line_edit",
                "values": ["Merchant", "Brand"]
            }
        }

        self.fill_tool_box()
        self.show()

    def open_files_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Directory
        options |= QFileDialog.ShowDirsOnly
        self.selected_dir = QFileDialog.getExistingDirectory(self, options=options)

        files = os.listdir(self.selected_dir)
        self.image_list = []
        for x in files:
            if x.endswith('jpg') or x.endswith('png'):
                self.image_list.append(x)

        if len(self.image_list) > 0:
            self.current_image_name = os.path.join(self.selected_dir, self.image_list[0])
            self.image_viewer.loadImageFromFile(self.current_image_name)
            self.load_labels(self.current_image_name)
            self.current_image_index = 0
            self.enable_buttons()

    def load_labels(self, image_full_path):
        self.disable_all_checkboxes()

        if os.path.isfile(image_full_path + ".json"):
            with open(image_full_path + ".json", "r") as f:
                text = f.read()
                current_image_data = json.loads(text)
                self.json_presence.setEnabled(True)

            self.load_single_type(self.check_boxes, current_image_data)
            self.load_single_type(self.radio_buttons, current_image_data)
            self.load_single_type(self.spin_boxes, current_image_data, mode='spin_box')
            self.load_single_type(self.line_edits, current_image_data, mode='line_edit')


    def load_single_type(self, widgets_dict, current_image_data, mode=None):
        for page in widgets_dict:
            if page in current_image_data:
                for item in widgets_dict[page]:
                    key = list(item.keys())[0]
                    if mode is None:
                        if key in current_image_data[page]:
                            item[key].setChecked(True)
                    elif mode=='line_edit':
                        for elem in current_image_data[page]:
                            first_key = list(elem.keys())[0]
                            if first_key == key:
                                item[key].setText(elem[first_key])
                    else:
                        for elem in current_image_data[page]:
                            first_key = list(elem.keys())[0]
                            if first_key == key:
                                item[key].setValue(elem[first_key])

    def enable_buttons(self):
        if self.current_image_index is not None:
            self.next_button.setEnabled(len(self.image_list) > self.current_image_index + 1)
            self.previous_button.setEnabled(len(self.image_list) > (len(self.image_list)
                                                                    - self.current_image_index))
            self.delete_button.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)
            self.save_button.setEnabled(False)


    def delete_image(self):
        image_path = os.path.join(self.selected_dir, self.image_list[self.current_image_index])
        os.remove(image_path)

        label_path = os.path.join(self.selected_dir, self.image_list[self.current_image_index] + ".json")
        if os.path.exists(label_path):
            os.remove(label_path)

        del self.image_list[self.current_image_index]
        self.current_image_index -= 1
        self.show_next()

    def show_next(self):
        if self.current_image_index is not None:
            self.current_image_index += 1
            if len(self.image_list) > self.current_image_index:
                self.current_image_name = os.path.join(self.selected_dir, self.image_list[self.current_image_index])
                self.image_viewer.loadImageFromFile(self.current_image_name)
                self.load_labels(self.current_image_name)
                if os.path.isfile(self.current_image_name + ".json"):
                    self.json_presence.setEnabled(True)
                else:
                    self.json_presence.setEnabled(False)
            elif len(self.image_list) > 0:
                self.show_previous()
            else:
                self.image_viewer.clearImage()
                self.current_image_index = None

        self.enable_buttons()

    def show_previous(self):
        if self.current_image_index is not None:
            if len(self.image_list) > (len(self.image_list) - self.current_image_index):
                self.current_image_index -= 1
                self.current_image_name = os.path.join(self.selected_dir, self.image_list[self.current_image_index])
                self.image_viewer.loadImageFromFile(self.current_image_name)
                self.load_labels(self.current_image_name)
                if os.path.isfile(self.current_image_name + ".json"):
                    self.json_presence.setEnabled(True)
                else:
                    self.json_presence.setEnabled(False)
        self.enable_buttons()

    def save(self):
        data = {}

        for multiclass in self.check_boxes:
            data[multiclass] = []
            for item in self.check_boxes[multiclass]:
                for key, value in item.items():
                    if value.isChecked():
                        data[multiclass].append(key)

        for single_class in self.radio_buttons:
            for item in self.radio_buttons[single_class]:
                for key, value in item.items():
                    if value.isChecked():
                        data[single_class] = key
                        break

        for page in self.spin_boxes:
            data[page] = []
            for item in self.spin_boxes[page]:
                for key, value in item.items():
                    data[page].append({key: value.value()})


        for line in self.line_edits:
            data[line] = []
            for item in self.line_edits[line]:
                for key, value in item.items():
                    data[line].append({key: value.text()})

        with open(os.path.join(self.selected_dir,
                               self.image_list[self.current_image_index] + ".json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(data))

    def disable_all_checkboxes(self):
        for multiclass in self.check_boxes:
            for item in self.check_boxes[multiclass]:
                for key, value in item.items():
                    value.setChecked(False)

    def depend_radiobuttons_switcher(self, need_update_page, selected_radiobutton):
        self.update_depend_page(need_update_page, selected_radiobutton)

    def update_depend_page(self, need_update_page, selected_radiobutton):
        widget = self.widgets[need_update_page]
        grid = widget.children()[0]

        for i in range(1, len(widget.children())):
            child_widget = widget.children()[1]
            child_widget.setParent(None)
            child_widget.deleteLater()

        values = self.label_dict[need_update_page]["map"][selected_radiobutton]
        if "soft_select" == self.label_dict[need_update_page]["type"]:
            self.spin_boxes[need_update_page] = []
            for key, value in values.items():
                shared_widget = QWidget()
                v_layout = QHBoxLayout()
                shared_widget.setLayout(v_layout)
                text = QLabel()
                text.setText(value)
                v_layout.addWidget(text)
                spin_box = QSpinBox()
                spin_box.setSuffix("%")
                spin_box.setRange(0, 100)
                v_layout.addWidget(spin_box)
                grid.addWidget(shared_widget)
                self.spin_boxes[need_update_page].append({value: spin_box})

        if "radio_buttons" == self.label_dict[need_update_page]["type"]:
            self.radio_buttons[need_update_page] = []

            for key, value in values.items():
                radio_button = QRadioButton()
                radio_button.setText(value)
                grid.addWidget(radio_button)
                self.radio_buttons[need_update_page].append({value: radio_button})
            if self.radio_buttons[need_update_page] != list():
                first_key = list(self.radio_buttons[need_update_page][0].keys())[0]
                self.radio_buttons[need_update_page][0][first_key].setChecked(True)

    def update_page(self, widget, page, mode="Update"):
        grid = widget.children()[0]

        if self.label_dict[page]["type"] == "check_boxes":
            self.check_boxes[page] = []

            for key, item in self.label_dict[page]["values"].items():
                check = QCheckBox()
                check.setText(item)
                grid.addWidget(check)
                self.check_boxes[page].append({item: check})

            def select_all_checkboxes():
                for item in self.check_boxes[page]:
                    key = list(item.keys())[0]
                    item[key].setChecked(True)

            select_all = QPushButton()
            select_all.setText('select all')
            grid.addWidget(select_all)
            select_all.clicked.connect(select_all_checkboxes)

        elif self.label_dict[page]["type"] == "radio_buttons":
            self.radio_buttons[page] = []

            for key, item in self.label_dict[page]["values"].items():
                radio_button = QRadioButton()
                radio_button.setText(item)
                grid.addWidget(radio_button)
                self.radio_buttons[page].append({item: radio_button})

            if self.radio_buttons[page] != list():
                first_key = list(self.radio_buttons[page][0].keys())[0]
                self.radio_buttons[page][0][first_key].setChecked(True)

        elif self.label_dict[page]["type"] == "line_edit":
            self.line_edits[page] = []

            for key in self.label_dict[page]["values"]:
                shared_widget = QWidget()
                v_layout = QVBoxLayout()
                text = QLabel()
                text.setText(key)
                v_layout.addWidget(text)
                shared_widget.setLayout(v_layout)
                line = QLineEdit()
                v_layout.addWidget(line)
                grid.addWidget(shared_widget)
                self.line_edits[page].append({key: line})


    def fill_tool_box(self):
        for page in self.label_dict:
            widget = QWidget()
            grid = QGridLayout()
            widget.setLayout(grid)
            self.widgets[page] = widget

            if "depend_on" in self.label_dict[page]:
                depend_on = self.label_dict[page]["depend_on"]
                if self.label_dict[depend_on]["type"] != "radio_buttons":
                    error_label = QLabel()
                    error_label.setText("Column with this one depend\n on must have type 'radio_buttons' ")
                    grid.addWidget(error_label)
                else:
                    # Привязываемся к сигналу toggle
                    for list_item in self.radio_buttons[depend_on]:

                        func = partial(self.depend_radiobuttons_switcher,
                                need_update_page=str(page),
                                selected_radiobutton=str(list(list_item.keys())[0])
                        )

                        list_item[list(list_item.keys())[0]].toggled.connect(func)

                    self.update_depend_page(page,
                                            list(self.label_dict[depend_on]["values"].items())[0][1])
            else:
                self.update_page(widget, page, mode="Create")
            self.toolBox.addItem(widget, page)
        self.toolBox.removeItem(0)

    def determine_color(self):
        colors_dict = self.color_determiner.run(self.current_image_name)

        for spinbox_color in self.spin_boxes["COLOR"]:
            list(spinbox_color.items())[0][1].setValue(0)

        for key, value in colors_dict.items():
            for spinbox_color in self.spin_boxes["COLOR"]:
                if key in spinbox_color:
                    spinbox_color[key].setValue(colors_dict[key]["value"])

        border_size = 0.3
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')

        colors_string = [key + " " + str(round(colors_dict[key]["value"] * 100, 2)) + "%" for
                         key in colors_dict.keys()]
        values = [colors_dict[key]["value"] for key in colors_dict.keys()]
        colors = np.array([colors_dict[key]["average"] for key in colors_dict.keys()])
        colors = colors / 255

        ax.pie(values,radius=1, labels=colors_string,colors=colors,
               wedgeprops=dict(width=border_size, edgecolor='w'))

        colors_map = []
        for key in colors_dict:
            is_first = True
            for color in colors_dict[key]["colors"]:
                if is_first:
                    colors_map.append([key, color[0], color[1]])
                else:
                    colors_map.append(["", color[0], color[1]])

                is_first = False

        colors_string = [x[0] for x in colors_map]
        values = [x[1] for x in colors_map]
        colors = np.array([x[2] for x in colors_map])

        colors = colors / 255
        ax.pie(values, radius=1 -border_size, colors=colors,
               wedgeprops=dict(width=border_size, edgecolor='w'))
        plt.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MainWindow()
    sys.exit(app.exec())
