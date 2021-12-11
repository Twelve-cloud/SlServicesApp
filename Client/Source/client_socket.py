# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

class ClientSocket(QWidget):
    onReadyRead = pyqtSignal()
    def __init__(self, address, port):
        super(ClientSocket, self).__init__()
        self.sock = QTcpSocket()
        self.sock.connectToHost(address, port)
        self.sock.readyRead.connect(self.slotReadyRead)

    def slotReadyRead(self):
        self.data = self.sock.read(4096)
        self.onReadyRead.emit()

    def get_data(self):
        return self.data.decode()

    def sendToServer(self, msg):
        msg = msg.encode()
        size = len(msg)
        size_bytes = size.to_bytes(16, 'little', signed = False)
        self.sock.write(size_bytes)
        self.sock.write(msg)

    def close(self):
        self.sock.close()
