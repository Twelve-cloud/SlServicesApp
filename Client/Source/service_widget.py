# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize

class ServiceWidget(QWidget):
    close = pyqtSignal()
    addButtonClicked = pyqtSignal()
    changeButtonClicked = pyqtSignal()
    deleteButtonClicked = pyqtSignal()

    def __init__(self):
        super(ServiceWidget, self).__init__()
        uic.loadUi('Form/service_form.ui', self)
        self.services = []
        self.selected_service = None
        self.addServiceButton.clicked.connect(self.slotAddButtonClicked)
        self.changeServiceButton.clicked.connect(self.slotChangeButtonClicked)
        self.deleteServiceButton.clicked.connect(self.slotDeleteButtonClicked)
        self.sortServiceButton.clicked.connect(self.slotSortButtonClicked)
        self.findServiceButton.clicked.connect(self.slotFindButtonClicked)
        self.returnServiceButton.clicked.connect(self.slotReturnButtonClicked)

    def closeEvent(self, event):
        self.close.emit()

    def slotAddButtonClicked(self):
        self.service, state_service = QInputDialog.getText(self, "Get text", "Имя услуги:", QLineEdit.Normal, "")
        self.price, state_price = QInputDialog.getText(self, "Get text", "Цена услуги:", QLineEdit.Normal, "")
        if state_service and state_price:
            if len(self.service) < 6 or len(self.service) > 32 or not all(x.isalpha() or x.isspace() for x in self.service):
                self.setError('Имя услуги должно быть от 6 до 32 и содержать буквы и цифры')
            else:
                for x in self.services:
                    if self.service in x:
                        self.setError('Такая услуга уже существует')
                        return

                try:
                    float(self.price)
                except Exception:
                    self.setError('Ошибка ввода цены')
                    return

                self.selected_service = self.service + ' [' + self.price + ']'
                self.services.append(self.selected_service)
                self.listServiceWidget.clear()
                for x in self.services:
                    self.listServiceWidget.addItem(x)
                self.addButtonClicked.emit()

    def slotChangeButtonClicked(self):
        if (item := self.listServiceWidget.currentItem()):
            takedItem = self.listServiceWidget.item(self.listServiceWidget.row(item))
            self.selected_service = takedItem.text()
            self.price, state_price = QInputDialog.getText(self, "Get text", "Цена услуги:", QLineEdit.Normal, "")
            if state_price:
                try:
                    float(self.price)
                except Exception:
                    self.setError('Ошибка ввода цены')
                    return

                self.new_name = self.selected_service[:self.selected_service.find('[')]
                self.service = self.new_name.strip()
                self.new_name = self.new_name + '[' + self.price + ']'
                for index, service in enumerate(self.services):
                    if service == self.selected_service:
                        self.services[index] = self.new_name
                        self.listServiceWidget.clear()
                for x in self.services:
                    self.listServiceWidget.addItem(x)
                self.changeButtonClicked.emit()
        else:
            self.setError("Выберите элемент в списке")

    def slotDeleteButtonClicked(self):
        if (item := self.listServiceWidget.currentItem()):
            takedItem = self.listServiceWidget.takeItem(self.listServiceWidget.row(item))
            self.selected_service = takedItem.text().split('[')
            self.service = self.selected_service[0].strip()
            self.services.remove(takedItem.text())
            self.listServiceWidget.clear()
            for x in self.services:
                self.listServiceWidget.addItem(x)
            self.deleteButtonClicked.emit()
        else:
            self.setError("Выберите элемент в списке")

    def slotSortButtonClicked(self):
        self.clearError()
        self.services = list(reversed(self.services))
        self.listServiceWidget.clear()
        for x in self.services:
            self.listServiceWidget.addItem(x)

    def slotFindButtonClicked(self):
        self.clearError()
        text, state = QInputDialog.getText(self, "Get text", "Данные об услуге:", QLineEdit.Normal, "")
        self.listServiceWidget.clear()
        for x in self.services:
            if text in x:
                self.listServiceWidget.addItem(x)

    def slotReturnButtonClicked(self):
        self.clearError()
        self.listServiceWidget.clear()
        for x in self.services:
            self.listServiceWidget.addItem(x)

    def setError(self, error):
        self.errorServiceLabel.setText(error)
        self.errorServiceLabel.setStyleSheet('font-weight: 100; color: red;')

    def clearError(self):
        self.errorServiceLabel.setText('')
        self.errorServiceLabel.setStyleSheet('font-weight: 100; color: black')

    def setServices(self, args):
        self.services = []
        self.listServiceWidget.clear()
        for x in args:
            self.services.append(x)
            self.listServiceWidget.addItem(x)
