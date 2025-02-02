import pygame
import random

from scripts.utils import load_image
from scripts.objects.player import Player
from scripts.utils import all_sprites, tiles_group, grount_group, water_group, resource_group

tile_width = tile_height = 75

tile_images = {
    'water': load_image('water.png'),
    'empty': load_image('grass.png')
}

resource_images = {
    'gold': load_image('gold.png'),
    'stone': load_image('stone.png'),
    'iron': load_image('iron.png'),
    'tree': load_image('tree.png'),
    'strawberry': load_image('strawberry.png')
}


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
        # print(dx, dy)
        self.rect.x += dx
        self.rect.y += dy

        self.x = self.rect.x
        self.y = self.rect.y

    def point_in_tile(self, x, y):
        return self.rect.collidepoint(x, y)


class Recourse(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type_resource):
        super().__init__(resource_group, all_sprites)
        self.image = load_image(f'{type_resource}.png')
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


class Tree(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'tree')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25,
            tile_height * pos_y + 25
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
            tile_width * pos_x + 25,
            tile_height * pos_y + 25
        )

        self.x = self.rect.x
        self.y = self.rect.y

        resource_group.add(self)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            Player.inventory['gold'] += random.randint(1, 3)
            self.kill()

        return self.health


class Gold(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'gold')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25,
            tile_height * pos_y + 25
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
            tile_width * pos_x + 25,
            tile_height * pos_y + 25
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
            tile_width * pos_x + 25,
            tile_height * pos_y + 25
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

    x, y = random.randint(
        0, len(mapa[0]) - 1), random.randint(0, len(mapa) - 1)

    while mapa[y][x] == '#':
        x, y = random.randint(
            0, len(mapa[0]) - 1), random.randint(0, len(mapa) - 1)

    item = ['gold', 'stone', 'iron', 'tree',
            'strawberry'][random.randint(0, 4)]

    # print(x, y)
    return Recourse(x * tile_width, y * tile_height, item)
