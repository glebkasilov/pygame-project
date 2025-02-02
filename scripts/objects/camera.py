from scripts.objects.player import Heart, Player


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if (not isinstance(obj, Player)) and (not isinstance(obj, Heart)):
            obj.rect.x += int(self.dx * 0.084)
            obj.rect.y += int(self.dy * 0.084)
        elif isinstance(obj, Player):
            obj.x += int(self.dx * 0.084)
            obj.y += int(self.dy * 0.084)

        # print(self.dx, self.dy)

    # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.x + target.rect.w // 2 - 800 // 2)
        self.dy = -(target.y + target.rect.h // 2 - 600 // 2)
