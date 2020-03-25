#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, qApp, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LABEL TOOL')
        self.statusBar().showMessage('This is a status bar')
        self.toolbar = self.addToolBar('Open')
        open_action = QAction(QIcon('images/open.png'), '  &Open', self)
        open_action.setStatusTip('Open file')
        self.toolbar.addAction(open_action)
        open_action.triggered.connect(self.openFileNamesDialog)


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
