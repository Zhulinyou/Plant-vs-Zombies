import pygame


class Bullet_cabbage(pygame.sprite.Sprite):
    def __init__(self, Cabbage_rect, background_size, life1):
        super(Bullet_cabbage, self).__init__()
        self.image = pygame.image.load('../pvz/png/bullet_0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = Cabbage_rect[0] + 50
        self.rect.top = Cabbage_rect[1]
        self.width = background_size[0]
        self.life2 = int(life1 / 120) - int(Cabbage_rect[1] / 200) - 4
        self.speed = 9 + self.life2
        self.a = 0  # 加速度

    def update(self, *args, **kwargs) -> None:
        if self.rect.right < self.width:
            self.rect.left += self.speed
            if self.a < 100:
                y = 8 - self.a
                self.rect.top -= int(y)
                self.a += 0.4
        else:
            self.kill()
