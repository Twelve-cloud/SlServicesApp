# This Python file uses the following encoding: utf-8

from initial_widget_view import InitialWidgetView
from PyQt5.QtCore import QObject, pyqtSignal

class InitialWidgetController(QObject):
    signalStartButtonClicked = pyqtSignal()

    def __init__(self):
        super(InitialWidgetController, self).__init__()
        self.view = InitialWidgetView(self)

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def startButtonClicked(self):
        self.signalStartButtonClicked.emit()
