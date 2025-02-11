import json
import pygame

from scripts.objects.objects import create_particles
from scripts.utils import (
    all_sprites,
    water_group,
    resource_group,
    exp_bar_group,
    inventory_group
)
from scripts.utils import load_image

PLAYER_MAX_SPEED = 4.5
FRICTION = 0.85
ACCELERATION = 0.5

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BG_COLOR = (50, 50, 50)
BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)


INVENTORY_WIDTH = 4
INVENTORY_HEIGHT = 3
CELL_SIZE = 40
PADDING = 5
ICON_SIZE = 32

tile_width = tile_height = 50

player_image = load_image('player.png')
player_heart_full = load_image('heart_full.png', color_key=-1)
player_heart_empty = load_image('heart_empty.png', color_key=-1)

player_group = pygame.sprite.Group()


class Inventory(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__(inventory_group)
        self.inventory_dict = self.load_inventory()
        self.is_visible = False
        self.items_positions = {
            "wood": (0, 0),
            "strawberry": (1, 0),
            "ore_iron": (2, 0),
            "ore_gold": (3, 0),
            "ore_stone": (0, 1),
            "ingot_iron": (1, 1),
            "ingot_gold": (2, 1)
        }

        self.width = CELL_SIZE * INVENTORY_WIDTH + \
            PADDING * (INVENTORY_WIDTH + 1)
        self.height = CELL_SIZE * INVENTORY_HEIGHT + \
            PADDING * (INVENTORY_HEIGHT + 1)

        self.image = pygame.Surface(
            (self.width, self.height))
        self.rect = self.image.get_rect(
            center=(screen_width // 2, screen_height // 2))

        self.icons = {}

        for name in self.items_positions.keys():
            if name.startswith("ore"):
                self.icons[name] = load_image(f"ore/{name}.png")
            elif name.startswith("ingot"):
                self.icons[name] = load_image(f"ingot/{name}.png")
            else:
                self.icons[name] = load_image(f"{name}.png")

        self.font = pygame.font.Font(None, 20)

    def update(self):
        if self.is_visible:
            self.image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)

            self.image.fill((0, 0, 0))

            pygame.draw.rect(self.image, BG_COLOR,
                             (0, 0, self.width, self.height))
            pygame.draw.rect(self.image, BORDER_COLOR,
                             (0, 0, self.width, self.height), 2)

            for name, (x, y) in self.items_positions.items():
                count = self.inventory_dict.get(name, 0)
                if count > 0:
                    pos_x = PADDING + x * (CELL_SIZE + PADDING)
                    pos_y = PADDING + y * (CELL_SIZE + PADDING)

                    self.image.blit(self.icons[name], (pos_x + 4, pos_y + 4))

                    text = self.font.render(str(count), True, TEXT_COLOR)
                    self.image.blit(
                        text, (pos_x + CELL_SIZE - 15, pos_y + CELL_SIZE - 15))

        else:
            self.image.set_alpha(0)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def add_item(self, item_type, amount=1):
        if item_type in self.inventory_dict:
            self.inventory_dict[item_type] += amount
        else:
            self.inventory_dict[item_type] = amount

        with open("data/player/inventory.json", "w") as f:
            json.dump(self.inventory_dict, f, ensure_ascii=False, indent=4)

    def load_inventory(self) -> dict:
        with open("data/player/inventory.json", "r") as f:
            data = json.load(f)

        return data


class ExpBar(pygame.sprite.Sprite):
    def __init__(self, max_exp, width, height, offset):
        super().__init__(exp_bar_group)
        self.max_exp = max_exp
        self.current_exp = 0
        self.width = width
        self.height = height
        self.offset = offset
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

    def update(self, parent_sprite):
        self.rect.midtop = self.offset

        exp_ratio = self.current_exp / self.max_exp

        new_width = int(self.width * exp_ratio)

        self.image = pygame.Surface([self.width, self.height])
        self.image_bar = pygame.Surface([new_width, self.height])
        self.image_bar.fill(BLUE)

        pygame.draw.rect(self.image, BLACK,
                         (0, 0, self.width, self.height), 1)

        self.image.blit(self.image_bar, (0, 0))

    def add_exp(self, amount) -> 0 | 1:
        self.current_exp += amount
        if self.current_exp >= self.max_exp:
            self.current_exp = 0

            self.max_exp *= 1.5

            return 1

        return 0


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

        self.exp_bar = ExpBar(10, 400, 20, (400, 20))
        self.load_stats()

        self.inventory = Inventory(800, 600)

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
        for sprite in resource_group:
            if pygame.sprite.collide_rect(self, sprite):
                obj, count = sprite.damage()
                if obj is not None:
                    self.add_item(obj, count)
                    self.experience += count
                    new_level = self.exp_bar.add_exp(count)

                    self.save_stats()

                    if new_level != 0:
                        self.level += new_level
                        self.save_stats()
                        self.level_up()

    def damaged(self):
        self.health -= 1
        self.hearts[self.health].damage()

        if self.health == 0:
            self.is_alive = False

        if self.health >= 0:
            self.health += 1

        self.save_stats()

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
        self.inventory.add_item(item, count)

    def load_stats(self):
        with open('data/player/stats.json', 'r') as f:
            stats = json.load(f)
        try:
            self.health = stats['health']
            self.max_health = stats['health_max']
            self.hearts = [Heart(i, 0) for i in range(self.health)]

            self.exp_bar.current_exp = stats['experience']
            self.exp_bar.max_exp = stats['experience_max']

            self.level = stats['level']
            self.experience = stats['experience']
        except:
            self.health = 3
            self.max_health = 3
            self.hearts = [Heart(i, 0) for i in range(self.health)]

            self.level = 1
            self.experience = 0

    def save_stats(self):
        with open('data/player/stats.json', 'w') as f:
            json.dump(
                {
                    'health': self.health,
                    'health_max': self.max_health,
                    'experience': self.exp_bar.current_exp,
                    'experience_max': self.exp_bar.max_exp,
                    'level': self.level
                },

                f, ensure_ascii=False,
                indent=4
            )

    def level_up(self):
        create_particles((self.rect.centerx, self.rect.centery - 200))


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
