import pygame
import random

from scripts.utils import load_image
from main import screen
from scripts.utils import (
    all_sprites,
    tiles_group,
    grount_group,
    water_group,
    resource_group,
    resource_bars_group,
    stars_group,
    forge_group,
    furnace_interface_group
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
BG_COLOR = (50, 50, 50)
BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)


class FurnaceInterface(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__(furnace_interface_group)
        self.inventory = {}
        self.is_visible = False
        self.smelting_recipes = {
            "ore_iron": ("ingot_iron", 1),
            "ore_gold": ("ingot_gold", 1)
        }

        self.tick = 0

        # Настройка размеров
        self.width = 300
        self.height = 200
        self.button_width = 100
        self.button_height = 40
        self.padding = 20

        # Создание поверхности
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(
            center=(screen_width // 2, screen_height // 2))

        # Загрузка текстур
        self.icons = {
            "ore_iron": load_image("ore/ore_iron.png"),
            "ore_gold": load_image("ore/ore_gold.png"),
            "ingot_iron": load_image("ingot/ingot_iron.png"),
            "ingot_gold": load_image("ingot/ingot_gold.png")
        }

        # Шрифты
        self.font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 22)

        # Кнопки
        self.buttons = []

    def update(self):
        self.buttons = []
        if self.is_visible:
            self.image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)

            self.image.fill((0, 0, 0,))

            # Рисуем фон
            pygame.draw.rect(self.image, BG_COLOR,
                             (0, 0, self.width, self.height))
            pygame.draw.rect(self.image, BORDER_COLOR,
                             (0, 0, self.width, self.height), 2)

            # Отрисовка рецептов и кнопок
            y = self.padding
            for i, (ore, (ingot, count)) in enumerate(self.smelting_recipes.items()):
                self._draw_recipe(y, ore, ingot)
                y += 60
        else:
            self.image.set_alpha(0)

    def _draw_recipe(self, y_pos, ore, ingot):
        # Иконки ресурсов
        self.image.blit(self.icons[ore], (self.padding, y_pos))
        self.image.blit(self.icons[ingot],
                        (self.width - self.padding - 32, y_pos))

        # Текст рецепта
        text = self.font.render(f"3 {ore} -> 1 {ingot}", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(self.width//2, y_pos + 16))
        self.image.blit(text, text_rect)

        # Кнопка крафта
        button_rect = pygame.Rect(
            self.width//2 - self.button_width//2,
            y_pos + 30,
            self.button_width,
            self.button_height
        )

        # Проверка доступности
        can_craft = self.inventory.get(ore, 0) >= 3
        button_color = (50, 150, 50) if can_craft else (100, 100, 100)

        # Отрисовка кнопки
        pygame.draw.rect(self.image, button_color,
                         button_rect, border_radius=5)
        pygame.draw.rect(self.image, BORDER_COLOR,
                         button_rect, 2, border_radius=5)

        # Текст кнопки
        btn_text = self.button_font.render("Smelt", True, TEXT_COLOR)
        text_rect = btn_text.get_rect(center=button_rect.center)
        self.image.blit(btn_text, text_rect)

        # Сохраняем кнопку для обработки кликов
        self.buttons.append({
            "rect": button_rect,
            "ore": ore,
            "ingot": ingot,
            "active": can_craft
        })

    def handle_click(self, mouse_pos, mouse_pressed):
        if not self.is_visible:
            return

        self.tick += 1

        rel_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        for button in self.buttons:
            if button["rect"].collidepoint(rel_pos) and button["active"] and mouse_pressed and self.tick % 100 == 0:
                self._smelt_item(button["ore"], button["ingot"])
                mouse_pressed = False

    def _smelt_item(self, ore, ingot):
        if self.inventory.get(ore, 0) >= 3:
            self.inventory[ore] -= 3
            self.inventory[ingot] = self.inventory.get(ingot, 0) + 1

            # Удаляем запись если количество 0
            if self.inventory[ore] == 0:
                del self.inventory[ore]

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def point_in_tile(self, x, y):
        return False


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
            f'block_{type_resource}.png', type_data="block", color_key=-1, scale=(64, 60) if type_resource != "strawberry" else (46, 40)
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
            return "ore_gold", random.randint(1, 3)

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
            return "ore_iron", random.randint(1, 3)

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
            return "ore_stone", random.randint(1, 3)

        return None, None


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", color_key=-1) for _ in range(20)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.35

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


class Furnace(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(forge_group, all_sprites)
        self.image = pygame.transform.scale(
            load_image('furnace.png', color_key=-1),
            (150, 150)
        )
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y

        self.x = self.rect.x
        self.y = self.rect.y

        self.furnace_interface = FurnaceInterface(self.rect.x, self.rect.y)

    def active(self, inventory):
        self.furnace_interface.inventory = inventory.inventory_dict
        self.furnace_interface.toggle_visibility()
        inventory.update_inventory()

    def point_in_tile(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self):
        if self.furnace_interface.is_visible:
            self.furnace_interface.handle_click(
                pygame.mouse.get_pos(), pygame.mouse.get_pressed())


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 60
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def generate_resource():
    with open('levels/main_level.txt', 'r') as f:
        mapa = [el.rstrip("\n") for el in f.readlines()]

    item = ['gold', 'stone', 'iron', 'tree',
            'strawberry'][random.randint(0, 4)]

    x = random.randint(0, len(mapa[0]) - 1)
    y = random.randint(0, len(mapa) - 1)

    while any((
        (mapa[y][x] == '#'),
        (mapa[y][x] == '@')
    )) or regenerate_point(x, y):
        x = random.randint(0, len(mapa[0]) - 1)
        y = random.randint(0, len(mapa) - 1)

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


def regenerate_point(x, y):
    x = tile_width * x
    y = tile_height * y
    for x1 in [x, x + 30, x - 30]:
        for y1 in [y, y + 30, y - 30]:
            for tile in water_group:
                if tile.rect.collidepoint(x1, y1):
                    return True

            for tile in resource_group:
                if tile.rect.collidepoint(x1, y1):
                    return True

            if x1 > 700 or y1 > 600 or x1 < 50 or y1 < 0:
                return True

    return False
