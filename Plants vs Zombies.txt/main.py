import pygame
import time

from card.Card import Card
from plant.Bullet import Bullet
from plant.Bullet_cabbage import Bullet_cabbage
from plant.Cabbage import Cabbage
from plant.Peashooter import Peashooter
from plant.Sun import Sun
from plant.Sun2 import Sun2
from plant.SunFlower import SunFlower
from plant.Wallnut import Wallnut
from zombie.Zombie import Zombie
from zombie.Zombie_lz import Zombie_lz

WIDTH = 820
HEIGHT = 560

pygame.init()
background_size = (WIDTH, HEIGHT)

# 引入资源路径
window = pygame.display.set_mode(background_size)  # 背景大小
pygame.display.set_caption("植物大战僵尸 pygame")
bg_img_obj = pygame.image.load("../pvz/png/background.png").convert_alpha()  # 加载背景图
SunflowerImg = pygame.image.load("../pvz/png/SunFlower/SunFlower_00.png").convert_alpha()  # 加载太阳花
wallnuts_img = pygame.image.load("../pvz/png/Wallnut/Wallnut_00.png").convert_alpha()  # 加载坚果图片
peashooter_img = pygame.image.load("../pvz/png/Peashooter/Peashooter00.png").convert_alpha()  # 加载豌豆射手
cabbage_img = pygame.image.load("../pvz/png/Cabbage/JXC00.png").convert_alpha()  # 加载卷心菜
sunback_img = pygame.image.load("../pvz/png/SeedBank01.png").convert_alpha()  # 阳光图
Sunflower_seed = pygame.image.load("../pvz/png/SunFlower_kp.png")  # 阳光种子图
Wallnuts_seed = pygame.image.load("../pvz/png/Wallnut_kp.png")  # 坚果种子图
Peashooter_seed = pygame.image.load("../pvz/png/Peashooter_kp.png")  # 豌豆射手种子图
Cabbage_seed = pygame.image.load("../pvz/png/jxc_kp.png")  # 卷心菜种子图
defeat_png = pygame.image.load("../pvz/png/Zombie/die/defeat.png")  # 加载失败后的图

# sun_num为阳光值
sun_num = "150"
sun_font = pygame.font.SysFont("黑体", 25)
sun_num_surface = sun_font.render(str(sun_num), True, (0, 0, 0))

# 定义植物组，子弹组，僵尸组，阳光组
plantGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
zombieGroup = pygame.sprite.Group()
sunGroup = pygame.sprite.Group()  # 组列表

# 设置游戏结束背景音乐
GAMEOVER = pygame.USEREVENT
pygame.mixer.music.set_endevent(GAMEOVER)

# 创建时钟对象
clock = pygame.time.Clock()

# 定义各类时间发生的时间
GEN_SUN_EVENT = pygame.USEREVENT + 1  # 定义事件
pygame.time.set_timer(GEN_SUN_EVENT, 2000)  # 定时器
GEN_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GEN_BULLET_EVENT, 2000)
# 太阳出现时间
GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 15000)
GEN_SUN2_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(GEN_SUN2_EVENT, 20000)

choose = 0  # 选择初始化
zombie_num = 0  # 定义僵尸数量
zombie_first = 0  # 第一次僵尸出现

