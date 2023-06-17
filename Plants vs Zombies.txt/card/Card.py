import pygame
import time
time1=[5,7,5,10]

class Card(pygame.sprite.Sprite):
    def __init__(self, screen, column):
        pygame.sprite.Sprite.__init__(self)
        self.column = column
        self.screen = screen
        self.x, self.y = 80 + 41 * self.column, 5
        self.w, self.h = 42, 58
        self.is_cd = True
        self.cd = time.time()
        self.cd_time = time1[column]

    def CD(self):  # 进入CD冷却画面
        if time.time() - self.cd < self.cd_time:
            progress = (time.time() - self.cd) / self.cd_time  # 计算冷却进度百分比
            height = self.h - int(self.h * progress)  # 冷却矩阵的高度
            cooldown_surface = pygame.Surface((self.w, height))
            cooldown_surface.set_colorkey((255, 255, 255))
            cooldown_surface.fill((0, 0, 0))  # 绘制冷却矩阵
            cooldown_surface.set_alpha(140)  # 设置透明度
            self.screen.blit(cooldown_surface, (self.x, self.y))
        else:
            self.is_cd = False

# pygame.init()
# screen = pygame.display.set_mode((820, 560))
# g_img_obj = pygame.image.load("../pvz/png/a3.png").convert_alpha()
# sunflower_seed = pygame.image.load("../pvz/png/SunFlower_kp.png")
# clock = pygame.time.Clock()
# while True:
#     clock.tick(20)
#     screen.blit(g_img_obj, (0, 0))
#     # screen.blit(sunflower_seed, (80, 5))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             key = pygame.mouse.get_pos()
#             if key[0]:
#                 card = Card(screen, 0)
#                 card.CD()
#     pygame.display.update()
