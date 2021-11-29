# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt

class RegistrationWidget(QWidget):
    createButtonClicked = pyqtSignal()
    backButtonClicked = pyqtSignal()

    def __init__(self):
        super(RegistrationWidget, self).__init__()
        uic.loadUi('Form/registration_widget.ui', self)
        self.createButton.clicked.connect(self.slotCreateButtonClicked)
        self.backButton.clicked.connect(self.slotBackButtonClicked)
        self.passwLineEdit.setEchoMode(QLineEdit.Password)
        self.againPasswLineEdit.setEchoMode(QLineEdit.Password)

    def slotCreateButtonClicked(self):
        self.login = self.loginLineEdit.text()
        self.passw = self.passwLineEdit.text()

        if self.passw != self.againPasswLineEdit.text():
            self.setError('Пароли не совпадают')
        elif len(self.login) < 6 or len(self.login) > 16:
            self.setError('Логин должен содержать от 6 до 16 символов')
        elif len(self.passw) < 6 or len(self.passw) > 32:
            self.setError('Пароль должен содержать от 6 до 32 символов')
        elif not self.login.isalnum() or not self.login.isalnum():
            self.setError('Логин состоит из латанских символов, цифр')
        elif not self.passw.isalnum() or not self.passw.isalnum():
            self.setError('Пароль состоит из латанских символов, цифр')
        else:
            self.createButtonClicked.emit()

    def slotBackButtonClicked(self):
        self.clearLines()
        self.backButtonClicked.emit()

    def clearLines(self):
        self.loginLineEdit.clear()
        self.passwLineEdit.clear()
        self.againPasswLineEdit.clear()
        self.errorLabel.setText('Регистрация')
        self.errorLabel.setStyleSheet('font-weight: 100; color: black;')

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


