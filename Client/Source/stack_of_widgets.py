# This Python file uses the following encoding: utf-8

class StackOfWidgets:
    def __init__(self):
        self.widgets = []

    def push(self, widget):
        self.widgets.append(widget)
        self.widgets[-1].show()

    def pop(self):
        self.widgets[-1].hide()
        self.widgets.pop()
