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
# player = None


def terminate():
    pygame.quit()
    sys.exit()


class Scene:
    def __init__(self, manager):
        self.manager = manager  # Менеджер сцен
        self.screen = manager.screen  # Экран для отрисовки

    # def handle_events(self, events):
    #     """Обработка событий"""
    #     raise NotImplementedError

    def update(self, screen):
        """Обновление логики"""
        raise NotImplementedError

    def draw(self):
        """Отрисовка содержимого"""
        raise NotImplementedError

    def on_activate(self):
        """Вызывается при активации сцены"""
        pass

    def on_deactivate(self):
        """Вызывается при деактивации сцены"""
        pass


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.current_scene = None
        self.shared_data = {}

    def switch_to(self, new_scene):
        """Переключение на новую сцену"""
        if self.current_scene:
            self.current_scene.on_deactivate()
        self.current_scene = new_scene
        self.current_scene.on_activate()

    def run(self):
        """Основной игровой цикл"""
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update(screen)
            # print(self.current_scene)
            # screen.fill(pygame.Color(56, 152, 255))  # Очистка экрана

            pygame.display.flip()
            clock.tick(FPS)


# Windows


class MainMenu(Scene):
    def __init__(self, manager):
        from scripts.objects.screens import start_screen, end_screen
        super().__init__(manager)
        start_screen()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                manager.running = False

    def update(self, screen):
        manager.switch_to(GameScene(manager))
        return "end"


class ReloadWindow(Scene):
    def __init__(self, manager, scnene_name):
        from scripts.objects.screens import reload_screen
        super().__init__(manager)
        self.scnene_name = scnene_name

        if self.scnene_name == "":
            raise "Scnene_name is empty"

        reload_screen()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                manager.running = False

    def update(self, screen):
        if self.scnene_name == "GameSceneV2":
            manager.switch_to(GameSceneV2(manager))
        print(self.scnene_name)
        return "end"


class EndWindow(Scene):
    def __init__(self, manager):
        from scripts.objects.screens import end_screen
        super().__init__(manager)
        end_screen()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                manager.running = False

    def update(self, screen):
        manager.running = False
        return "end"


# Scenes


class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

    def on_activate(self):
        super().on_activate()
        from scripts.objects.map import generate_level, update_level
        from scripts.objects.map import load_level
        from scripts.objects.camera import Camera
        self.player, x, y = generate_level(load_level('main_level.txt'))

        self.camera = Camera()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                manager.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.player.hit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.player.inventory.toggle_visibility()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                clear_screen()
                manager.switch_to(EndWindow(manager))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and self.player.level >= 5:
                clear_screen()
                manager.switch_to(ReloadWindow(manager, "GameSceneV2"))

        keys = pygame.key.get_pressed()

        if not self.player.inventory.is_visible:
            direction = {
                'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
                'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
                'up': keys[pygame.K_UP] or keys[pygame.K_w],
                'down': keys[pygame.K_DOWN] or keys[pygame.K_s]
            }

            self.player.move_self(direction)
        else:
            self.player.stop_moving()

    def update(self, screen):
        from scripts.utils import (
            tiles_group,
            all_sprites,
            grount_group,
            water_group,
            resource_group,
            resource_bars_group,
            exp_bar_group,
            inventory_group,
            stars_group
        )
        from scripts.objects.objects import generate_resource
        from scripts.objects.player import player_group

        screen.fill(pygame.Color(56, 152, 255))
        tiles_group.draw(screen)

        while len(resource_group) < 10:
            generate_resource()

        water_group.draw(screen)
        grount_group.draw(screen)

        resource_group.draw(screen)
        resource_group.update()

        resource_bars_group.draw(screen)

        player_group.draw(screen)
        player_group.update()

        exp_bar_group.draw(screen)
        exp_bar_group.update(self.player.experience)

        inventory_group.draw(screen)
        inventory_group.update()

        stars_group.draw(screen)
        stars_group.update()

        self.camera.update(self.player)

        for sprite in all_sprites:
            self.camera.apply(sprite)

        if self.player.health == 0:
            manager.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.entities.draw(self.screen)
        self.player.draw(self.screen)


class GameSceneV2(Scene):
    def __init__(self, manager):
        super().__init__(manager)

    def on_activate(self):
        super().on_activate()
        from scripts.objects.map import generate_level
        from scripts.objects.map import load_level
        from scripts.objects.camera import Camera
        self.player, x, y = generate_level(load_level('map_with_furnace.txt'))

        self.camera = Camera()

    def handle_events(self, events):
        from scripts.utils import forge_group

        for event in events:
            if event.type == pygame.QUIT:
                manager.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.player.hit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.player.inventory.toggle_visibility()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.player.active()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                clear_screen()
                manager.switch_to(EndWindow(manager))

        keys = pygame.key.get_pressed()

        if (not self.player.inventory.is_visible) and (not any([sprite.furnace_interface.is_visible for sprite in forge_group])):
            direction = {
                'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
                'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
                'up': keys[pygame.K_UP] or keys[pygame.K_w],
                'down': keys[pygame.K_DOWN] or keys[pygame.K_s]
            }

            self.player.move_self(direction)
        else:
            self.player.stop_moving()

    def update(self, screen):
        from scripts.utils import (
            tiles_group,
            all_sprites,
            grount_group,
            water_group,
            resource_group,
            resource_bars_group,
            exp_bar_group,
            inventory_group,
            stars_group,
            forge_group,
            furnace_interface_group
        )
        from scripts.objects.objects import generate_resource
        from scripts.objects.player import player_group

        screen.fill(pygame.Color(56, 152, 255))
        tiles_group.draw(screen)

        while len(resource_group) < 10:
            generate_resource()

        water_group.draw(screen)
        grount_group.draw(screen)

        resource_group.draw(screen)
        resource_group.update()

        resource_bars_group.draw(screen)

        player_group.draw(screen)
        player_group.update()

        exp_bar_group.draw(screen)
        exp_bar_group.update(self.player.experience)

        stars_group.draw(screen)
        stars_group.update()

        forge_group.draw(screen)
        forge_group.update()

        inventory_group.draw(screen)
        inventory_group.update()

        furnace_interface_group.draw(screen)
        furnace_interface_group.update()

        self.camera.update(self.player)

        for sprite in all_sprites:
            self.camera.apply(sprite)

        if self.player.health == 0:
            manager.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.entities.draw(self.screen)
        self.player.draw(self.screen)


def clear_screen():
    from scripts.utils import all_sprites

    for sprite in all_sprites:
        sprite.kill()

    screen.fill(pygame.Color(56, 152, 255))
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    manager = SceneManager(screen)
    manager.switch_to(MainMenu(manager))
    manager.run()
    pygame.quit()
