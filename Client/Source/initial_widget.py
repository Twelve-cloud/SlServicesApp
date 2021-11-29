# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class InitialWidget(QWidget):
    startButtonClicked = pyqtSignal()

    def __init__(self):
        super(InitialWidget, self).__init__()
        uic.loadUi('Form/initial_widget.ui', self)
        self.startButton.clicked.connect(lambda: self.startButtonClicked.emit())
