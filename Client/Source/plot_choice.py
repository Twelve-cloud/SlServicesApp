# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize

class PlotChoice(QWidget):
    histogramClicked = pyqtSignal()
    linearClicked = pyqtSignal()

    def __init__(self):
        super(PlotChoice, self).__init__()
        uic.loadUi('Form/plot_choice.ui', self)
        self.histogram.clicked.connect(lambda: self.histogramClicked.emit())
        self.linear.clicked.connect(lambda: self.linearClicked.emit())
