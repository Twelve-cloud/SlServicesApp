# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt

class AuthentificationWidget(QWidget):
    authentificationButtonClicked = pyqtSignal()
    registrationButtonClicked = pyqtSignal()

    def __init__(self):
        super(AuthentificationWidget, self).__init__()
        uic.loadUi('Form/authentification_widget.ui', self)
        self.authentificationButton.clicked.connect(self.slotAuthentificationButtonClicked)
        self.registrationButton.clicked.connect(self.slotRegistrationButtonClicked)
        self.passwLineEdit.setEchoMode(QLineEdit.Password)

    def slotAuthentificationButtonClicked(self):
        self.login = self.loginLineEdit.text()
        self.passw = self.passwLineEdit.text()

        if self.isEmptyLines():
            self.setError('Ошибка аутентификации')
        else:
            self.authentificationButtonClicked.emit()

    def slotRegistrationButtonClicked(self):
        self.clearLines()
        self.registrationButtonClicked.emit()

    def clearLines(self):
        self.loginLineEdit.clear()
        self.passwLineEdit.clear()
        self.errorLabel.setText('Аутентификация')
        self.errorLabel.setStyleSheet('font-weight: 100; color: black')

    def isEmptyLines(self):
        if self.login == '' or self.passw == '':
            return True
        return False

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red;')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down and self.loginLineEdit == QApplication.focusWidget():
            self.passwLineEdit.setFocus()
        elif event.key() == Qt.Key_Up and self.passwLineEdit == QApplication.focusWidget():
            self.loginLineEdit.setFocus()
