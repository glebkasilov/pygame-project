from scripts.objects.objects import Furnace, Tile
from scripts.objects.player import Player


def load_level(filename):
    filename = "levels/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, "grount_group")
            elif level[y][x] == '#':
                Tile('water', x, y, "water_group")
            elif level[y][x] == '@':
                Tile('empty', x, y, "grount_group")
                new_player = Player(x, y)
            elif level[y][x] == '+':
                Tile('empty', x, y, "grount_group")
                Furnace(x, y)

    return new_player, x, y


def update_level(player, level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, "grount_group")
            elif level[y][x] == '#':
                Tile('water', x, y, "water_group")
            elif level[y][x] == '@':
                Tile('empty', x, y, "grount_group")
                player.rect.x = x
                player.rect.y = y

    return None
