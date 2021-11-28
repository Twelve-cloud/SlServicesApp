# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class InitialWidgetView(QWidget):
    def __init__(self, controller):
        super(InitialWidgetView, self).__init__()
        self.controller = controller

        uic.loadUi('initial_widget_form.ui', self)
        self.startButton.clicked.connect(self.controller.startButtonClicked)
