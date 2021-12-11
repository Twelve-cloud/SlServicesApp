# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter


class Histogram(QWidget):
    def __init__(self):
        super(Histogram, self).__init__()
        uic.loadUi('Form/histogram.ui', self)

    def createHistogram(self):
        set0 = QBarSet('X0')
        set1 = QBarSet('X1')
        set2 = QBarSet('X2')
        set3 = QBarSet('X3')
        set4 = QBarSet('X4')

        set0.append([1, 2, 3, 4, 5, 6])


        series = QHorizontalBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QChart()
        chart.resize(700, 400)
        chart.addSeries(series)
        chart.setTitle('График средних цен и дисперсии цен')

        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisY = QValueAxis()
        axisY.setRange(0, 1000)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.gridLayout.addWidget(chartView)

    def setServices(self, args):
        args = list(set(args))
        for x in args:
            self.comboBox.addItem(x)

    def currName(self):
        return str(self.comboBox.currentText())

    def slotSelectOption(self):
        self.selOption.emit()
