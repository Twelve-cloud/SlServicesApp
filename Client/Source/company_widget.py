# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize

class CompanyWidget(QWidget):
    close = pyqtSignal()
    addButtonClicked = pyqtSignal()
    changeButtonClicked = pyqtSignal()
    deleteButtonClicked = pyqtSignal()
    itemDoubleClicked = pyqtSignal()

    def __init__(self):
        super(CompanyWidget, self).__init__()
        uic.loadUi('Form/company_form.ui', self)
        self.companies = []
        self.selected_company = None
        self.addButton.clicked.connect(self.slotAddButtonClicked)
        self.changeButton.clicked.connect(self.slotChangeButtonClicked)
        self.deleteButton.clicked.connect(self.slotDeleteButtonClicked)
        self.sortButton.clicked.connect(self.slotSortButtonClicked)
        self.findButton.clicked.connect(self.slotFindButtonClicked)
        self.returnButton.clicked.connect(self.slotReturnButtonClicked)
        self.listWidget.itemDoubleClicked.connect(self.slotItemDoubleClicked)

    def closeEvent(self, event):
        self.close.emit()

    def slotAddButtonClicked(self):
        text, state = QInputDialog.getText(self, "Get text", "Имя компании:", QLineEdit.Normal, "")
        if state:
            if len(text) < 6 or len(text) > 16 or not all(x.isalpha() or x.isspace() for x in text):
                self.setError('Имя копании должно быть от 6 до 16 и содержать буквы и цифры')
            elif text in self.companies:
                self.setError('Такая компания уже существует')
            else:
                self.selected_company = text
                self.companies.append(text)
                self.listWidget.clear()
                for x in self.companies:
                    self.listWidget.addItem(x)
                self.addButtonClicked.emit()

    def slotChangeButtonClicked(self):
        if (item := self.listWidget.currentItem()):
            takedItem = self.listWidget.item(self.listWidget.row(item))
            self.selected_company = takedItem.text()
            text, state = QInputDialog.getText(self, "Get text", "Имя компании:", QLineEdit.Normal, "")
            if state:
                if len(text) < 6 or len(text) > 16 or not all(x.isalpha() or x.isspace() for x in text):
                    self.setError('Имя копании должно быть от 6 до 16')
                elif text in self.companies:
                    self.setError('Такая компания уже существует')
                else:
                    self.new_name = text
                    for index, company in enumerate(self.companies):
                        if company == self.selected_company:
                            self.companies[index] = self.new_name
                    self.listWidget.clear()
                    for x in self.companies:
                        self.listWidget.addItem(x)
                    self.changeButtonClicked.emit()
        else:
            self.setError("Выберите элемент в списке")

    def slotDeleteButtonClicked(self):
        if (item := self.listWidget.currentItem()):
            takedItem = self.listWidget.takeItem(self.listWidget.row(item))
            self.selected_company = takedItem.text()
            self.companies.remove(takedItem.text())
            self.listWidget.clear()
            for x in self.companies:
                self.listWidget.addItem(x)
            self.deleteButtonClicked.emit()
        else:
            self.setError("Выберите элемент в списке")

    def slotSortButtonClicked(self):
        self.clearError()
        self.companies = list(reversed(self.companies))
        self.listWidget.clear()
        for x in self.companies:
            self.listWidget.addItem(x)

    def slotFindButtonClicked(self):
        self.clearError()
        text, state = QInputDialog.getText(self, "Get text", "Имя компании:", QLineEdit.Normal, "")
        self.listWidget.clear()
        for x in self.companies:
            if text in x:
                self.listWidget.addItem(x)

    def slotReturnButtonClicked(self):
        self.clearError()
        self.listWidget.clear()
        for x in self.companies:
            self.listWidget.addItem(x)

    def setError(self, error):
        self.errorLabel.setText(error)
        self.errorLabel.setStyleSheet('font-weight: 100; color: red;')

    def clearError(self):
        self.errorLabel.setText('')
        self.errorLabel.setStyleSheet('font-weight: 100; color: black')

    def setCompanies(self, args):
        self.companies = []
        self.listWidget.clear()
        for x in args:
            self.companies.append(x)
            self.listWidget.addItem(x)

    def slotItemDoubleClicked(self, item):
        self.selected_company = item.text()
        self.itemDoubleClicked.emit()
