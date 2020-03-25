#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, qApp, QMainWindow, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon

class TutorialWinow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LABEL TOOL')
        self.statusBar().showMessage('This is a status bar')

        self.toolbar = self.addToolBar('Open')

        open_action = QAction(QIcon('images/open.png'), '  &Open', self)
        #open_action.setShortcut('Win+E')
        open_action.setStatusTip('Open file')
        open_action.triggered.connect(qApp.quit)

        self.toolbar.addAction(open_action)
        self.setGeometry(300, 300, 400, 200)

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]

        f = open(fname, 'r')

        with f:
            data = f.read()
            self.textEdit.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tutorial_window = TutorialWinow()
    tutorial_window.showMaximized()
    ex = Example()
    tutorial_window.setWindowIcon(QIcon('images/icon.png'))
    sys.exit(app.exec_())
