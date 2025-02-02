import os
import sys
import pygame


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


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    from scripts.objects.screens import start_screen
    from scripts.objects.map import generate_level
    from scripts.objects.map import load_level
    from scripts.objects.objects import tiles_group
    from scripts.objects.player import player_group

    start_screen()
    player, x, y = generate_level(load_level('main_level.txt'))

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        direction = {
            'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
            'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
            'up': keys[pygame.K_UP] or keys[pygame.K_w],
            'down': keys[pygame.K_DOWN] or keys[pygame.K_s]
        }

        player.move_self(direction)

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    terminate()
