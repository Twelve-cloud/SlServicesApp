# This Python file uses the following encoding: utf-8

from socket import *

class ClientSocket:
    def __init__(self, address, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((address, port))

    def sendToServer(self, msg):
        self.sock.send(msg.encode())

    def getRespond(self):
        return self.sock.recv(4096).decode()


    def close(self):
        self.sock.close()
