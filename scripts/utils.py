import os

import pygame

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

water_group = pygame.sprite.Group()
grount_group = pygame.sprite.Group()

resource_group = pygame.sprite.Group()


def load_image(name, type_data="", color_key=None, scale=None):
    fullname = os.path.join('data', type_data, name)

    try:
        image = pygame.image.load(fullname).convert()

    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    if scale is not None:
        image = pygame.transform.scale(image, scale)

    else:
        image = image.convert_alpha()

    return image
