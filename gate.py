class Gate:
    def __init__(self):
        self.y = 0
        self.x = 640
        self.open = False

    def update(self, speed):
        self.x -= speed
        if self.x < 0:
            del self
