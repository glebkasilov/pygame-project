import pygame
import random

from scripts.utils import load_image
from scripts.objects.player import Player
from scripts.utils import all_sprites, tiles_group, grount_group, water_group, resource_group

tile_width = tile_height = 75

mass_resources = {
    'gold': [],
    'stone': [],
    'iron': [],
    'tree': [],
    'strawberry': []
}

tile_images = {
    'water': load_image('water.png'),
    'empty': load_image('grass.png')
}


class HeathBar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, max_health):
        super().__init__(resource_group, all_sprites)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_health = max_health
        self.health = max_health

        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        radio = self.health / self.max_health


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, group_name):
        super().__init__(tiles_group, all_sprites)

        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x,
            tile_height * pos_y
        )

        if group_name == "grount_group":
            grount_group.add(self)
        elif group_name == "water_group":
            water_group.add(self)

        self.x = self.rect.x
        self.y = self.rect.y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.x = self.rect.x
        self.y = self.rect.y

    def point_in_tile(self, x, y):
        return self.rect.collidepoint(x, y)


class Recourse(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type_resource):
        super().__init__(resource_group, all_sprites)
        self.image = load_image(
            f'block_{type_resource}.png', type_data="block", color_key=-1, scale=(64, 64) if type_resource != "strawberry" else (46, 40)
        )
        self.rect = self.image.get_rect().move(
            tile_width * pos_x,
            tile_height * pos_y
        )

        self.x = self.rect.x
        self.y = self.rect.y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.x = self.rect.x
        self.y = self.rect.y

    def point_in_tile(self, x, y):
        return self.rect.collidepoint(x, y)


class Tree(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'tree')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + self.image.get_width() // 2,
            tile_height * pos_y + self.image.get_height() // 2
        )

        self.x = self.rect.x
        self.y = self.rect.y

        self.health = 4

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health == 0:
            Player.inventory['wood'] += random.randint(1, 3)
            self.kill()

        return self.health


class Strawberry(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'strawberry')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + self.image.get_width() // 2,
            tile_height * pos_y + self.image.get_height() // 2
        )

        self.x = self.rect.x
        self.y = self.rect.y

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            Player.inventory['strawberry'] += random.randint(1, 3)
            self.kill()

        return self.health


class Gold(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'gold')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + self.image.get_width() // 2,
            tile_height * pos_y + self.image.get_height() // 2
        )

        self.x = self.rect.x
        self.y = self.rect.y

        self.health = 6

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            Player.inventory['gold'] += random.randint(1, 3)
            self.kill()

        return self.health


class Iron(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'iron')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + self.image.get_width() // 2,
            tile_height * pos_y + self.image.get_height() // 2
        )

        self.x = self.rect.x
        self.y = self.rect.y

        self.health = 5

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            Player.inventory['iron'] += random.randint(1, 3)
            self.kill()

        return self.health


class Stone(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'stone')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + self.image.get_width() // 2,
            tile_height * pos_y + self.image.get_height() // 2
        )

        self.x = self.rect.x
        self.y = self.rect.y

        self.health = 4

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            Player.inventory['stone'] += random.randint(1, 3)
            self.kill()

        return self.health


def generate_Resource():
    with open('levels/main_level.txt', 'r') as f:
        mapa = f.readlines()

    item = ['gold', 'stone', 'iron', 'tree',
            'strawberry'][random.randint(0, 4)]

    mass_values = list()
    for i in mass_resources.values():
        mass_values += i

    while True:
        x = random.randint(0, len(mapa[0]) - 1)
        y = random.randint(0, len(mapa) - 1)

        if (x, y) in mass_values or mapa[y][x] == '#' or mapa[y][x] == '@':
            continue
        break

    mass_resources[item].append((x, y))

    if item == 'gold':
        Gold(x, y)
    elif item == 'stone':
        Stone(x, y)
    elif item == 'iron':
        Iron(x, y)
    elif item == 'tree':
        Tree(x, y)
    elif item == 'strawberry':
        Strawberry(x, y)
