# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
import string

class RegistrationWidget(QWidget):
    createButtonClicked = pyqtSignal()
    backButtonClicked = pyqtSignal()

    def __init__(self, client):
        super(RegistrationWidget, self).__init__()
        uic.loadUi('registration_widget.ui', self)
        self.client = client
        self.createButton.clicked.connect(self.slotCreateButtonClicked)
        self.backButton.clicked.connect(self.slotBackButtonClicked)
        self.passwLineEdit.setEchoMode(QLineEdit.Password)
        self.againPasswLineEdit.setEchoMode(QLineEdit.Password)

    def slotCreateButtonClicked(self):
        self.login = self.loginLineEdit.text()
        self.passw = self.passwLineEdit.text()

        if self.passw != self.againPasswLineEdit.text():
            self.setError('Пароли не совпадают')

        self.createButtonClicked.emit()

    def slotBackButtonClicked(self):
        self.clearLines()
        self.backButtonClicked.emit()

    def clearLines(self):
        self.loginLineEdit.clear()
        self.passwLineEdit.clear()
        self.againPasswLineEdit.clear()
        self.errorLabel.setText('Регистрация')
        self.errorLabel.setStyleSheet('font-weight: 100; color: rgb(200, 200, 200);')

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red;')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down and self.loginLineEdit == QApplication.focusWidget():
            self.passwLineEdit.setFocus()
        elif event.key() == Qt.Key_Up and self.passwLineEdit == QApplication.focusWidget():
            self.loginLineEdit.setFocus()
        elif event.key() == Qt.Key_Down and self.passwLineEdit == QApplication.focusWidget():
            self.againPasswLineEdit.setFocus()
        elif event.key() == Qt.Key_Up and self.againPasswLineEdit == QApplication.focusWidget():
            self.passwLineEdit.setFocus()


