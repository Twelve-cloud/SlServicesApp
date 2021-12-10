# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal

class UserMenu(QWidget):
    close = pyqtSignal()
    consultationButtonClicked = pyqtSignal()

    def __init__(self):
        super(UserMenu, self).__init__()
        uic.loadUi('Form/user_menu_form.ui', self)
        self.consultationButton.clicked.connect(self.slotConstultationButtonClicked)


    def slotConstultationButtonClicked(self):
        QMessageBox.about(self, "Уведомление", "Ваша заявка отправлена, находитесь онлайн")
        self.consultationButtonClicked.emit()

    def closeEvent(self, event):
        self.close.emit()
