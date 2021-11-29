# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

class RequestStrDialog(QDialog):
        okButtonClicked = pyqtSignal()
        def __init__(self):
            super(RequestStrDialog, self).__init__()
            uic.loadUi('Form/request_str_form.ui', self)
            self.okButton.clicked.connect(self.slotOkButton)
            self.cancelButton.clicked.connect(self.slotCancelButton)

        def slotOkButton(self):
            self.target = self.lineEdit.text()
            self.okButtonClicked.emit()
            self.close()

        def slotCancelButton(self):
            self.close()
