import pygame
import random
import sys
from pygame.locals import *

# 初始化 Pygame，用於設置遊戲引擎
pygame.init()

# 定義遊戲視窗的寬高、幀率等常量
WIDTH, HEIGHT = 800, 600  # 視窗大小
FPS = 60  # 每秒幀數
CAT_OK_SHAKE_DURATION = 500  # cat_ok 晃動持續時間 (毫秒)
CAT_NO_TREMBLE_DURATION = 2000  # cat_no 顫抖持續時間，與顯示時間一致 (毫秒)

# 設定遊戲視窗並命名標題
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("重量級大食客")
clock = pygame.time.Clock()  # 用於控制遊戲幀率

# 設定字體：普通字體和用於暫停標示的大字體
font = pygame.font.SysFont(None, 36)  # 一般 UI 文字大小
large_font = pygame.font.SysFont(None, 72)  # 暫停畫面的大字體

# 初始化音效模組
pygame.mixer.init()

# 載入背景音樂
pygame.mixer.music.load('sound/bgm.mp3')
pygame.mixer.music.set_volume(0.3)  # 設定音量（0.0 到 1.0 範圍）
pygame.mixer.music.play(-1)  # 循環播放 (-1 表示無限循環)

# 載入音效
customer_sound = pygame.mixer.Sound("sound/customer_appears.mp3")
ice_cream_sound = pygame.mixer.Sound("sound/ice_cream.mp3")
wrong_sound = pygame.mixer.Sound("sound/wrong.mp3")
coin_sound = pygame.mixer.Sound("sound/coin.mp3")
click_sound = pygame.mixer.Sound("sound/click.mp3")
bye_bye_sound = pygame.mixer.Sound("sound/bye_bye.mp3")
gameover_sound = pygame.mixer.Sound("sound/gameover.mp3")

# 檢查表面是否有效
def check_surface(surface, name):
    if surface.get_width() == 0 or surface.get_height() == 0:
        print(f"圖片 {name} 載入失敗：無效表面")
        sys.exit()
    # 檢查圖片尺寸（除錯用，可選擇移除）
    expected_width, expected_height = WIDTH, HEIGHT
    if name in ['background', 'cat_ok', 'cat_no', 'counter'] and (surface.get_width() != expected_width or surface.get_height() != expected_height):
        print(f"警告：圖片 {name} 尺寸為 {surface.get_width()}x{surface.get_height()}，預期為 {expected_width}x{expected_height}")
    return surface

# 載入圖片資源
try:
    coin_img = check_surface(pygame.image.load('assest/coin.png').convert_alpha(), 'coin')
    clock_img = check_surface(pygame.image.load('assest/clock.png').convert_alpha(), 'clock')
    game_over_img = check_surface(pygame.image.load('GAMEOVER.svg').convert_alpha(), 'game_over')
    background_img = check_surface(pygame.image.load('assest/background_1.png').convert(), 'background')
    cat_ok_img = check_surface(pygame.image.load('assest/cat_ok.png').convert_alpha(), 'cat_ok')
    cat_no_img = check_surface(pygame.image.load('assest/cat_no.png').convert_alpha(), 'cat_no')
    counter_img = check_surface(pygame.image.load('assest/counter.png').convert_alpha(), 'counter')
except FileNotFoundError as e:
    print(f"載入圖片失敗: {e}")
    sys.exit()

# 載入冰淇淋、杯子/甜筒、Topping 圖片
try:
    items_img = {
        '巧克力': check_surface(pygame.image.load('assest/ice_choco.png').convert_alpha(), 'ice_choco'),
        '芒果': check_surface(pygame.image.load('assest/ice_mango.png').convert_alpha(), 'ice_mango'),
        '哈密瓜': check_surface(pygame.image.load('assest/ice_melon.png').convert_alpha(), 'ice_melon'),
        '柳橙': check_surface(pygame.image.load('assest/ice_orange.png').convert_alpha(), 'ice_orange'),
        '開心果': check_surface(pygame.image.load('assest/ice_pistachio.png').convert_alpha(), 'ice_pistachio'),
        '草莓': check_surface(pygame.image.load('assest/ice_strawberry.png').convert_alpha(), 'ice_strawberry'),
        '芋頭': check_surface(pygame.image.load('assest/ice_taro.png').convert_alpha(), 'ice_taro'),
        '香草': check_surface(pygame.image.load('assest/ice_vanilla.png').convert_alpha(), 'ice_vanilla'),
        '杯子': check_surface(pygame.image.load('assest/cup_o.png').convert_alpha(), 'cup_o'),
        '甜筒': check_surface(pygame.image.load('assest/cone_o.png').convert_alpha(), 'cone_o'),
        '杯子按鈕': check_surface(pygame.image.load('assest/cup.png').convert_alpha(), 'cup'),
        '甜筒按鈕': check_surface(pygame.image.load('assest/cone.png').convert_alpha(), 'cone'),
        '花生': check_surface(pygame.image.load('assest/peanut.png').convert_alpha(), 'peanut'),
        '草莓裝飾': check_surface(pygame.image.load('assest/strawberry.png').convert_alpha(), 'strawberry'),
        '櫻桃': check_surface(pygame.image.load('assest/cherry.png').convert_alpha(), 'cherry'),
        'done': check_surface(pygame.image.load('assest/done.png').convert_alpha(), 'done')
    }
