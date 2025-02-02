import pygame

from scripts.utils import load_image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

tile_width = tile_height = 75

tile_images = {
    'water': load_image('water.png'),
    'empty': load_image('grass.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)

        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x,
            tile_height * pos_y
        )
