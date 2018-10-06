class Coin:
    def __init__(self, offset):
        if offset < 0:
            self.y = 280 - 50
            self.x = 640
        else:
            self.y = 280 - 200
            self.x = 640 + (50 * offset)

    def update(self, speed):
        self.x -= speed
        if self.x < 0:
            del self
