# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QFile, QDir, QSize
from PyQt5.QtGui import QPixmap, QPalette, QImage, QBrush

from request_str_dialog import RequestStrDialog

class AccountInfoWidget(QWidget):
    saveButtonClicked = pyqtSignal()
    deleteAccountButtonClicked = pyqtSignal()
    uploadThemeButtonClicked = pyqtSignal()
    deleteThemeButtonClicked = pyqtSignal()

    def __init__(self):
        super(AccountInfoWidget, self).__init__()
        uic.loadUi('Form/account_info_widget.ui', self)
        self.saveSettingsButton.clicked.connect(self.slotSaveButtonClicked)
        self.deleteAccountButton.clicked.connect(self.slotDeleteAccountButtonClicked)
        self.uploadPhotoButton.clicked.connect(self.slotUploadPhotoClicked)
        self.deletePhotoButton.clicked.connect(self.slotDeletePhotoClicked)
        self.backgroundButton.clicked.connect(self.slotUploadThemeClicked)
        self.backgroundDeleteButton.clicked.connect(self.slotDeleteThemeButtonClicked)
        self.passwLineEdit.setEchoMode(QLineEdit.Password)

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
        currentDir = QDir(QDir.currentPath() + '/' + self.loginLineEdit.text())
        currentDir.removeRecursively()
        self.passw = self.dialog.target
        self.deleteAccountButtonClicked.emit()

    def slotUploadPhotoClicked(self):
        filename = QFileDialog.getOpenFileName(self, "Выберите файл", QDir.homePath())
        currentDir = QDir(QDir.currentPath())
        currentDir.mkdir(self.loginLineEdit.text())
        QFile.remove(QDir.currentPath() + '/' + self.loginLineEdit.text() + '/profile_photo.jpg')
        QFile.copy(filename[0], QDir.currentPath() + '/' + self.loginLineEdit.text() + '/profile_photo.jpg')
        self.photoLabel.setPixmap(QPixmap(self.loginLineEdit.text() + '/profile_photo.jpg').scaled(240, 240))

    def slotDeletePhotoClicked(self):
        if QFile.exists(self.loginLineEdit.text() + '/profile_photo.jpg'):
            QFile.remove(QDir.currentPath() + '/' + self.loginLineEdit.text() + '/profile_photo.jpg')
            self.photoLabel.clear()

    def slotUploadThemeClicked(self):
        self.uploadThemeButtonClicked.emit()

    def slotDeleteThemeButtonClicked(self):
        self.deleteThemeButtonClicked.emit()

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red; background: rgba(255, 0, 0, 0);')

    def clearErrorMsg(self):
        self.errorLabel.setText('')
        self.errorLabel.setStyleSheet('font-weight: 100; color: black; background: rgba(255, 0, 0, 0);')

    def setInfo(self, data):
        login, passw, mobnum, email = data.split('~!#$~')
        self.loginLineEdit.setText(login)
        self.passwLineEdit.setText(passw)
        self.mobnumLineEdit.setText(mobnum)
        self.emailLineEdit.setText(email)
        if QFile.exists(self.loginLineEdit.text() + '/profile_photo.jpg'):
            self.photoLabel.setPixmap(QPixmap(self.loginLineEdit.text() + '/profile_photo.jpg').scaled(240, 240))
