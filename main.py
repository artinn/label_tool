#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolBar, QVBoxLayout
from PyQt5.QtGui import QIcon


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle('Label tool')
    w.showMaximized()
    w.setWindowIcon(QIcon('images/icon.png'))

    left_tool_bar = QToolBar()
    left_tool_bar.addAction("hi")
    left_layout = QVBoxLayout()

    left_layout.setMenuBar(left_tool_bar)
    w.setLayout(left_layout)

    w.show()
    sys.exit(app.exec_())