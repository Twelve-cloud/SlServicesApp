# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class AuthentificationWidget(QWidget):
    authentificationButtonClicked = pyqtSignal()
    registrationButtonClicked = pyqtSignal()

    def __init__(self):
        super(AuthentificationWidget, self).__init__()
        uic.loadUi('authentification_widget.ui', self)
        self.authentificationButton.clicked.connect(self.slotAuthentificationButtonClicked)
        self.registrationButton.clicked.connect(self.slotRegistrationButtonClicked)

    def slotAuthentificationButtonClicked(self):
        self.login = self.loginLineEdit.text()
        self.passw = self.passwLineEdit.text()
        self.authentificationButtonClicked.emit()

    def slotRegistrationButtonClicked(self):
        self.clearLines()
        self.registrationButtonClicked.emit()

    def clearLines(self):
        self.loginLineEdit.clear()
        self.passwLineEdit.clear()
        self.errorLabel.setText('Аутентификация')
        self.errorLabel.setStyleSheet('font-weight: 100; color: rgb(200, 200, 200);')

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red;')
