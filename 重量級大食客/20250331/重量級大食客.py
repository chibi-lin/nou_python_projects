import pygame
import random
import sys
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 常量定義
WIDTH, HEIGHT = 800, 600
FPS = 60
QUEUE_LIMIT = 5  # 改為最多允許 5 個客人在螢幕上
NEW_CUSTOMER_INTERVAL = 3000  # 每 3 秒新增一位客人 (毫秒)
SCOOP_RADIUS = 20
SHAKE_DURATION = 300  # 錯誤後晃動的持續時間 (毫秒)

# 設定遊戲視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("重量級大食客")
clock = pygame.time.Clock()

# 字體設定
font = pygame.font.SysFont(None, 36)

# 載入圖片
person_img = pygame.image.load('person.svg').convert_alpha()
person_img = pygame.transform.scale(person_img, (60, 60))
coin_img = pygame.image.load('錢幣.svg').convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))
game_over_img = pygame.image.load('GAMEOVER.svg').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (400, 200))

ice_cream_tubs_img = {
    '巧克力': pygame.image.load('巧克力.svg').convert_alpha(),
    '草莓': pygame.image.load('草莓.svg').convert_alpha(),
    '香草': pygame.image.load('香草.svg').convert_alpha()
}

for flavor in ice_cream_tubs_img:
    ice_cream_tubs_img[flavor] = pygame.transform.scale(ice_cream_tubs_img[flavor], (40, 40))

# 遊戲變數
customers = []
money = 0
last_customer_time = pygame.time.get_ticks()
game_over = False
current_order = []
shake_start_time = None

# 冰淇淋桶位置
ice_cream_tubs = {
    '巧克力': pygame.Rect(50, 500, 100, 50),
    '香草': pygame.Rect(200, 500, 100, 50),
    '草莓': pygame.Rect(350, 500, 100, 50)
}

# 客人座標起始點
customer_start_x = 50
customer_start_y = 100


def draw_text(text, x, y):
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (x, y))


def add_customer():
    global game_over
    if len(customers) < QUEUE_LIMIT:
        order = random.choices(['巧克力', '香草', '草莓'], k=3)
        customers.append(order)
    else:
        game_over = True


def draw_customers():
    for index, customer in enumerate(customers):
        y_pos = customer_start_y + index * 70
        screen.blit(person_img, (customer_start_x, y_pos))
        for i, flavor in enumerate(customer):
            scoop_img = pygame.transform.scale(ice_cream_tubs_img[flavor], (20, 20))
            screen.blit(scoop_img, (customer_start_x + 70 + i * 30, y_pos + 20))


def draw_ice_cream_tubs():
    for flavor, rect in ice_cream_tubs.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)
        screen.blit(ice_cream_tubs_img[flavor], (rect.x + 30, rect.y))


def main():
    global last_customer_time, money, game_over, current_order, shake_start_time

    while True:
        screen.fill((173, 216, 230))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                for flavor, rect in ice_cream_tubs.items():
                    if rect.collidepoint(pos):
                        if len(current_order) < 3:
                            current_order.append(flavor)
                            if len(current_order) == 3:
                                if current_order == customers[0]:
                                    money += 10
                                    customers.pop(0)
                                else:
                                    shake_start_time = pygame.time.get_ticks()
                                current_order = []

        current_time = pygame.time.get_ticks()
        if not game_over and current_time - last_customer_time >= NEW_CUSTOMER_INTERVAL:
            add_customer()
            last_customer_time = current_time

        if shake_start_time and current_time - shake_start_time <= SHAKE_DURATION:
            offset = random.randint(-5, 5)
            screen.blit(person_img, (customer_start_x + offset, customer_start_y))
        else:
            shake_start_time = None

        draw_customers()
        draw_ice_cream_tubs()
        screen.blit(coin_img, (10, 10))  # 顯示金幣圖片
        draw_text(f'{money}', 50, 10)

        if game_over:
            screen.blit(game_over_img, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
