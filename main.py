#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle('Label tool')
    w.showMaximized()
    w.setWindowIcon(QIcon('images/icon.png'))
    w.show()

    sys.exit(app.exec_())