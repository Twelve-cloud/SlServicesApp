class State:
    def __init__(self, active = False):
        self.active = active;

    def is_active(self):
        return self.active == True