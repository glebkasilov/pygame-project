import pygame
import time

from scripts.utils import all_sprites, water_group, resource_group
from scripts.utils import load_image

PLAYER_MAX_SPEED = 4.5
FRICTION = 0.85
ACCELERATION = 0.5

tile_width = tile_height = 50

player_image = load_image('player.png')
player_heart_full = load_image('heart_full.png', color_key=-1)
player_heart_empty = load_image('heart_empty.png', color_key=-1)

player_group = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.tick = 0
        self.update_tick = 8

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animation_move_forward(self):
        if self.tick % self.update_tick == 0:
            self.cur_frame = ((self.cur_frame + 1) % 4) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.tick += 1

    def animation_move_right(self):
        if self.tick % self.update_tick == 0:
            self.cur_frame = ((self.cur_frame + 1) % 4 + 4) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.tick += 1

    def animation_move_backward(self):
        if self.tick % self.update_tick == 0:
            self.cur_frame = ((self.cur_frame + 1) % 4 + 8) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.tick += 1

    def animation_move_left(self):
        if self.tick % self.update_tick == 0:
            self.cur_frame = ((self.cur_frame + 1) % 4 + 12) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.tick += 1

    def animation_default(self):
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


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


class Player(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        player_image = load_image('player.png', color_key=-1, scale=(150, 150))

        super().__init__(player_image, 4, 4, tile_width *
                         pos_x + 25, tile_width * pos_y + 25)

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
            "iron": 0,
            "strawberry": 0
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

        if direction['left'] and (not can_move_point(self.x, self.y + self.rect.height // 2, 'left')):
            self.pos_x = 0.0

        if direction['right'] and (not can_move_point(self.x + self.rect.width // 2, self.y + self.rect.height // 2, 'right')):
            self.pos_x = 0.0

        if direction['up'] and (not can_move_point(self.x + self.rect.width // 2, self.y, 'up')):
            self.pos_y = 0.0

        if direction['down'] and (not can_move_point(self.x + self.rect.width // 2, self.y + self.rect.height // 2, 'down')):
            self.pos_y = 0.0

        self.pos_x = max(-PLAYER_MAX_SPEED,
                         min(self.pos_x, PLAYER_MAX_SPEED))
        self.pos_y = max(-PLAYER_MAX_SPEED,
                         min(self.pos_y, PLAYER_MAX_SPEED))

        if self.pos_y > 0.5:
            self.animation_move_forward()
        elif self.pos_y < -0.5:
            self.animation_move_backward()
        elif self.pos_x > 0.5:
            self.animation_move_right()
        elif self.pos_x < -0.5:
            self.animation_move_left()

        if self.pos_x == 0 and self.pos_y == 0:
            self.animation_default()

        self.x += self.pos_x
        self.y += self.pos_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if abs(self.pos_x) < 0.1:
            self.pos_x = 0.0
        if abs(self.pos_y) < 0.1:
            self.pos_y = 0.0

    def hit(self):
        print("hit")

        for sprite in resource_group:
            if pygame.sprite.collide_rect(self, sprite):
                obj, count = sprite.damage()
                if obj is not None:
                    self.add_item(obj, count)

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

    def add_item(self, item, count):
        self.inventory[item] += count
        print(self.inventory)


def can_move_point(x_now, y_now, direction) -> bool:
    if direction == 'left':
        for tile in water_group:
            # or tile.point_in_tile(x_now - 4, y_now - 5) or tile.point_in_tile(x_now - 4, y_now + 5):
            if tile.point_in_tile(x_now, y_now):
                return False
        for tile in resource_group:
            # or tile.point_in_tile(x_now - 4, y_now - 5) or tile.point_in_tile(x_now - 4, y_now + 5):
            if tile.point_in_tile(x_now, y_now):
                return False

    if direction == 'right':
        for tile in water_group:
            # or tile.point_in_tile(x_now + 4, y_now - 5) or tile.point_in_tile(x_now + 4, y_now + 5):
            if tile.point_in_tile(x_now + 4, y_now):
                return False

        for tile in resource_group:
            # or tile.point_in_tile(x_now + 4, y_now - 5) or tile.point_in_tile(x_now + 4, y_now + 5):
            if tile.point_in_tile(x_now + 4, y_now):
                return False

    if direction == 'up':
        for tile in water_group:
            # or tile.point_in_tile(x_now - 5, y_now - 4) or tile.point_in_tile(x_now + 5, y_now - 4):
            if tile.point_in_tile(x_now, y_now - 2):
                return False
        for tile in resource_group:
            # or tile.point_in_tile(x_now - 5, y_now - 4) or tile.point_in_tile(x_now + 5, y_now - 4):
            if tile.point_in_tile(x_now, y_now - 2):
                return False

    if direction == 'down':
        for tile in water_group:
            # or tile.point_in_tile(x_now - 5, y_now + 4) or tile.point_in_tile(x_now + 5, y_now + 4):
            if tile.point_in_tile(x_now, y_now + 4):
                return False
        for tile in resource_group:
            # or tile.point_in_tile(x_now - 5, y_now + 4) or tile.point_in_tile(x_now + 5, y_now + 4):
            if tile.point_in_tile(x_now, y_now + 4):
                return False

    return True
