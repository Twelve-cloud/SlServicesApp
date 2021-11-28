# This Python file uses the following encoding: utf-8

from Views.initial_widget_view import InitialWidgetView
from PyQt5.QtCore import QObject, pyqtSignal

class InitialWidgetController(QObject):
    signalStartButtonClicked = pyqtSignal()

    def __init__(self, client):
        super(InitialWidgetController, self).__init__()
        self.view = InitialWidgetView(self)
        self.client = client

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def startButtonClicked(self):
        self.signalStartButtonClicked.emit()

    def windowDestroyed(self):
        self.client.sendToServer('EXIT')
