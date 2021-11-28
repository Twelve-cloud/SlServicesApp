# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class InitialWidgetView(QWidget):
    def __init__(self, controller):
        super(InitialWidgetView, self).__init__()
        uic.loadUi('Forms/initial_form.ui', self)

        self.controller = controller

        self.startButton.clicked.connect(self.controller.startButtonClicked)
        self.destroyed.connect(self.controller.windowDestroyed)
