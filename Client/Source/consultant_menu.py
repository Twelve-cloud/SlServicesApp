# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize

class ConsultationMenu(QWidget):
    close = pyqtSignal()
    cancelConsultation = pyqtSignal()
    createConsultation = pyqtSignal()

    def __init__(self):
        super(ConsultationMenu, self).__init__()
        uic.loadUi('Form/consultant_menu_form.ui', self)
        self.showRequests.clicked.connect(self.slotShowRequestsClicked)
        self.hideRequests.clicked.connect(self.slotHideRequestsClicked)
        self.cancelConsultationButton.clicked.connect(self.slotCancelConsultationClicked)
        self.createConsultationButton.clicked.connect(self.slotCreateConsultationButtonClicked)

        self.listWidget.setStyleSheet("QListWidget::item {border: 1px solid rgb(100, 149, 237); margin: 0.5px; padding: 2px;}")

    def closeEvent(self, event):
        self.close.emit()

    def slotShowRequestsClicked(self):
        for x in range(len(self.listWidget)):
            self.listWidget.item(x).setHidden(False)
        self.listWidget.setStyleSheet("QListWidget::item {border: 1px solid rgb(100, 149, 237); margin: 0.5px; padding: 2px;}")
        self.hideRequests.setEnabled(True)
        self.showRequests.setEnabled(False)

    def slotHideRequestsClicked(self):
        for x in range(len(self.listWidget)):
            self.listWidget.item(x).setHidden(True)
        self.listWidget.setStyleSheet("background: rgba(255, 0, 0, 0);")
        self.showRequests.setEnabled(True)
        self.hideRequests.setEnabled(False)

    def slotCancelConsultationClicked(self):
        if (item := self.listWidget.currentItem()):
            self.label.setText('')
            self.label.setStyleSheet('font-weight: 100; color: black; background: rgba(255, 0, 0, 0);')
            takedItem = self.listWidget.takeItem(self.listWidget.row(item))
            self.currentUser = takedItem.text().split()
            self.currentUser = self.currentUser[0]
            self.cancelConsultation.emit()
        else:
            self.setError("Выберите элемент в списке")

    def slotCreateConsultationButtonClicked(self):
        if (item := self.listWidget.currentItem()):
            self.label.setText('')
            self.label.setStyleSheet('font-weight: 100; color: black; background: rgba(255, 0, 0, 0);')
            takedItem = self.listWidget.takeItem(self.listWidget.row(item))
            self.currentUser = takedItem.text().split()
            self.currentUser = self.currentUser[0]
            self.createConsultation.emit()
        else:
            self.setError("Выберите элемент в списке")

    def setConsultation(self, data):
        self.listWidget.clear()
        for x in data:
            item = QListWidgetItem(x)
            item.setSizeHint(QSize (self.listWidget.width() - 20, 40));
            self.listWidget.addItem(item)

    def setError(self, error):
        self.label.setStyleSheet('font-weight: 100; color: red; background: rgba(255, 0, 0, 0);')
        self.label.setText(error)


    def clearList(self):
        self.listWidget.clear()
