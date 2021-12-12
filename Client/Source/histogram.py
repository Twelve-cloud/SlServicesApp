# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter


class Histogram(QWidget):
    selOption = pyqtSignal()

    def __init__(self):
        super(Histogram, self).__init__()
        uic.loadUi('Form/histogram.ui', self)
        self.comboBox.activated[str].connect(self.slotSelectOption)

    def createHistogram(self, std, companies_prices):
        print(companies_prices, std)
        chart = QChart()
        chart.resize(700, 400)
        chart.setTitle('График средних цен и дисперсии цен')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        series = QBarSeries()

        for x in range(len(companies_prices)):
            set = QBarSet(companies_prices[x])
            set.append(float(std[x]))
            series.append(set)

        chart.addSeries(series)

        axisY = QValueAxis()
        axisY.setRange(0, 10000)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        if self.gridLayout.count() == 2:
            self.gridLayout.itemAt(self.gridLayout.count() - 1).widget().setParent(None)
        self.gridLayout.addWidget(chartView)

    def setServices(self, args):
        args = list(set(args))
        for x in args:
            self.comboBox.addItem(x)

    def currName(self):
        return str(self.comboBox.currentText())

    def slotSelectOption(self):
        self.selOption.emit()
