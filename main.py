import os
import sys
import pygame

from scripts.utils import load_image
from scripts.objects.player import Player


# Constants
FPS = 60
WIDTH = 800
HEIGHT = 640

# Init
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Global variables
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    terminate()
