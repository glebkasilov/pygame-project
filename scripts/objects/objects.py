import pygame
import random

from scripts.utils import load_image
from scripts.objects.player import Player
from scripts.utils import (
    all_sprites,
    tiles_group,
    grount_group,
    water_group,
    resource_group,
    resource_bars_group
)

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

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health, width, height, offset):
        super().__init__(resource_bars_group, all_sprites)
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.offset = offset
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def update(self, parent_sprite):
        if self.current_health != self.max_health:
            self.rect.midtop = (
                parent_sprite.rect.centerx,
                parent_sprite.rect.top - self.offset[1]
            )

            health_ratio = self.current_health / self.max_health

            new_width = int(self.width * health_ratio)

            self.image = pygame.Surface([new_width, self.height])
            self.image.fill(GREEN)

            pygame.draw.rect(self.image, BLACK,
                             (0, 0, self.width, self.height), 1)

            if self.current_health <= 0:
                parent_sprite.kill()
        else:
            self.image.set_alpha(0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def decrease_health(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def point_in_tile(self, x, y):
        return False


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

    def kill(self):
        super().kill()
        if self in grount_group:
            grount_group.remove(self)
        elif self in water_group:
            water_group.remove(self)
        all_sprites.remove(self)


class Recourse(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type_resource):
        super().__init__(resource_group, all_sprites)
        self.image = load_image(
            f'block_{type_resource}.png', type_data="block", color_key=-1, scale=(64, 64) if type_resource != "strawberry" else (46, 40)
        )

        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y

        self.x = self.rect.x
        self.y = self.rect.y

    def point_in_tile(self, x, y):
        return self.rect.collidepoint(x, y)

    def kill(self):
        super().kill()
        all_sprites.remove(self)
        resource_group.remove(self)
        # mass_resources[self.type_resource].remove((self.x, self.y))

    def create_health_bar(self, health=1):
        health_bar = HealthBar(
            health,
            self.image.get_width() - 30,
            10,
            (0, -self.image.get_height() // 2 - 35)
        )
        health_bar.update(self)
        return health_bar


class Tree(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'tree')
        self.max_health = 4

        self.health = 4

        resource_group.add(self)
        self.health_bar = self.create_health_bar(self.health)

    def update(self):
        self.health_bar.update(self)

    def damage(self, damage=1) -> tuple[str | None, int | None]:
        self.health -= damage

        self.health_bar.current_health -= 1
        self.health_bar.update(self)

        if self.health <= 0:
            self.kill()
            return "wood", random.randint(1, 3)

        return None, None 


class Strawberry(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'strawberry')
        self.health = 1

        resource_group.add(self)

    def damage(self, damage=1) -> tuple[str | None, int | None]:
        self.health -= damage

        if self.health <= 0:
            self.kill()
            return "strawberry", random.randint(1, 3)

        return None, None


class Gold(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'gold')

        self.health = 6

        resource_group.add(self)

        self.health_bar = self.create_health_bar(self.health)

    def update(self):
        self.health_bar.update(self)

    def damage(self, damage=1) -> tuple[str | None, int | None]:
        self.health -= damage

        self.health_bar.current_health -= 1
        self.health_bar.update(self)

        if self.health <= 0:
            self.kill()
            return "gold", random.randint(1, 3)

        return None, None 


class Iron(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'iron')

        self.health = 5

        resource_group.add(self)

        self.health_bar = self.create_health_bar(self.health)

    def update(self):
        self.health_bar.update(self)

    def damage(self, damage=1) -> tuple[str | None, int | None]:
        self.health -= damage

        self.health_bar.current_health -= 1
        self.health_bar.update(self)

        if self.health <= 0:
            self.kill()
            return "iron", random.randint(1, 3)

        return None, None 


class Stone(Recourse):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 'stone')

        self.health = 4

        resource_group.add(self)

        self.health_bar = self.create_health_bar(self.health)
    
    def update(self):
        self.health_bar.update(self)

    def damage(self, damage=1) -> tuple[str | None, int | None]:
        self.health -= damage

        self.health_bar.current_health -= 1
        self.health_bar.update(self)

        if self.health <= 0:
            self.kill()
            return "stone", random.randint(1, 3)

        return None, None 


def generate_resource():
    with open('levels/main_level.txt', 'r') as f:
        mapa = [el.rstrip("\n") for el in f.readlines()]

    item = ['gold', 'stone', 'iron', 'tree',
            'strawberry'][random.randint(0, 4)]

    mass_values = list()
    for i in mass_resources.values():
        mass_values += i

    x = random.randint(0, len(mapa[0]) - 1)
    y = random.randint(0, len(mapa) - 1)

    while any((((x, y) in mass_values), (mapa[y][x] == '#'), (mapa[y][x] == '@'))):
        x = random.randint(0, len(mapa[0]) - 1)
        y = random.randint(0, len(mapa) - 1)

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
