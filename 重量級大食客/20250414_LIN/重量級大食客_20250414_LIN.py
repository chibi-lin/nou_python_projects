import pygame
import random
import sys
from pygame.locals import *

# 初始化 Pygame，用於設置遊戲引擎
pygame.init()

# 定義遊戲視窗的寬高、幀率等常量
WIDTH, HEIGHT = 800, 600  # 視窗大小
FPS = 60  # 每秒幀數
QUEUE_LIMIT = 5  # 螢幕上最多允許的客人數量
NEW_CUSTOMER_INTERVAL = 3000  # 每 3 秒新增一位客人 (毫秒)
SCOOP_RADIUS = 20  # 冰淇淋球的半徑 (未使用)
SHAKE_DURATION = 300  # 錯誤時客人圖示晃動的持續時間 (毫秒)

# 設定遊戲視窗並命名標題
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("重量級大食客")
clock = pygame.time.Clock()  # 用於控制遊戲幀率

# 設定字體：普通字體和用於暫停標示的大字體
font = pygame.font.SysFont(None, 36)  # 一般 UI 文字大小
large_font = pygame.font.SysFont(None, 72)  # 暫停畫面的大字體

# 載入並縮放圖片資源
person_img = pygame.image.load('person.svg').convert_alpha()  # 客人圖示
person_img = pygame.transform.scale(person_img, (60, 60))  # 縮放到 60x60
coin_img = pygame.image.load('錢幣.svg').convert_alpha()  # 金幣圖示
coin_img = pygame.transform.scale(coin_img, (30, 30))  # 縮放到 30x30
game_over_img = pygame.image.load('GAMEOVER.svg').convert_alpha()  # 遊戲結束圖示
game_over_img = pygame.transform.scale(game_over_img, (400, 200))  # 縮放到 400x200

# 載入並縮放冰淇淋圖片
ice_cream_tubs_img = {
    '巧克力': pygame.image.load('巧克力.svg').convert_alpha(),
    '草莓': pygame.image.load('草莓.svg').convert_alpha(),
    '香草': pygame.image.load('香草.svg').convert_alpha()
}
for flavor in ice_cream_tubs_img:
    ice_cream_tubs_img[flavor] = pygame.transform.scale(ice_cream_tubs_img[flavor], (40, 40))  # 縮放到 40x40

# 遊戲變數初始化
customers = []  # 儲存當前客人的訂單
money = 0  # 玩家賺到的金錢
total_customers = 0  # 總來客數
last_customer_time = pygame.time.get_ticks()  # 上次新增客人的時間
game_over = False  # 遊戲結束標誌
paused = False  # 暫停狀態標誌
current_order = []  # 玩家當前製作的冰淇淋口味
shake_start_time = None  # 錯誤時晃動效果的開始時間

# 定義冰淇淋桶的位置與懸浮狀態
ice_cream_tubs = {
    '巧克力': {'rect': pygame.Rect(50, 500, 100, 50), 'hover': False},  # 巧克力桶位置與懸浮標誌
    '香草': {'rect': pygame.Rect(200, 500, 100, 50), 'hover': False},   # 香草桶位置與懸浮標誌
    '草莓': {'rect': pygame.Rect(350, 500, 100, 50), 'hover': False}     # 草莓桶位置與懸浮標誌
}

# 客人圖示的起始座標
customer_start_x = 50
customer_start_y = 100

# 定義 UI 按鈕區域
pause_button = pygame.Rect(WIDTH - 110, 10, 100, 40)  # 暫停按鈕 (右上角)
resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)  # 暫停選單的返回遊戲按鈕
settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)  # 暫停選單的設定按鈕
main_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 190, 200, 50)  # 暫停選單的主畫面按鈕

# 繪製文字的函數
def draw_text(text, x, y, font=font, color=(0, 0, 0)):
    img = font.render(text, True, color)  # 渲染文字
    screen.blit(img, (x, y))  # 將文字畫到螢幕上

# 新增客人的函數
def add_customer():
    global game_over, total_customers
    if len(customers) < QUEUE_LIMIT:  # 如果客人數量未達上限
        order = random.choices(['巧克力', '香草', '草莓'], k=3)  # 隨機生成 3 個口味的訂單
        customers.append(order)  # 加入客人清單
        total_customers += 1  # 總來客數增加
    else:
        game_over = True  # 超過上限，遊戲結束

# 繪製客人和他們的訂單
def draw_customers():
    for index, customer in enumerate(customers):  # 遍歷所有客人
        x_pos = customer_start_x + index * 130  # 計算每個客人的水平位置
        y_pos = customer_start_y  # 固定垂直位置
        screen.blit(person_img, (x_pos, y_pos))  # 繪製客人圖示
        for i, flavor in enumerate(customer):  # 繪製客人訂單的冰淇淋
            scoop_img = pygame.transform.scale(ice_cream_tubs_img[flavor], (20, 20))  # 縮小冰淇淋圖示
            screen.blit(scoop_img, (x_pos + 10 + i * 25, y_pos + 65))  # 在客人下方顯示訂單

# 繪製冰淇淋桶並實現懸浮效果
def draw_ice_cream_tubs():
    mouse_pos = pygame.mouse.get_pos()  # 獲取滑鼠位置
    for flavor, data in ice_cream_tubs.items():
        rect = data['rect']  # 冰淇淋桶的區域
        data['hover'] = rect.collidepoint(mouse_pos)  # 檢查滑鼠是否懸浮在桶上
        offset = -5 if data['hover'] else 0  # 懸浮時向上偏移 5 像素
        pygame.draw.rect(screen, (200, 200, 200), rect.move(0, offset))  # 繪製桶的背景
        screen.blit(ice_cream_tubs_img[flavor], (rect.x + 30, rect.y + offset))  # 繪製冰淇淋圖示
        draw_text("x99", rect.x + 35, rect.y + 45 + offset)  # 顯示假的冰淇淋數量

