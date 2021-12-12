# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal, QSize

class UserMenu(QWidget):
    close = pyqtSignal()
    consultationButtonClicked = pyqtSignal()
    orderButtonClicked = pyqtSignal()

    def __init__(self):
        super(UserMenu, self).__init__()
        uic.loadUi('Form/user_menu_form.ui', self)
        self.consultationButton.clicked.connect(self.slotConstultationButtonClicked)
        self.showServiceButton.clicked.connect(self.slotShowServiceButtonClicked)
        self.hideServiceButton.clicked.connect(self.slotHideServiceButtonClicked)
        self.orderButton.clicked.connect(self.slotOrderButtonClicked)


    def slotConstultationButtonClicked(self):
        QMessageBox.about(self, "Уведомление", "Ваша заявка отправлена, находитесь онлайн")
        self.consultationButtonClicked.emit()

    def closeEvent(self, event):
        self.close.emit()

    def setServices(self, data):
        self.data = data
        self.serviceList.clear()
        for x in data:
            item = QListWidgetItem(x)
            item.setSizeHint(QSize (self.serviceList.width() - 20, 40));
            self.serviceList.addItem(item)

    def slotHideServiceButtonClicked(self):
        for x in range(len(self.serviceList)):
            self.serviceList.item(x).setHidden(True)
        self.serviceList.setStyleSheet("background: rgba(255, 0, 0, 0);")
        self.showServiceButton.setEnabled(True)
        self.hideServiceButton.setEnabled(False)

    def slotShowServiceButtonClicked(self):
        for x in range(len(self.serviceList)):
            self.serviceList.item(x).setHidden(False)
        self.serviceList.setStyleSheet("QserviceList::item {border: 1px solid rgb(100, 149, 237); margin: 0.5px; padding: 2px;}")
        self.hideServiceButton.setEnabled(True)
        self.showServiceButton.setEnabled(False)

    def slotOrderButtonClicked(self):
       service = self.serviceList.item(self.serviceList.currentRow()).text()
       msgBox = QMessageBox()
       msgBox.setIcon(QMessageBox.Information)
       msgBox.setText("Средняя цена: " + self.data[service])
       msgBox.setWindowTitle(service)
       msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

       returnValue = msgBox.exec()
       if returnValue == QMessageBox.Ok:
          self.currentService = service
          QMessageBox.about(self, "Уведомление", "Спасибо за оформление заказа! Брокер свяжется с вами в ближайщее время")
          self.orderButtonClicked.emit()

