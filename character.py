import pygame
import os

_sound_library = {}


def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    pygame.mixer.init()
    sound.play()


def get_running_image(image_library, step):
    path = 'res/Char/run/{}.png'.format(step)
    image = image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        image_library[path] = image
    return image


def get_image(path, image_library):
    image = image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        image_library[path] = image
    return image


class Player:
    def is_collided_with(self, sprite):
        if self.rect.colliderect(sprite):
            self.buffer -= 1
            if self.buffer == 0:
                self.state = "dead"
                play_sound('res/sound/dead.wav')

    def coin_collide(self, sprite):
        if self.rect.colliderect(sprite):
            self.money += 1
            play_sound('res/sound/coin.wav')
            return True
        return False

    def gate_collide(self, sprite):
        if self.rect.colliderect(sprite):
            return True
        return False

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._image_library = {}
        self.state = "sleep"
        self.is_jumping = False
        self.y_relative_pos = 0
        self.velocity = 0
        self.jump_counter = 2
        self.run_frame = 1
        self.x = 100
        self.y = 180
        self.image = get_image('res/Char/sleep.png', self._image_library)
        self.rect = self.image.get_rect()
        self.run_counter = 0
        self.buffer = 3
        self.money = 0

    def jump(self):
        if self.state is not "dead":
            if self.jump_counter > 0:
                if self.is_jumping is False:
                    self.is_jumping = True
                    self.velocity = 40
                    self.state = "jump"
                else:
                    if self.velocity < 20:
                        self.velocity += 40
                        self.state = "jump"
                play_sound('res/sound/jump.wav')
            self.jump_counter -= 1

    def update_run(self):
        if self.state is not "dead":
            self.run_frame += 1
            if self.run_frame > 6:
                self.run_frame = 1
            return get_running_image(self._image_library, self.run_frame)
        return get_image('res/Char/dead.png', self._image_library)

    def update(self):
        F = 0
        if self.is_jumping:
            F = (1 * self.velocity) / 2
            self.velocity -= 4
        self.y_relative_pos += F
        if self.y_relative_pos <= 0:
            self.y_relative_pos = 0
            if self.state is not "dead":
                self.state = "running"
            self.is_jumping = False
            self.jump_counter = 2

    def get_down(self):
        if self.is_jumping:
            self.velocity -= 10

    def render(self, window):
        if self.state == "running":
            if self.run_counter > 2:
                self.image = self.update_run()
                self.run_counter = 0
            self.run_counter += 1
        elif self.state == "jump":
            self.image = get_image('res/Char/jump.png', self._image_library)
        elif self.state == "sleep":
            self.image = get_image('res/Char/sleep.png', self._image_library)
        elif self.state == "dead":
            self.image = get_image('res/Char/dead.png', self._image_library)
        # self.rect = self.image.get_rect()
        self.rect = window.blit(self.image,
                                (self.x, self.y - self.y_relative_pos))
