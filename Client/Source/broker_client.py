# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize

class BrokerClient(QWidget):
    orderClicked = pyqtSignal()

    def __init__(self):
        super(BrokerClient, self).__init__()
        uic.loadUi('Form/broker_client_form.ui', self)
        self.orderButton.clicked.connect(self.slotOrderButtonClicked)

    def slotOrderButtonClicked(self):
        order = self.listWidget.item(self.listWidget.currentRow()).text()
        x = order.split(':')
        self.login = x[0]
        x = x[1].split('[')
        self.order = x[0].strip()
        self.orderClicked.emit()

    def setData(self, args):
        self.listWidget.clear()
        for x in args:
            self.listWidget.addItem(x)
