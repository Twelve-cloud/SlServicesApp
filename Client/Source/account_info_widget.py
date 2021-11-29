# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt

from request_str_dialog import RequestStrDialog

class AccountInfoWidget(QWidget):
    saveButtonClicked = pyqtSignal()
    backButtonClicked = pyqtSignal()
    uploadThemeButtonClicked = pyqtSignal()
    deleteAccountButtonClicked = pyqtSignal()
    deletePhotoButtonClicked = pyqtSignal()
    uploadPhotoButtonClicked = pyqtSignal()

    def __init__(self):
        super(AccountInfoWidget, self).__init__()
        uic.loadUi('Form/account_info_widget.ui', self)
        self.saveSettingsButton.clicked.connect(self.slotSaveButtonClicked)
        self.backButton.clicked.connect(self.slotBackButtonClicked)
        self.deleteAccountButton.clicked.connect(self.slotDeleteAccountButtonClicked)
        self.passwLineEdit.setEchoMode(QLineEdit.Password)

    def slotBackButtonClicked(self):
        self.backButtonClicked.emit()

    def slotSaveButtonClicked(self):
        self.login = self.loginLineEdit.text()
        self.passw = self.passwLineEdit.text()
        self.mobnum = self.mobnumLineEdit.text()
        self.email = self.emailLineEdit.text()
        self.saveButtonClicked.emit()

    def slotDeleteAccountButtonClicked(self):
        self.dialog = RequestStrDialog()
        self.dialog.okButtonClicked.connect(self.slotDeleteConfirmClicked)
        self.dialog.show()

    def slotDeleteConfirmClicked(self):
        self.passw = self.dialog.target
        self.deleteAccountButtonClicked.emit()

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red;')

    def clearErrorMsg(self):
        self.errorLabel.setText('Личная информация')
        self.errorLabel.setStyleSheet('font-weight: 100; color: black;')

    def setInfo(self, data):
        login, passw, mobnum, email = data.split('~!#$~')
        self.loginLineEdit.setText(login)
        self.passwLineEdit.setText(passw)
        self.mobnumLineEdit.setText(mobnum)
        self.emailLineEdit.setText(email)
