# This Python file uses the following encoding: utf-8
import sys
from socket import *

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from initial_widget_controller import InitialWidgetController
from authentification_widget import AuthentificationWidget
from registration_widget import RegistrationWidget

class MainWindow(QMainWindow):
    def __init__(self, adress, port):
        super(MainWindow, self).__init__()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('localhost', 6606))
        uic.loadUi('form.ui', self)

        self.init_wdg = InitialWidgetController()
        self.init_wdg.signalStartButtonClicked.connect(self.slotStartButtonClicked)
        self.init_wdg.show()

        self.auth_wdg = AuthentificationWidget()
        self.auth_wdg.authentificationButtonClicked.connect(self.slotAuthentificationButtonClicked)
        self.auth_wdg.registrationButtonClicked.connect(self.slotRegistrationButtonClicked)

        self.regi_wdg = RegistrationWidget()
        self.regi_wdg.createButtonClicked.connect(self.slotCreateButtonClicked)
        self.regi_wdg.backButtonClicked.connect(self.slotBackButtonClicked)

    def slotStartButtonClicked(self):
        self.init_wdg.close()     
        self.auth_wdg.show()

    def slotAuthentificationButtonClicked(self):
        self.sendToServer('SIGN IN~!#$~' + self.auth_wdg.login + '~!#$~' + self.auth_wdg.passw)

    def slotRegistrationButtonClicked(self):
        self.auth_wdg.close()
        self.regi_wdg.show()

    def slotCreateButtonClicked(self):
        self.sendToServer('REGISTRATION ACCOUNT~!#$~login:' + self.regi_wdg.login + '~!#$~password:' + self.regi_wdg.passw)
        respond_encoded = self.sock.recv(4096)
        respond = respond_encoded.decode('utf-8')
        print(respond)

    def slotBackButtonClicked(self):
        self.regi_wdg.close()
        self.auth_wdg.show()

    def sendToServer(self, msg):
        self.sock.send(msg.encode('utf-8'))



if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow('localhost', 6606)
    sys.exit(app.exec_())
