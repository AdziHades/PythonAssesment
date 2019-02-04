
from PyQt5 import QtWidgets
from mainWindowUIFinal import Ui_mainWindow  # importing our generated file

import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.btnFindText.clicked.connect(self.btnFindTextClicked)

    def btnFindTextClicked(self):
        self.ui.label.setText("Button pressed")

app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())