# 载入Bgm
pygame.mixer.init()
pygame.mixer.music.load("./sounds/plant vs zombies.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1, 0.0)


# pygame.mixer.music.stop()

def main():
    global zombie_num
    global choose
    global sun_num
    global sun_num_surface
    global zombie_first
    running = True
    index = 0
    stop = False  # 停止键
    cards = []
    for i in range(4):
        cards.append(Card(window, i))  # 定义一个冷却显示数组
    while running:
        if not stop:  # 当停止未执行时
            clock.tick(20)
            for bullet in bulletGroup:
                for zombie in zombieGroup:
                    if pygame.sprite.collide_mask(bullet, zombie):  # 子弹与僵尸相撞
                        attack = pygame.mixer.Sound("./sounds/attack.wav")
                        attack.set_volume(1)
                        attack.play()
                        if isinstance(bullet, Bullet_cabbage):
                            zombie.energy -= 2  # 卷心菜投手的伤害
                            bulletGroup.remove(bullet)
                        else:
                            zombie.energy -= 1  # 豌豆射手的伤害
                            bulletGroup.remove(bullet)  # 子弹撞击僵尸时
            for plant in plantGroup:
                for zombie in zombieGroup:  # 当植物与僵尸相碰撞时
                    if pygame.sprite.collide_mask(plant, zombie):
                        zombie_eat = pygame.mixer.Sound("./sounds/eat.wav")
                        zombie_eat.set_volume(0.25)
                        zombie_eat.play()
                        zombie.is_go = False
                        plant.zombies.add(zombie)
                    if isinstance(plant, Cabbage):
                        if abs(zombie.rect.top - plant.rect[1]) <= 40 and zombie.rect.left < 760:
                            plant.attack = True
                            if plant.att == 11:
                                bullet_jxc = Bullet_cabbage(plant.rect, background_size, zombie.rect[0])
                                bulletGroup.add(bullet_jxc)
                                break

            window.blit(bg_img_obj, (0, 0))  # 显示背景
            window.blit(sunback_img, (20, 0.5))  # 显示阳光图
            window.blit(sun_num_surface, (35, 50))  # 显示阳光值
            window.blit(Sunflower_seed, (80, 5))  # 显示太阳花种子图
            window.blit(Peashooter_seed, (121, 5))  # 显示豌豆射手种子图
            window.blit(Wallnuts_seed, (162, 5))  # 显示坚果种子图
            window.blit(Cabbage_seed, (203, 5))  # 显示卷心菜种子图
            plantGroup.update(index)
            plantGroup.draw(window)
            bulletGroup.update(index)
            bulletGroup.draw(window)
            zombieGroup.update(index)
            zombieGroup.draw(window)
            sunGroup.update(index)
            sunGroup.draw(window)
            for card in cards:
                card.CD()  # 重新更新和绘制植物，显示冷却图

            # 点击选择植物
            (x, y) = pygame.mouse.get_pos()
            if choose == 1:
                window.blit(SunflowerImg,
                            (x - SunflowerImg.get_rect().width // 2, y - SunflowerImg.get_rect().height // 2))
                cards[0].cd = time.time()
            if choose == 2:
                window.blit(peashooter_img,
                            (x - peashooter_img.get_rect().width // 2, y - peashooter_img.get_rect().height // 2))
                cards[1].cd = time.time()
            if choose == 3:
                window.blit(wallnuts_img,
                            (x - wallnuts_img.get_rect().width // 2, y - wallnuts_img.get_rect().height // 2))
                cards[2].cd = time.time()
            if choose == 4:
                window.blit(cabbage_img,
                            (x - cabbage_img.get_rect().width // 2, y - cabbage_img.get_rect().height // 2))
                cards[3].cd = time.time()

            index += 1  # 索引
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # 当键盘按下停止键时
                    if event.key == pygame.K_p:
                        stop = not stop
                elif event.type == GEN_SUN2_EVENT:  # 一定时间中掉下阳光
                    sun2 = Sun2()
                    sunGroup.add(sun2)
                elif event.type == GEN_ZOMBIE_EVENT:  # 僵尸出现
                    if not zombie_first:
                        begin_sound = pygame.mixer.Sound("./sounds/begin.wav")
                        begin_sound.play()
                        zombie_first = 1
                    zombie_num += 1
                    zombie = Zombie()
                    zombie_lz = Zombie_lz()
                    if 0 < zombie_num <= 15:
                        zombieGroup.add(zombie)
                    if zombie_num > 7:
                        # zombieGroup.add(zombie)
                        zombieGroup.add(zombie_lz)
                elif event.type == GEN_SUN_EVENT:  # 太阳花一段时间掉落的阳光
                    for plant in plantGroup:
                        if isinstance(plant, SunFlower):
                            now = time.time()
                            if now - plant.lasttime >= 10:
                                sun = Sun(plant.rect)
                                sunGroup.add(sun)
                                plant.lasttime = now  # 重置产生阳光出现时间
                elif event.type == GEN_BULLET_EVENT:
                    for plant in plantGroup:
                        for zombie in zombieGroup:
                            if isinstance(plant, Peashooter) \
                                    and 0 < plant.rect[1] - zombie.rect[1] < 50 \
                                    and zombie.rect[0] < 760:  # 当僵尸与植物有一段距离时
                                bullet = Bullet(plant.rect, background_size)
                                bulletGroup.add(bullet)
                                break
                elif event.type == pygame.QUIT:  # 程序终止
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击鼠标时
                    pressed_key = pygame.mouse.get_pressed()  # 鼠标是否被按下
                    if pressed_key[0]:  # 是否按左键
                        pos = pygame.mouse.get_pos()
                        x, y = pos
                        # 根据图大小计算了当什么范围选择什么植物
                        if 80 <= x < 121 and 5 <= y <= 63 and int(sun_num) >= 50 and not cards[0].is_cd:
                            choose = 1
                        elif 121 <= x < 162 and 5 <= y <= 63 and int(sun_num) >= 100 and not cards[1].is_cd:
                            choose = 2
                        elif 162 <= x < 203 and 5 <= y <= 63 and int(sun_num) >= 50 and not cards[2].is_cd:
                            choose = 3
                        elif 203 <= x < 244 and 5 <= y <= 63 and int(sun_num) >= 100 and not cards[3].is_cd:
                            choose = 4
                        elif 36 < x < 800 and 70 < y < 550:
                            if choose == 1:
                                trueX = x // 90 * 85 + 35
                                trueY = y // 100 * 95 - 15
                                canHold = True
                                for plant in plantGroup:
                                    if isinstance(plant, Peashooter):
                                        if plant.rect.left + 3 == trueX and plant.rect.top + 3 == trueY:
                                            canHold = False
                                            break
                                    elif isinstance(plant, Cabbage):
                                        if plant.rect.left + 13 == trueX and plant.rect.top + 20 == trueY:
                                            canHold = False
                                            break
                                    elif plant.rect.left == trueX and plant.rect.top == trueY:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                cards[0].is_cd = True
                                sunflower = SunFlower(time.time(), (trueX, trueY))
                                plantGroup.add(sunflower)
                                choose = 0
                                sun_num = int(sun_num)
                                sun_num -= 50
                                font = pygame.font.SysFont("黑体", 25)  # 字体颜色和大小
                                sun_num_surface = font.render(str(sun_num), True, (0, 0, 0))  # 背景颜色
                            if choose == 2:
                                trueX = x // 90 * 85 + 32
                                trueY = y // 100 * 95 - 18
                                canHold = True
                                for plant in plantGroup:
                                    if isinstance(plant, Cabbage):
                                        if plant.rect.left + 10 == trueX and plant.rect.top + 17 == trueY:
                                            canHold = False
                                            break
                                    elif isinstance(plant, SunFlower) or isinstance(plant, Wallnut):
                                        if plant.rect.left - 3 == trueX and plant.rect.top - 3 == trueY:
                                            canHold = False
                                            break
                                    elif plant.rect.left == trueX and plant.rect.top == trueY:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                cards[1].is_cd = True
                                peashooter = Peashooter((trueX, trueY))
                                plantGroup.add(peashooter)
                                choose = 0
                                sun_num = int(sun_num)
                                sun_num -= 100
                                font = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = font.render(str(sun_num), True, (0, 0, 0))
                            if choose == 3:
                                trueX = x // 90 * 85 + 35
                                trueY = y // 100 * 95 - 15
                                canHold = True
                                for plant in plantGroup:
                                    if isinstance(plant, Peashooter):
                                        if plant.rect.left + 3 == trueX and plant.rect.top + 3 == trueY:
                                            canHold = False
                                            break
                                    elif isinstance(plant, Cabbage):
                                        if plant.rect.left + 13 == trueX and plant.rect.top + 20 == trueY:
                                            canHold = False
                                            break
                                    elif plant.rect.left == trueX and plant.rect.top == trueY:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                cards[2].is_cd = True
                                wallNut = Wallnut((trueX, trueY))
                                plantGroup.add(wallNut)
                                choose = 0
                                sun_num = int(sun_num)
                                sun_num -= 50
                                font = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = font.render(str(sun_num), True, (0, 0, 0))
                            if choose == 4:
                                trueX = x // 90 * 85 + 22
                                trueY = y // 100 * 95 - 35
                                canHold = True
                                for plant in plantGroup:
                                    if isinstance(plant, Peashooter):
                                        if plant.rect.left - 10 == trueX and plant.rect.top - 17 == trueY:
                                            canHold = False
                                            break
                                    elif isinstance(plant, SunFlower) or isinstance(plant, Wallnut):
                                        if plant.rect.left - 13 == trueX and plant.rect.top - 20 == trueY:
                                            canHold = False
                                            break
                                    elif plant.rect.left == trueX and plant.rect.top == trueY:
                                        canHold = False
                                        break
                                if not canHold or trueY < 25:
                                    break
                                cards[3].is_cd = True
                                jxc = Cabbage((trueX, trueY))
                                plantGroup.add(jxc)
                                choose = 0
                                sun_num = int(sun_num)
                                sun_num -= 100
                                font = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = font.render(str(sun_num), True, (0, 0, 0))
                        for sun in sunGroup:
                            if sun.rect.collidepoint(pos):
                                sunGroup.remove(sun)
                                sun_num = str(int(sun_num) + 25)
                                font = pygame.font.SysFont("黑体", 25)
                                sun_num_surface = font.render(str(sun_num), True, (0, 0, 0))
                    if pressed_key[2]:
                        choose = 0
                if event.type == GAMEOVER:
                    window.blit(defeat_png, (20, 0))
                    defeat = pygame.mixer.Sound("./sounds/defeat.wav")
                    defeat.play()
                    # screen.blit(defeat_png,(20,0))
                    time.sleep(2)
                    running = False
                for zombie in zombieGroup:
                    if zombie.rect.left == -120:
                        # defeat = pygame.mixer.Sound("./sounds/defeat.wav")
                        # defeat.play()
                        pygame.mixer.music.stop()
                        print("你的脑子被僵尸吃了")
                        # running = False
                    if zombie_num > 20:
                        victory = pygame.mixer.Sound("./sounds/victory.wav")
                        victory.play()
                        time.sleep(2)
                        print("胜利")
                        running = False
            pygame.display.update()
        elif stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        stop = not stop


if __name__ == '__main__':
    main()
    # pygame.mixer.music.stop()
