import os
import pygame
from explosion import *
from character import *
from obstacle import *
from coin import *
from gate import *


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 30)
_image_library = {}
_cached_font = {}
_cached_text = {}
_sound_library = {}
clock = pygame.time.Clock()
offset = 0
down_pressed = False
explosions = initiate_explode()
explode = False
character = Player()
gate_timer = 10
required_coins = 10


def get_font(size):
    global _cached_font
    key = str(size)
    font = _cached_font.get(key, None)
    if font is None:
        font = pygame.font.Font("res/segoe-print-bold.ttf", size)
        _cached_font[key] = font
    return font


def create_text(text, size, color):
    global _cached_text
    key = '|'.join(map(str, (size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    pygame.mixer.init()
    sound.play()


def main(screen):
    screen.on_execute()


class MainMenu:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = (640, 480)

    def on_init(self):
        global character
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Run UIB Run!")
        self._running = True
        self.clock = pygame.time.Clock()
        self.start_button = self.screen.blit(get_image('res/start_btn.png'),
                                             (350, 320))
        self.exit_button = self.screen.blit(get_image('res/exit_btn.png'),
                                            (350, 400))
        character.render(self.screen)

    def on_event(self, event):
        global explode
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_RETURN:
                explode = True
                self.ticks = pygame.time.get_ticks()
                play_sound('res/sound/expl3.wav')
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.start_button.collidepoint(pygame.mouse.get_pos()):
                explode = True
                self.ticks = pygame.time.get_ticks()
                play_sound('res/sound/expl3.wav')
            elif self.exit_button.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()

    def on_loop(self):
        global explode, explosions
        if explode is True:
            for i, j in enumerate(explosions):
                explosions[i].update()
            ticks_passed = (pygame.time.get_ticks() - self.ticks)
            if ticks_passed > 500:
                explode = False
                theApp = Play()
                main(theApp)
        self.clock.tick(30)

    def on_render(self):
        global character
        self.screen.blit(get_image('res/building.png'), (0, 0))
        self.start_button = self.screen.blit(get_image('res/start_btn.png'),
                                             (350, 320))
        self.exit_button = self.screen.blit(get_image('res/exit_btn.png'),
                                            (350, 400))
        character.render(self.screen)
        if explode is True:
            ticks_passed = (pygame.time.get_ticks() - self.ticks)
            alpha_value = 255 - (255.0 * (ticks_passed / 500.0))
            s = pygame.Surface((640, 480))
            s.set_alpha(int(alpha_value))
            s.fill((225, 221, 20))
            self.screen.blit(s, (0, 0))
            draw_explosion(self.screen, explosions)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class Play:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = (640, 480)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Run UIB Run!")
        self._running = True
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        self.speed = 8
        self.obj_speed = 10
        self.building = get_image('res/building.png')
        self.building_bg1 = self.screen.blit(self.building, (self.offset_x, 0))
        self.building_bg2 = self.screen.blit(self.building,
                                             (self.offset_x + 640, 0))
        self.obstacles = []
        self.coins = []
        self.gate = None
        self.passed_gate = False
        self.obstacles.append(Obstacle(1, 0))

    def on_event(self, event):
        global character, down_pressed, gate_timer
        global explosions, explode, required_coins
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                del character
                character = Player()
                explosions = initiate_explode()
                explode = False
                self.gate = None
                self.passed_gate = False
                theApp = MainMenu()
                gate_timer = 10
                required_coins = 10
                main(theApp)
            elif event.key == pygame.K_SPACE:
                character.jump()
            elif event.key == pygame.K_DOWN:
                down_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                down_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pass

    def on_loop(self):
        global character, down_pressed, gate_timer, required_coins
        character.update()
        if character.state is not "dead":
            self.offset_x -= self.speed
            if self.offset_x < -640:
                self.offset_x = 0
            for i, j in enumerate(explosions):
                explosions[i].update()
            if down_pressed:
                character.get_down()
            for i in self.obstacles:
                i.update(self.obj_speed)
            for i in self.coins:
                i.update(self.obj_speed)

            if self.gate is not None:
                self.gate.update(self.obj_speed)
                if character.money >= required_coins:
                    self.gate.open = True
                if self.gate.x < 0:
                    self.gate = None
                    self.passed_gate = False
                    gate_timer = 10

            chance = random.randint(0, 20)
            if chance == 0 and gate_timer > 0:
                if len(self.obstacles) > 0:
                    if self.obstacles[-1].x < 300 and self.gate is None:
                        s = random.randint(1, 5)
                        if random.randint(0, 8) == 0:
                            for i in range(random.randint(2, 3)):
                                gate_timer -= 1
                                if gate_timer == 0 and self.gate is None:
                                    self.gate = Gate()
                                else:
                                    self.obstacles.append(Obstacle(s, i))
                                    self.coins.append(Coin(i))
                        else:
                            gate_timer -= 1
                            if gate_timer == 0 and self.gate is None:
                                self.gate = Gate()
                                print "Created new Gate"
                            else:
                                self.obstacles.append(Obstacle(s, 0))
                                self.coins.append(Coin(0))
                        character.buffer = 3
                    elif self.obstacles[-1].x < 550:
                        if len(self.coins) > 0:
                            if self.coins[-1].x < 690:
                                self.coins.append(Coin(-1))

        character.render(self.screen)
        self.clock.tick(30)

    def on_render(self):
        global char_sprite, character, required_coins
        self.building_bg1 = self.screen.blit(self.building, (self.offset_x, 0))
        self.building_bg2 = self.screen.blit(self.building,
                                             (self.offset_x + 640, 0))
        for i in self.obstacles:
            obs = self.screen.blit(get_image('res/obs' + str(i.type) + '.png'),
                                   (i.x, i.y))
            character.is_collided_with(obs)

        for key, v in enumerate(self.coins):
            coin = self.screen.blit(get_image('res/coin.png'), (v.x, v.y))
            if (character.coin_collide(coin)):
                self.coins.pop(key)

        character.render(self.screen)
        draw_explosion(self.screen, explosions)

        text = create_text(str(character.money) + "/" + str(required_coins) + "  COINS",
                           25, (255, 250, 20))
        self.screen.blit(text, (20, 300))

        if self.gate is not None:
            if self.gate.open:
                gate = self.screen.blit(get_image('res/gate_opened.png'),
                                        (self.gate.x, self.gate.y))
            else:
                gate = self.screen.blit(get_image('res/gate_closed.png'),
                                        (self.gate.x, self.gate.y))
            if (character.gate_collide(gate)):
                if self.gate.open:
                    if self.passed_gate is False:
                        character.money = character.money - required_coins
                        required_coins += 1
                        self.speed += 2
                        self.obj_speed += 1
                        self.passed_gate = True
                else:
                    character.state = "dead"
                    play_sound('res/sound/dead.wav')

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = MainMenu()
    main(theApp)
