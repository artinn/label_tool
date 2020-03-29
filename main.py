#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, qApp, QMainWindow, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from qtpy import QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LABEL TOOL')
        self.toolbar = self.addToolBar('Open')
        open_action = QAction(QIcon('images/open.png'), '  &Open', self)
        open_action.setStatusTip('Open file')
        self.toolbar.addAction(open_action)
        open_action.triggered.connect(self.openFileNamesDialog)

        label = QLabel(self)
        pixmap = QPixmap('images/image_jeans.jpg')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width()+pixmap.width(), pixmap.height()+pixmap.height())

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Directory
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(self, options=options)
        print(dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    main_window.setWindowIcon(QIcon('images/icon.png'))
    sys.exit(app.exec_())
