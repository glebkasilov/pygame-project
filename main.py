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
    from scripts.utils import tiles_group, all_sprites, grount_group, water_group, resource_group
    from scripts.objects.objects import generate_Resource
    from scripts.objects.player import player_group
    from scripts.objects.camera import Camera

    start_screen()
    player, x, y = generate_level(load_level('main_level.txt'))

    running = True
    while running:
        while len(resource_group) < 10:
            # print(len(resource_group))
            generate_Resource()

        camera = Camera()

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

        # screen.fill(pygame.Color(56, 152, 255))
        tiles_group.draw(screen)

        water_group.draw(screen)
        grount_group.draw(screen)

        player_group.draw(screen)
        player_group.update()

        resource_group.draw(screen)

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        if player.health == 0:
            running = False

        pygame.display.flip()

        clock.tick(FPS)

    terminate()
