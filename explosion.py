import random
import pygame


class Explosion_fragment:
    def __init__(self):
        self.y_pos = 100 + random.randint(0, 80)
        self.x_pos = 0
        self.x_velocity = random.randint(15, 30)
        self.y_velocity = (random.randint(20, 55)) - 35
        self.size = random.randint(2, 10)

    def update(self):
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        if self.x_pos > 640:
            del self


def initiate_explode():
    explode_var = []
    for i in range(250):
        explode_var.append(Explosion_fragment())

    return explode_var


def draw_explosion(screen, explosions):
    for i, j in enumerate(explosions):
        x = explosions[i].x_pos
        y = explosions[i].y_pos
        size = explosions[i].size
        pygame.draw.rect(screen, (0, 0, 0),
                         [x, y, size, size], 0)
