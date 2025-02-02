import pygame

from scripts.utils import all_sprites, water_group
from scripts.utils import load_image

PLAYER_MAX_SPEED = 4.5
FRICTION = 0.85
ACCELERATION = 0.5

tile_width = tile_height = 50

player_image = load_image('player.png')
player_heart_full = load_image('heart_full.png', -1)
player_heart_empty = load_image('heart_empty.png', -1)

player_group = pygame.sprite.Group()


class Heart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, is_active=True):
        super().__init__(player_group, all_sprites)
        if not is_active:
            self.image = player_heart_empty

        else:
            self.image = player_heart_full

        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25, tile_height * pos_y + 15)

        self.x = self.rect.x
        self.y = self.rect.y

        self.pos_x = 0.0
        self.pos_y = 0.0

    def damage(self):
        self.image = player_heart_empty

    def heal(self):
        self.image = player_heart_full


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

        self.is_alive = True
        self.health = 3
        self.max_health = 3
        self.hearts = [Heart(i, 0) for i in range(self.health)]

        self.inventory = {
            "gold": 0,
            "wood": 0,
            "stone": 0,
            "iron": 0
        }

    def update(self):
        super().update()

        if not self.is_alive:
            self.kill()

    def move_self(self, direction):
        if direction['left'] and direction['right']:
            self.pos_x *= FRICTION
        else:
            if direction['left']:
                if not point_in_water_tile(self.rect.x - 1, self.rect.y):
                    self.pos_x -= ACCELERATION
            if direction['right']:
                self.pos_x += ACCELERATION

        if point_in_water_tile(self.rect.x - 1, self.rect.y) and direction['left'] \
                or point_in_water_tile(self.rect.x + self.rect.w - 1, self.rect.y) and direction['right']:
            self.pos_x = 0

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

        if point_in_water_tile(self.rect.x, self.rect.y - 1) and direction['up'] \
                or point_in_water_tile(self.rect.x, self.rect.y + self.rect.h - 1) and direction['down']:
            self.pos_y = 0

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

    def damaged(self):
        self.health -= 1
        self.hearts[self.health].damage()

        if self.health == 0:
            self.is_alive = False

    def healed(self):
        if self.health <= self.max_health:
            self.health += 1
            self.hearts[self.health - 1].heal()

    def move(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy

    def move_center(self):
        self.x = 800 / 2
        self.y = 600 / 2


def point_in_water_tile(x, y):
    for tile in water_group:
        if tile.point_in_tile(x, y):
            return True
    return False
