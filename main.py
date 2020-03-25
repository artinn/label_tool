#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, qApp, QMainWindow
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

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tutorial_window = TutorialWinow()
    tutorial_window.showMaximized()
    tutorial_window.setWindowIcon(QIcon('images/icon.png'))
    sys.exit(app.exec_())
