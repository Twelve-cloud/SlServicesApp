# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class LinearPlot(QWidget):
    selOption = pyqtSignal()

    def __init__(self):
        super(LinearPlot, self).__init__()
        uic.loadUi('Form/linear_plot.ui', self)
        self.comboBox.activated[str].connect(self.slotSelectOption)


    def createLinearPlot(self, companies, prices):
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.label.setText(', '.join(companies))
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(range(len(companies)), prices, pen = pen)
        if self.gridLayout.count() == 3:
            self.gridLayout.itemAt(self.gridLayout.count() - 1).widget().setParent(None)
        self.gridLayout.addWidget(self.graphWidget)

    def setServices(self, args):
        args = list(set(args))
        for x in args:
            self.comboBox.addItem(x)

    def currName(self):
        return str(self.comboBox.currentText())

    def slotSelectOption(self):
        self.selOption.emit()
