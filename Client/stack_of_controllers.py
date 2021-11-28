# This Python file uses the following encoding: utf-8

class StackOfControllers:
    def __init__(self):
        self.controllers = []

    def push(self, controller):
        self.controllers.append(controller)
        self.controllers[-1].show()

    def pop(self):
        self.controllers[-1].close()
        self.controllers.pop()
