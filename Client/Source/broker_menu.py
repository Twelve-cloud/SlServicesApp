# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize

class BrokerMenu(QWidget):
    close = pyqtSignal()
    companyClicked = pyqtSignal()
    plotClicked = pyqtSignal()

    def __init__(self):
        super(BrokerMenu, self).__init__()
        uic.loadUi('Form/broker_menu_form.ui', self)
        self.companyButton.clicked.connect(self.slotCompanyClicked)
        self.plotButton.clicked.connect(lambda: self.plotClicked.emit())


    def slotCompanyClicked(self):
        self.companyClicked.emit()

    def closeEvent(self, event):
        self.close.emit()
