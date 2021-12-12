# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize

class ReportWidget(QWidget):
    txtButtonClicked = pyqtSignal()
    pdfButtonClicked = pyqtSignal()

    def __init__(self):
        super(ReportWidget, self).__init__()
        uic.loadUi('Form/report_form.ui', self)
        self.txtButton.clicked.connect(self.slotTxtButtonClicked)
        self.pdfButton.clicked.connect(self.slotPdfButtonClicked)

    def slotTxtButtonClicked(self):
        self.filename, state = QInputDialog.getText(self, "Get text", "Имя файла:", QLineEdit.Normal, "")
        if state:
            self.format = True
            self.txtButtonClicked.emit()

    def slotPdfButtonClicked(self):
        self.filename, state = QInputDialog.getText(self, "Get text", "Имя файла:", QLineEdit.Normal, "")
        if state:
            self.format = False
            self.pdfButtonClicked.emit()