# 繪製當前製作的冰淇淋訂單
def draw_current_order():
    # 無白色背景，直接顯示文字和圖示
    draw_text("Making:", WIDTH // 2 - 80, HEIGHT // 2 - 40)  # 顯示「製作中」標籤
    for i, flavor in enumerate(current_order):  # 遍歷當前選擇的口味
        scoop_img = pygame.transform.scale(ice_cream_tubs_img[flavor], (30, 30))  # 縮放冰淇淋圖示
        screen.blit(scoop_img, (WIDTH // 2 - 60 + i * 40, HEIGHT // 2 - 10))  # 在中間顯示選擇的口味

# 繪製 UI 元素
def draw_ui_decorations():
    # 顯示金錢 (左上角)
    screen.blit(coin_img, (10, 10))  # 繪製金幣圖示
    draw_text(f'{money}', 50, 10)  # 顯示當前金錢數量
    
    # 顯示總來客數 (左上角，緊接金錢)
    draw_text(f"總人數: {total_customers}", 120, 10)  # 顯示總來客數
    
    # 顯示假的時間條 (中間上方)
    draw_text("Time: 02:45", WIDTH // 2 - 50, 10)  # 固定顯示時間，未實作計時功能
    
    # 顯示暫停按鈕 (右上角)
    pygame.draw.rect(screen, (100, 100, 100), pause_button, border_radius=10)  # 繪製暫停按鈕背景
    draw_text("Pause", WIDTH - 85, 20)  # 顯示「Pause」文字

# 繪製暫停選單
def draw_pause_menu():
    # 繪製半透明背景
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # 黑色，透明度 180
    screen.blit(overlay, (0, 0))
    
    # 顯示「Paused」標示
    draw_text("Paused", WIDTH // 2 - 80, HEIGHT // 2 - 100, large_font, (255, 255, 255))  # 大字體顯示「Paused」
    
    # 繪製返回遊戲按鈕
    pygame.draw.rect(screen, (100, 100, 100), resume_button, border_radius=10)  # 按鈕背景
    draw_text("Resume", WIDTH // 2 - 50, HEIGHT // 2 + 60, color=(255, 255, 255))  # 按鈕文字
    
    # 繪製設定按鈕 (未實作功能)
    pygame.draw.rect(screen, (100, 100, 100), settings_button, border_radius=10)
    draw_text("Settings", WIDTH // 2 - 50, HEIGHT // 2 + 130, color=(255, 255, 255))
    
    # 繪製主畫面按鈕 (未實作功能)
    pygame.draw.rect(screen, (100, 100, 100), main_menu_button, border_radius=10)
    draw_text("Main Menu", WIDTH // 2 - 60, HEIGHT // 2 + 200, color=(255, 255, 255))

# 主遊戲迴圈
def main():
    global last_customer_time, money, game_over, current_order, shake_start_time, paused, total_customers

    while True:
        screen.fill((173, 216, 230))  # 清空螢幕並填充淺藍色背景

        if not paused:  # 非暫停狀態下繪製遊戲內容
            draw_ui_decorations()  # 繪製 UI (金錢、來客數、時間、暫停按鈕)
            draw_customers()  # 繪製客人及其訂單
            draw_ice_cream_tubs()  # 繪製冰淇淋桶
            draw_current_order()  # 繪製當前製作的冰淇淋

        for event in pygame.event.get():  # 處理事件
            if event.type == QUIT:  # 關閉視窗
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:  # 滑鼠點擊事件
                pos = pygame.mouse.get_pos()  # 獲取滑鼠點擊位置
                if paused:  # 暫停狀態
                    if resume_button.collidepoint(pos):  # 點擊返回遊戲
                        paused = False
                    # 設定和主畫面按鈕未實作功能
                else:  # 遊戲進行中
                    if pause_button.collidepoint(pos):  # 點擊暫停按鈕
                        paused = True
                    elif not game_over:  # 非遊戲結束狀態
                        for flavor, data in ice_cream_tubs.items():  # 檢查點擊冰淇淋桶
                            if data['rect'].collidepoint(pos):
                                if len(current_order) < 3:  # 當前訂單未滿 3 個口味
                                    current_order.append(flavor)  # 新增口味到訂單
                                    if len(current_order) == 3:  # 訂單滿 3 個口味
                                        if current_order == customers[0]:  # 訂單正確
                                            money += 10  # 增加金錢
                                            customers.pop(0)  # 移除第一位客人
                                        else:  # 訂單錯誤
                                            shake_start_time = pygame.time.get_ticks()  # 觸發晃動效果
                                        current_order = []  # 清空當前訂單

        if paused:  # 暫停狀態下繪製暫停選單
            draw_pause_menu()
        else:  # 非暫停狀態，更新遊戲邏輯
            current_time = pygame.time.get_ticks()  # 獲取當前時間
            if not game_over and current_time - last_customer_time >= NEW_CUSTOMER_INTERVAL:  # 定時新增客人
                add_customer()
                last_customer_time = current_time

            # 處理錯誤晃動效果
            if shake_start_time and current_time - shake_start_time <= SHAKE_DURATION:
                offset = random.randint(-5, 5)  # 隨機偏移
                screen.blit(person_img, (customer_start_x + offset, customer_start_y))  # 繪製晃動的客人圖示
            else:
                shake_start_time = None  # 結束晃動

            # 顯示遊戲結束畫面
            if game_over:
                screen.blit(game_over_img, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

        pygame.display.flip()  # 更新螢幕顯示
        clock.tick(FPS)  # 控制遊戲幀率

# 程式入口
if __name__ == "__main__":
    main()