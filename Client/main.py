# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from stack_of_controllers import StackOfControllers

from Controllers.initial_controller import InitialController
from Controllers.authentification_controller import AuthentificationController
from Controllers.registration_controller import RegistrationController

class MainWindow(QMainWindow):
    def __init__(self, client):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.client = client
        self.stack_of_controllers = StackOfControllers()

        self.init_controller = InitialController(client)
        self.auth_controller = AuthentificationController(client)
        self.regi_controller = RegistrationController(client)

        self.stack_of_controllers.push(self.init_controller)

if __name__ == "__main__":
    app = QApplication([])
    client = Client('localhost', 6606)
    main_window = MainWindow(client)
    sys.exit(app.exec_())
