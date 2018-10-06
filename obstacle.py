class Obstacle:
    def __init__(self, s, offset):
            self.type = s
            if self.type == 1:
                self.y = 280 - 85
                width = 80
            elif self.type == 2:
                self.y = 280 - 90
                width = 65
            elif self.type == 3:
                self.y = 280 - 100
                width = 45
            elif self.type == 4:
                self.y = 280 - 80
                width = 65
            elif self.type == 5:
                self.y = 280 - 130
                width = 125
            if self.type < 5:
                if offset == 0:
                    self.x = 640
                else:
                    self.x = 640 + (width * offset)
            else:
                self.x = 640

    def update(self, speed):
        self.x -= speed
        if self.x < 0:
            del self