except FileNotFoundError as e:
    print(f"載入圖片失敗: {e}")
    sys.exit()

# 遊戲變數初始化
customer_order = None
money = 0
game_over = False
paused = False
current_order = {'topping': None, 'ice_creams': [], 'base': None}
base_wait_time = 20
wait_time = base_wait_time
current_wait = wait_time
last_update = pygame.time.get_ticks()

# 控制 cat_ok/cat_no 圖片的顯示與效果
show_cat_no = False
cat_no_timer = 0
cat_no_duration = 2000
cat_ok_shake_start_time = None
gameover_sound_played = False  # 遊戲結束音效是否已播放

# 定義按鈕的位置與懸浮狀態
buttons = {
    '開心果': {'rect': pygame.Rect(240, 150, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '芒果': {'rect': pygame.Rect(325, 150, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '芋頭': {'rect': pygame.Rect(410, 150, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '柳橙': {'rect': pygame.Rect(495, 150, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '巧克力': {'rect': pygame.Rect(580, 150, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '哈密瓜': {'rect': pygame.Rect(410, 230, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '草莓': {'rect': pygame.Rect(495, 230, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '香草': {'rect': pygame.Rect(580, 230, 100, 100), 'hover': False, 'type': 'ice_cream'},
    '草莓裝飾': {'rect': pygame.Rect(410, 310, 100, 100), 'hover': False, 'type': 'topping'},
    '花生': {'rect': pygame.Rect(495, 300, 100, 100), 'hover': False, 'type': 'topping'},
    '櫻桃': {'rect': pygame.Rect(580, 310, 100, 100), 'hover': False, 'type': 'topping'},
    '甜筒按鈕': {'rect': pygame.Rect(440, 410, 100, 100), 'hover': False, 'type': 'base', 'value': '甜筒'},
    '杯子按鈕': {'rect': pygame.Rect(560, 420, 100, 100), 'hover': False, 'type': 'base', 'value': '杯子'},
    'done': {'rect': pygame.Rect(370, 500, 100, 100), 'hover': False, 'type': 'done'}
}

# 定義 UI 按鈕區域
pause_button = pygame.Rect(690, 10, 100, 40)
resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
main_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 190, 200, 50)

# 定義層級的固定位置（顧客需求）
CUSTOMER_POSITIONS = {
    'base': {'x': 75, 'y': 330},
    'ice_cream_1': {'x': 75, 'y': 300},
    'ice_cream_2': {'x': 75, 'y': 270},
    'ice_cream_3': {'x': 75, 'y': 240},
    'topping': {'x': 75, 'y': 200}
}

# 定義層級的固定位置（當前製作）
CURRENT_POSITIONS = {
    'base': {'x': 260, 'y': 420},
    'ice_cream_1': {'x': 260, 'y': 390},
    'ice_cream_2': {'x': 260, 'y': 360},
    'ice_cream_3': {'x': 260, 'y': 330},
    'topping': {'x': 260, 'y': 290}
}

# 繪製文字的函數
def draw_text(text, x, y, font=font, color=(0, 0, 0)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 生成新的顧客需求
def generate_customer_order():
    ice_cream_flavors = ['巧克力', '芒果', '哈密瓜', '柳橙', '開心果', '草莓', '芋頭', '香草']
    toppings = ['花生', '草莓裝飾', '櫻桃']
    bases = ['杯子', '甜筒']
    
    order = {
        'topping': random.choice(toppings),
        'ice_creams': random.sample(ice_cream_flavors, random.randint(1, 3)),
        'base': random.choice(bases)
    }
    customer_sound.play()  # 播放新訂單音效
    return order

# 繪製顧客需求
def draw_customer_order(order, shake=False):
    if not order:
        return

    shake_offset = (random.randint(-2, 2), random.randint(-2, 2)) if shake else (0, 0)

    base_img = items_img[order['base']]
    base_pos = CUSTOMER_POSITIONS['base'].copy()
    if order['base'] == '甜筒':
        base_pos = {'x': 75, 'y': 340}
    screen.blit(base_img, (base_pos['x'] + shake_offset[0], base_pos['y'] + shake_offset[1]))

    for i, flavor in enumerate(order['ice_creams']):
        scoop_img = items_img[flavor]
        if i == 0:
            pos = CUSTOMER_POSITIONS['ice_cream_1']
        elif i == 1:
            pos = CUSTOMER_POSITIONS['ice_cream_2']
        else:
            pos = CUSTOMER_POSITIONS['ice_cream_3']
        screen.blit(scoop_img, (pos['x'] + shake_offset[0], pos['y'] + shake_offset[1]))

    topping_img = items_img[order['topping']]
    topping_pos = CUSTOMER_POSITIONS['topping'].copy()
    num_ice_creams = len(order['ice_creams'])
    if num_ice_creams == 3:
        topping_pos['y'] = CUSTOMER_POSITIONS['topping']['y']
    elif num_ice_creams == 2:
        topping_pos['y'] = CUSTOMER_POSITIONS['ice_cream_3']['y']
    else:
        topping_pos['y'] = CUSTOMER_POSITIONS['ice_cream_2']['y']
    screen.blit(topping_img, (topping_pos['x'] + shake_offset[0], topping_pos['y'] + shake_offset[1]))

# 繪製按鈕
def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    for item, data in buttons.items():
        rect = data['rect']
        data['hover'] = rect.collidepoint(mouse_pos)
        offset = -5 if data['hover'] else 0
        screen.blit(items_img[item], (rect.x + 15, rect.y + offset))

# 繪製當前製作的冰淇淋
def draw_current_order():
    if current_order['base']:
        base_img = items_img[current_order['base']]
        base_pos = CURRENT_POSITIONS['base'].copy()
        if current_order['base'] == '甜筒':
            base_pos = {'x': 260, 'y': 430}
        screen.blit(base_img, (base_pos['x'], base_pos['y']))

    for i, flavor in enumerate(current_order['ice_creams']):
        scoop_img = items_img[flavor]
        if i == 0:
            pos = CURRENT_POSITIONS['ice_cream_1']
        elif i == 1:
            pos = CURRENT_POSITIONS['ice_cream_2']
        else:
            pos = CURRENT_POSITIONS['ice_cream_3']
        screen.blit(scoop_img, (pos['x'], pos['y']))

    if current_order['topping']:
        topping_img = items_img[current_order['topping']]
        topping_pos = CURRENT_POSITIONS['topping'].copy()
        num_ice_creams = len(current_order['ice_creams'])
        if num_ice_creams == 3:
            topping_pos['y'] = CURRENT_POSITIONS['topping']['y']
        elif num_ice_creams == 2:
            topping_pos['y'] = CURRENT_POSITIONS['ice_cream_3']['y']
        else:
            topping_pos['y'] = CURRENT_POSITIONS['ice_cream_2']['y']
        screen.blit(topping_img, (topping_pos['x'], topping_pos['y']))

# 繪製 counter 圖片
def draw_counter():
    screen.blit(counter_img, (0, 0))

# 繪製 cat_ok/cat_no 圖片，並加入晃動與顫抖效果
def draw_cat_images():
    cat_img = cat_no_img if show_cat_no else cat_ok_img
    current_time = pygame.time.get_ticks()
    
    # 處理 cat_ok 的晃動效果
    if not show_cat_no and cat_ok_shake_start_time and (current_time - cat_ok_shake_start_time <= CAT_OK_SHAKE_DURATION):
        offset_x = random.randint(-5, 5)  # 隨機水平偏移
        offset_y = random.randint(-5, 5)  # 隨機垂直偏移
        screen.blit(cat_img, (offset_x, offset_y))
    # 處理 cat_no 的顫抖效果
    elif show_cat_no and (current_time - cat_no_timer <= CAT_NO_TREMBLE_DURATION):
        offset_x = random.randint(-2, 2)  # 顫抖幅度較小
        offset_y = random.randint(-2, 2)
        screen.blit(cat_img, (offset_x, offset_y))
    else:
        screen.blit(cat_img, (0, 0))  # 正常繪製

# 繪製 UI 元素（clock, coin, setting）
def draw_ui_decorations():
    screen.blit(coin_img, (20, 0))
    draw_text(f'{money}', 100, 35, color=(0, 0, 0))
    screen.blit(clock_img, (330, 0))
    draw_text(f'{int(current_wait)}', 410, 35, color=(0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), pause_button, border_radius=10)
    draw_text("Pause", 715, 20)

# 繪製暫停選單
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    draw_text("Paused", WIDTH // 2 - 80, HEIGHT // 2 - 100, large_font, (255, 255, 255))
    pygame.draw.rect(screen, (100, 100, 100), resume_button, border_radius=10)
    draw_text("Resume", WIDTH // 2 - 50, HEIGHT // 2 + 60, color=(255, 255, 255))
    pygame.draw.rect(screen, (100, 100, 100), settings_button, border_radius=10)
    draw_text("Settings", WIDTH // 2 - 50, HEIGHT // 2 + 130, color=(255, 255, 255))
    pygame.draw.rect(screen, (100, 100, 100), main_menu_button, border_radius=10)
    draw_text("Main Menu", WIDTH // 2 - 60, HEIGHT // 2 + 200, color=(255, 255, 255))

# 主遊戲迴圈
def main():
    global money, game_over, current_order, paused, customer_order, wait_time, current_wait, last_update, base_wait_time
    global show_cat_no, cat_no_timer, cat_ok_shake_start_time, gameover_sound_played

    if customer_order is None:
        customer_order = generate_customer_order()

    while True:
        if show_cat_no:
            current_time = pygame.time.get_ticks()
            if current_time - cat_no_timer >= cat_no_duration:
                show_cat_no = False
                customer_order = generate_customer_order()
                current_order = {'topping': None, 'ice_creams': [], 'base': None}
                wait_time = base_wait_time
                current_wait = wait_time
                last_update = pygame.time.get_ticks()
        else:
            if not paused:
                current_time = pygame.time.get_ticks()
                if current_time - last_update >= 1000:
                    current_wait -= 1
                    last_update = current_time
                    if current_wait <= 0:
                        customer_order = generate_customer_order()
                        current_order = {'topping': None, 'ice_creams': [], 'base': None}
                        wait_time = base_wait_time
                        current_wait = wait_time
                        last_update = pygame.time.get_ticks()

        # 繪製背景（最底層）
        screen.blit(background_img, (0, 0))

        if not paused:
            # 先繪製 cat_ok/cat_no 圖片
            draw_cat_images()
            # 繪製 counter（在 cat 圖片之後）
            draw_counter()
            # 再繪製冰淇淋相關元素（顧客需求和當前製作）
            shake = current_wait <= 5
            draw_customer_order(customer_order, shake)
            draw_buttons()
            draw_current_order()
            # 最後繪製 UI 元素（clock, coin, pause 等）
            draw_ui_decorations()

        for event in pygame.event.get():
            if event.type == QUIT:
                bye_bye_sound.play()  # 播放關閉音效
                pygame.time.delay(int(bye_bye_sound.get_length() * 1000))  # 等待音效播放完成
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if paused:
                    if resume_button.collidepoint(pos):
                        click_sound.play()  # 播放點擊音效
                        paused = False
                else:
                    if pause_button.collidepoint(pos):
                        click_sound.play()  # 播放點擊音效
                        paused = True
                    elif not game_over:
                        for item, data in buttons.items():
                            if data['rect'].collidepoint(pos):
                                if data['type'] == 'ice_cream' and len(current_order['ice_creams']) < 3:
                                    ice_cream_sound.play()  # 播放製作冰淇淋音效
                                    current_order['ice_creams'].append(item)
                                elif data['type'] == 'base' and not current_order['base']:
                                    ice_cream_sound.play()  # 播放製作冰淇淋音效
                                    current_order['base'] = data['value']
                                elif data['type'] == 'topping' and not current_order['topping']:
                                    ice_cream_sound.play()  # 播放製作冰淇淋音效
                                    current_order['topping'] = item
                                elif data['type'] == 'done':
                                    if (current_order['topping'] and current_order['ice_creams'] and current_order['base']):
                                        if (current_order['topping'] == customer_order['topping'] and
                                            sorted(current_order['ice_creams']) == sorted(customer_order['ice_creams']) and
                                            current_order['base'] == customer_order['base']):
                                            money += 10
                                            coin_sound.play()  # 播放金幣音效
                                            cat_ok_shake_start_time = pygame.time.get_ticks()  # 觸發 cat_ok 晃動
                                            customer_order = generate_customer_order()
                                            base_wait_time = max(8, base_wait_time - 1)
                                            wait_time = base_wait_time
                                            current_wait = wait_time
                                            last_update = pygame.time.get_ticks()
                                        else:
                                            show_cat_no = True
                                            cat_no_timer = pygame.time.get_ticks()
                                            wrong_sound.play()  # 播放錯誤音效
                                            draw_text("錯誤！請重試", CURRENT_POSITIONS['ice_cream_1']['x'] - 20, CURRENT_POSITIONS['base']['y'] + 50, color=(255, 0, 0))
                                            pygame.display.flip()
                                        current_order = {'topping': None, 'ice_creams': [], 'base': None}

        if paused:
            draw_pause_menu()

        if game_over:
            screen.blit(game_over_img, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
            if not gameover_sound_played:
                gameover_sound.play()  # 播放遊戲結束音效
                gameover_sound_played = True

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()