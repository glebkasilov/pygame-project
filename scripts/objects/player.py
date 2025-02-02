import pygame

from scripts.objects.objects import all_sprites
from scripts.utils import load_image

PLAYER_MAX_SPEED = 8
FRICTION = 0.85
ACCELERATION = 0.5

tile_width = tile_height = 50

player_image = load_image('player.png')
player_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25, tile_height * pos_y + 15)

        self.x = self.rect.x
        self.y = self.rect.y

        self.pos_x = 0.0
        self.pos_y = 0.0

        self.player_speed = 0.0

    def move_self(self, direction):
        if direction['left'] and direction['right']:
            self.pos_x *= FRICTION
        else:
            if direction['left']:
                self.pos_x -= ACCELERATION
            if direction['right']:
                self.pos_x += ACCELERATION

        if not (direction['left'] or direction['right']):
            self.pos_x *= FRICTION

        if direction['up'] and direction['down']:
            self.pos_y *= FRICTION
        else:
            if direction['up']:
                self.pos_y -= ACCELERATION
            if direction['down']:
                self.pos_y += ACCELERATION

        if not (direction['up'] or direction['down']):
            self.pos_y *= FRICTION

        self.pos_x = max(-PLAYER_MAX_SPEED,
                         min(self.pos_x, PLAYER_MAX_SPEED))
        self.pos_y = max(-PLAYER_MAX_SPEED,
                         min(self.pos_y, PLAYER_MAX_SPEED))

        self.x += self.pos_x
        self.y += self.pos_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if abs(self.pos_x) < 0.1:
            self.pos_x = 0.0
        if abs(self.pos_y) < 0.1:
            self.pos_y = 0.0
