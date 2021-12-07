# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QMdiArea, QWidget, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QFile, QDir, QSize
from PyQt5.QtGui import QPixmap, QPalette, QImage, QBrush

from client_socket import ClientSocket
from stack_of_widgets import StackOfWidgets

from initial_widget import InitialWidget
from authentification_widget import AuthentificationWidget
from registration_widget import RegistrationWidget
from account_info_widget import AccountInfoWidget

class MainWindow(QMainWindow):
    def __init__(self, client_socket):
        super(MainWindow, self).__init__()
        uic.loadUi('Form/main_window_form.ui', self)

        self.client_socket = client_socket
        self.stack_of_widgets = StackOfWidgets()

        self.init_wdg = InitialWidget()
        self.auth_wdg = AuthentificationWidget()
        self.regi_wdg = RegistrationWidget()

        self.init_wdg.startButtonClicked.connect(self.slotInitStartButtonClicked)

        self.auth_wdg.authentificationButtonClicked.connect(self.slotAuthentificationButtonClicked)
        self.auth_wdg.registrationButtonClicked.connect(self.slotRegistrationButtonClicked)

        self.regi_wdg.createButtonClicked.connect(self.slotCreateAccountButtonClicked)
        self.regi_wdg.backButtonClicked.connect(self.slotBackFromRegistrationButtonClicked)

        self.accInfo.triggered.connect(self.slotAccInfoButtonClicked)
        self.quitAccount.triggered.connect(self.slotQuitAccountClicked)
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        self.setWindowTitle('')
        self.stack_of_widgets.push(self.init_wdg)
        self.sourcePalette = None

        if QFile.exists(self.auth_wdg.loginLineEdit.text() + '/background.jpg'):
            self.sourcePalette = self.palette()
            originalImage = QImage(QDir.currentPath() + '/' + self.auth_wdg.loginLineEdit.text() + '/background.jpg')
            scaledImage = originalImage.scaled(QSize(self.frameGeometry().width(), self.frameGeometry().height()))
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(scaledImage))
            self.mdiArea.setBackground(QBrush(scaledImage))

    def slotInitStartButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)

    def slotAuthentificationButtonClicked(self):
        self.client_socket.sendToServer('SIGN IN ACCOUNT~!#$~login:' + self.auth_wdg.login + '~!#$~password:' + self.auth_wdg.passw)
        respond = self.client_socket.getRespond()
        self.handleRespond(respond)

    def slotRegistrationButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.regi_wdg)

    def slotCreateAccountButtonClicked(self):
        self.client_socket.sendToServer('REGISTRATION ACCOUNT~!#$~login:' + self.regi_wdg.login + '~!#$~password:' + self.regi_wdg.passw)
        respond = self.client_socket.getRespond()
        self.handleRespond(respond)

    def slotBackFromRegistrationButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)

    def slotAccInfoButtonClicked(self):
        self.info_wdg = AccountInfoWidget()
        self.info_wdg.saveButtonClicked.connect(self.slotSaveAccountInfoButtonClicked)
        self.info_wdg.deleteAccountButtonClicked.connect(self.slotDeleteAccountButtonClicked)
        self.info_wdg.uploadThemeButtonClicked.connect(self.slotUploadThemeButtonClicked)
        self.info_wdg.deleteThemeButtonClicked.connect(self.slotDeleteThemeButtonClicked)
        self.client_socket.sendToServer('GET ACCOUNT INFO~!#$~login:' + self.auth_wdg.login)
        respond = self.client_socket.getRespond()
        self.info_wdg.setInfo(respond)
        self.info_wdg.clearErrorMsg()
        wnd = self.mdiArea.addSubWindow(self.info_wdg)
        wnd.setWindowTitle('Личная информация')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotUploadThemeButtonClicked(self):
        filename = QFileDialog.getOpenFileName(self, "Выберите файл", QDir.homePath())
        currentDir = QDir(QDir.currentPath())
        currentDir.mkdir(self.info_wdg.loginLineEdit.text())
        QFile.remove(QDir.currentPath() + '/' + self.info_wdg.loginLineEdit.text() + '/background.jpg')
        QFile.copy(filename[0], QDir.currentPath() + '/' + self.info_wdg.loginLineEdit.text() + '/background.jpg')
        originalImage = QImage(QDir.currentPath() + '/' + self.info_wdg.loginLineEdit.text() + '/background.jpg')
        scaledImage = originalImage.scaled(QSize(self.frameGeometry().width(), self.frameGeometry().height()))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaledImage))
        if not self.sourcePalette:
            self.sourcePalette = self.palette()
        self.setPalette(palette)

    def slotDeleteThemeButtonClicked(self):
        if QFile.exists(self.info_wdg.loginLineEdit.text() + '/background.jpg'):
            QFile.remove(QDir.currentPath() + '/' + self.info_wdg.loginLineEdit.text() + '/background.jpg')
            self.setPalette(self.sourcePalette)

    def resizeEvent(self, event):
        if QFile.exists(self.auth_wdg.loginLineEdit.text() + '/background.jpg'):
            palette = QPalette()
            img = QImage(QDir.currentPath() + '/' + self.auth_wdg.loginLineEdit.text() + '/background.jpg')
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)

    def slotQuitAccountClicked(self):
        self.auth_wdg.clearLines()
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)

    def slotSaveAccountInfoButtonClicked(self):
        self.client_socket.sendToServer('REDO ACCOUNT INFO~!#$~login:' + self.info_wdg.login + '~!#$~password:' + self.info_wdg.passw + '~!#$~mob_num:' + self.info_wdg.mobnum + '~!#$~email:' + self.info_wdg.email)
        respond = self.client_socket.getRespond()
        self.handleRespond(respond)

    def slotDeleteAccountButtonClicked(self):
        if self.info_wdg.passw == self.auth_wdg.passw:
            self.client_socket.sendToServer('DELETE ACCOUNT~!#$~login:' + self.auth_wdg.login)
            respond = self.client_socket.getRespond()
            self.handleRespond(respond)
        else:
            QMessageBox.about(self, "Уведомление", "Неверный пароль")

    def closeEvent(self, event):
        self.client_socket.sendToServer('EXIT')

    def handleRespond(self, respond):
        respond_list = respond.split('~!#$~')

        if len(respond_list) == 1:
            command = respond_list[0]
        elif len(respond_list) == 2:
            command, args = respond_list

        if command == 'REGISTRATION FAILED':
            self.regi_wdg.setError('Ошибка регистрации')
        elif command == 'REGISTRATION SUCCESSFUL':
            self.regi_wdg.clearLines()
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self.auth_wdg)
            QMessageBox.about(self, "Уведомление", "Регистрация успешна")
        elif command == 'AUTHENTIFICATION FAILED':
            self.auth_wdg.setError(args)
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args == 'USER':
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args == 'CONSULTANT':
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args == 'BROKER':
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
        elif command == 'REDO ACC INFO SUCCESS':
            self.auth_wdg.passw = self.info_wdg.passw
            QMessageBox.about(self, "Уведомление", "Данные изменены успешно")
            self.info_wdg.setError('')
        elif command == 'REDO ACC INFO FAILED':
            self.info_wdg.setError('Ошибка. Некорректные данные')
        elif command == 'DELETING SUCCESSFUL':
            QMessageBox.about(self, "Уведомление", "Аккаунт удален")
            self.auth_wdg.clearLines()
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self.auth_wdg)
        elif command == 'DELETING FAILED':
            QMessageBox.about(self, "Уведомление", "Ошибка удаления аккаунта")


if __name__ == "__main__":
    app = QApplication([])
    client_socket = ClientSocket('localhost', 6606)
    main_window = MainWindow(client_socket)
    sys.exit(app.exec_())
