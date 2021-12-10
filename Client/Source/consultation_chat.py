# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, Qt, QSize

class ConsultationChat(QWidget):
    sendMessage = pyqtSignal()
    finishChat = pyqtSignal()
    def __init__(self):
        super(ConsultationChat, self).__init__()
        uic.loadUi('Form/consultation_chat_form.ui', self)
        self.sendMessageButton.clicked.connect(self.slotSendMessageClicked)
        self.finishChatButton.clicked.connect(self.slotFinishChatClicked)

        self.chatWidget.setStyleSheet("QListWidget::item {border-radius: 13px; border: 1px solid rgb(100, 149, 237); margin: 0.5px; padding: 3px;}")

    def setParticipants(self, login, companion):
        self.login = login
        self.companion = companion

    def slotSendMessageClicked(self):
        self.message = self.messageLineEdit.text()
        self.messageLineEdit.clear()
        item = QListWidgetItem("Я: " + self.message)
        item.setSizeHint (QSize (self.chatWidget.width() - 20, 35));
        self.chatWidget.addItem(item)
        self.sendMessage.emit()

    def slotFinishChatClicked(self):
        self.messageLineEdit.clear()
        self.finishChat.emit()

    def setMessage(self, companion, message):
        item = QListWidgetItem(companion + ": " + message)
        item.setSizeHint (QSize (self.chatWidget.width() - 20, 35));
        self.chatWidget.addItem(item)

    def clearLine(self):
        if self.messageLineEdit.text():
            self.messageLineEdit.clear()
