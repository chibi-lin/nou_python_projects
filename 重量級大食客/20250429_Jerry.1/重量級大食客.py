import pygame
import random
import sys

pygame.init()# 初始化 Pygame，用於設置遊戲引擎

# 定義遊戲視窗的寬高、幀率等常量
WIDTH, HEIGHT = 800, 600  # 視窗大小
FPS = 60  # 每秒幀數
CAT_OK_SHAKE_DURATION = 500  # cat_ok 晃動持續時間 (毫秒)
CAT_NO_TREMBLE_DURATION = 2000  # cat_no 顫抖持續時間，與顯示時間一致 (毫秒)

# 設定遊戲視窗並命名標題
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("重量級大食客")
clock = pygame.time.Clock()  # 用於控制遊戲幀率

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

# 載入圖片資源
start_screen_img = pygame.image.load('assest/start_screen.png')
background_img = pygame.image.load('assest/background_1.png')
game_over_img = pygame.image.load('assest/GAMEOVER.png')
cat_ok_img = pygame.image.load('assest/cat_ok.png')
cat_bye_img = pygame.image.load('assest/cat_bye.png')
cat_no_img = pygame.image.load('assest/cat_no.png')
counter_img = pygame.image.load('assest/counter.png')

# 載入冰淇淋、杯子/甜筒、Topping 圖片
items_img = {
    '芋頭': pygame.image.load('assest/ice_taro.png'),
    '開心果': pygame.image.load('assest/ice_pistachio.png'),
    '哈密瓜': pygame.image.load('assest/ice_melon.png'),
    '柳橙': pygame.image.load('assest/ice_orange.png'),
    '芒果': pygame.image.load('assest/ice_mango.png'),
    '草莓': pygame.image.load('assest/ice_strawberry.png'),
    '巧克力': pygame.image.load('assest/ice_choco.png'),
    '香草': pygame.image.load('assest/ice_vanilla.png'),
    '草莓裝飾': pygame.image.load('assest/strawberry.png'),
    '花生': pygame.image.load('assest/peanut.png'),
    '櫻桃': pygame.image.load('assest/cherry.png'),
    '甜筒': pygame.image.load('assest/cone_o.png'),
    '甜筒按鈕': pygame.image.load('assest/cone.png'),
    '杯子': pygame.image.load('assest/cup_o.png'),
    '杯子按鈕': pygame.image.load('assest/cup.png'),
    'done': pygame.image.load('assest/done.png')
}

# 遊戲變數初始化
screen_stage = 0  # 0=開始畫面, 1=說明畫面, 2=遊戲中
settings_from_stage = 0
paused = False
pause_start_ticks = 0
total_paused_time = 0
first_start_clicked_time = None  # 一開始是 None
first_start_clicked = False      # 確保只記錄一次
customer_order = None
current_order = {'topping': None, 'ice_creams': [], 'base': None}
base_wait_time = 20
wait_time = base_wait_time
current_wait = wait_time
last_update = pygame.time.get_ticks()
money = 0
gametime = 120
remaining_seconds = None
game_over = False

# 控制 cat_ok/cat_no 圖片的顯示與效果
show_cat_no = False
cat_no_timer = 0
cat_no_duration = 2000
cat_ok_shake_start_time = None
gameover_sound_played = False  # 遊戲結束音效是否已播放

# 定義冰淇淋組件變數
ice_cream_flavors = ['香草', '巧克力', '草莓']
ice_cream_flavors_add = ['芒果', '柳橙', '哈密瓜', '開心果', '芋頭']
toppings = ['花生', '草莓裝飾', '櫻桃']
bases = ['杯子', '甜筒']

# 定義按鈕的位置與懸浮狀態
buttons = {
    '芋頭': {'rect': pygame.Rect(240, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
    '開心果': {'rect': pygame.Rect(325, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
    '哈密瓜': {'rect': pygame.Rect(410, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
    '柳橙': {'rect': pygame.Rect(495, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
    '芒果': {'rect': pygame.Rect(580, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
    '草莓': {'rect': pygame.Rect(410, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
    '巧克力': {'rect': pygame.Rect(495, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
    '香草': {'rect': pygame.Rect(580, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
    '草莓裝飾': {'rect': pygame.Rect(410, 310, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
    '花生': {'rect': pygame.Rect(495, 300, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
    '櫻桃': {'rect': pygame.Rect(580, 310, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
    '甜筒按鈕': {'rect': pygame.Rect(440, 410, 100, 100), 'hover': False, 'type': 'base', 'visible': True,
                 'value': '甜筒'},
    '杯子按鈕': {'rect': pygame.Rect(560, 420, 100, 100), 'hover': False, 'type': 'base', 'visible': True,
                 'value': '杯子'},
    'done': {'rect': pygame.Rect(370, 500, 100, 100), 'hover': False, 'type': 'done', 'visible': True}
}
def replay_game():
    global screen_stage, settings_from_stage, settings_from_stage, paused, pause_start_ticks, total_paused_time, first_start_clicked_time
    global first_start_clicked, customer_order, current_order, wait_time, current_wait, last_update, money, remaining_seconds, game_over
    global show_cat_no, cat_no_timer, cat_no_duration, cat_ok_shake_start_time, gameover_sound_played, ice_cream_flavors, ice_cream_flavors_add
    global buttons
    # 遊戲變數初始化
    screen_stage = 0  # 0=開始畫面, 1=說明畫面, 2=遊戲中
    settings_from_stage = 0
    paused = False
    pause_start_ticks = 0
    total_paused_time = 0
    first_start_clicked_time = None  # 一開始是 None
    first_start_clicked = False  # 確保只記錄一次
    customer_order = None
    current_order = {'topping': None, 'ice_creams': [], 'base': None}
    wait_time = base_wait_time
    current_wait = wait_time
    last_update = pygame.time.get_ticks()
    money = 0
    remaining_seconds = None
    game_over = False
    show_cat_no = False
    cat_no_timer = 0
    cat_no_duration = 2000
    cat_ok_shake_start_time = None
    gameover_sound_played = False  # 遊戲結束音效是否已播放
    ice_cream_flavors = ['香草', '巧克力', '草莓']
    ice_cream_flavors_add = ['芒果', '柳橙', '哈密瓜', '開心果', '芋頭']
    buttons = {
        '芋頭': {'rect': pygame.Rect(240, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
        '開心果': {'rect': pygame.Rect(325, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
        '哈密瓜': {'rect': pygame.Rect(410, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
        '柳橙': {'rect': pygame.Rect(495, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
        '芒果': {'rect': pygame.Rect(580, 150, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': False},
        '草莓': {'rect': pygame.Rect(410, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
        '巧克力': {'rect': pygame.Rect(495, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
        '香草': {'rect': pygame.Rect(580, 230, 100, 100), 'hover': False, 'type': 'ice_cream', 'visible': True},
        '草莓裝飾': {'rect': pygame.Rect(410, 310, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
        '花生': {'rect': pygame.Rect(495, 300, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
        '櫻桃': {'rect': pygame.Rect(580, 310, 100, 100), 'hover': False, 'type': 'topping', 'visible': True},
        '甜筒按鈕': {'rect': pygame.Rect(440, 410, 100, 100), 'hover': False, 'type': 'base', 'visible': True,
                     'value': '甜筒'},
        '杯子按鈕': {'rect': pygame.Rect(560, 420, 100, 100), 'hover': False, 'type': 'base', 'visible': True,
                     'value': '杯子'},
        'done': {'rect': pygame.Rect(370, 500, 100, 100), 'hover': False, 'type': 'done', 'visible': True}
    }

# 定義 UI 按鈕區域
quit_button = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 210, 150, 50)
settings_0_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 210, 150, 50)
back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
next_button = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 + 210, 150, 50)
prev_button = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 210, 200, 50)
start_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 210, 200, 50)
pause_button = pygame.Rect(680, 25, 100, 40)
resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
main_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 190, 200, 50)
replay_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 210, 200, 50)

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

# 設定字體：普通字體和用於暫停標示的大字體
font = pygame.font.SysFont(None, 36)  # 一般 UI 文字大小
large_font = pygame.font.SysFont(None, 72)  # 暫停畫面的大字體
font_bye = pygame.font.SysFont(None, 60)  # game 畫面 得到多少金幣文字大小

# 繪製文字的函數
def draw_text(text, x, y, font_obj=font, color=(0, 0, 0)):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

# 多行文字函數
def draw_text_multiline(text, x, y, font_size=28, color=(0, 0, 0), line_spacing=10):
    temp_font = pygame.font.SysFont('Microsoft JhengHei', font_size)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = temp_font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * (font_size + line_spacing)))

# 繪製開始畫面
def draw_start_screen():
    start_screen_1_img = pygame.transform.scale(start_screen_img, (WIDTH, HEIGHT)) # 調整背景圖尺寸
    screen.blit(start_screen_1_img, (0, 0))  # 繪製開始畫面背景
    pygame.draw.rect(screen, (180, 160, 140), next_button, border_radius=10)  # NEXT按鈕背景
    draw_text("NEXT", WIDTH // 2 + 145, HEIGHT // 2 + 225, color=(255, 255, 255))  # NEXT按鈕文字
    pygame.draw.rect(screen, (180, 160, 140), settings_0_button, border_radius=10)  # settings按鈕背景
    draw_text("SETTINGS", WIDTH // 2 - 62, HEIGHT // 2 + 225, color=(255, 255, 255))  # settings按鈕文字
    pygame.draw.rect(screen, (180, 160, 140), quit_button, border_radius=10)  # QUIT按鈕背景
    draw_text("QUIT", WIDTH // 2 - 203, HEIGHT // 2 + 225, color=(255, 255, 255))  # QUIT按鈕文字

# 結束遊戲
def quit_game():
    bye_bye_sound.play()  # 播放關閉音效
    pygame.time.delay(int(bye_bye_sound.get_length() * 1000))  # 等待音效播放完成
    pygame.quit()
    sys.exit()

# 繪製設定畫面
def draw_settings_menu():
    global screen_stage
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((150, 170, 200, 180))
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, (100, 100, 100), back_button, border_radius=10)
    draw_text("Back", WIDTH // 2 - 30, HEIGHT // 2 + 130, color=(255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if back_button.collidepoint(pos):
                click_sound.play()
                if settings_from_stage == 0:
                    screen_stage = 0  # 回主選單
                elif settings_from_stage == 2:
                    screen_stage = 2  # 回暫停畫面
                return

# 繪製規則畫面
def draw_rule_screen():
    start_screen_1_img = pygame.transform.scale(start_screen_img, (WIDTH, HEIGHT)) # 調整背景圖尺寸
    screen.blit(start_screen_1_img, (0, 0))  # 繪製開始畫面背景
    pygame.draw.rect(screen, (180, 160, 140), start_button, border_radius=10)  # START按鈕背景
    draw_text("START", WIDTH // 2 + 115, HEIGHT // 2 + 225, color=(255, 255, 255))  # START按鈕文字
    pygame.draw.rect(screen, (180, 160, 140), prev_button, border_radius=10)  # Prev按鈕背景
    draw_text("Prev", WIDTH // 2 - 180, HEIGHT // 2 + 225, color=(255, 255, 255))  # Prev按鈕文字

    # 畫淺白色圓角框
    rect_alpha = 220
    rect_width, rect_height = 500, 300
    rect_x = (WIDTH - rect_width) // 2
    rect_y = (HEIGHT - rect_height) // 2

    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 0))  # 完全透明背景
    pygame.draw.rect(rect_surface, (255, 255, 255, rect_alpha), (0, 0, rect_width, rect_height), border_radius=20)
    screen.blit(rect_surface, (rect_x, rect_y))

    # 顯示規則文字
    draw_text_multiline(
        "遊戲規則：\n"
        "1. 請依照客人要求，製作冰淇淋。\n"
        "2. 隨著完成訂單數增加，客人容忍等\n"
        "   候時間將下降。\n"
        "3. 每獲得30元利潤，將研發新口味。\n"
        "4. 倒數計時結束則遊戲結束，來挑戰\n"
        "   看看你能賺多少錢吧！",
        rect_x + 30, rect_y + 15
    )

# 生成新的顧客需求
def generate_customer_order():
    order = {
        'topping': random.choice(toppings),
        'ice_creams': random.sample(ice_cream_flavors, random.randint(1, 3)),
        'base': random.choice(bases)
    }
    customer_sound.play()  # 播放新訂單音效
    return order

# 繪製 cat_ok/cat_no 圖片，並加入晃動與顫抖效果
def draw_cat_images():
    cat_img = cat_no_img if show_cat_no else cat_ok_img
    current_time = pygame.time.get_ticks()
    # 處理 cat_ok 的晃動效果
    if not show_cat_no and cat_ok_shake_start_time and (
            current_time - cat_ok_shake_start_time <= CAT_OK_SHAKE_DURATION):
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

# 繪製 counter 圖片
def draw_counter():
    screen.blit(counter_img, (0, 0))

# 繪製顧客需求
def draw_customer_order(order, shake=False):
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
        if data['visible']:
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

# 繪製 UI 元素（clock, coin, setting）
def draw_ui_decorations():
    global remaining_seconds
    coin_img = pygame.image.load('assest/coin.png')
    screen.blit(coin_img, (20, 0))
    draw_text(f'{money}', 100, 35, color=(0, 0, 0))

    wait_time_img = pygame.image.load('assest/wait_time.png')
    screen.blit(wait_time_img, (230, 20))
    draw_text(f'{int(current_wait)}', 300, 35, color=(0, 0, 0))

    clock_img = pygame.image.load('assest/clock.png')
    screen.blit(clock_img, (410, -2))  # 繪製時間條圖示

    pygame.draw.rect(screen, (100, 100, 100), pause_button, border_radius=10)
    draw_text("Pause", 695, 33)

    remaining_seconds = max(0, gametime - ((pygame.time.get_ticks() - total_paused_time - first_start_clicked_time) // 1000))  # 計算剩下幾秒，如果剩下是負數，就變成 0
    minutes = remaining_seconds // 60  # 轉成分:秒格式，取分值
    seconds = remaining_seconds % 60  # 轉成分:秒格式，取秒值
    time_text = f" {minutes:02d}:{seconds:02d}"  # 分:秒格式
    draw_text(time_text, 480, 35)  # 顯示剩餘時間

# 加入新口味
def unlock_new_flavor():
    if money % 30 == 0 and ice_cream_flavors_add:
        new_flavor = ice_cream_flavors_add.pop(0)  # 拿出一個新口味
        buttons[new_flavor]['visible'] = True  # 把新口味按鈕打開
        ice_cream_flavors.append(new_flavor)  # 加進主口味列表

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

# 繪製GAMEOVER畫面
def draw_gameover():
    global gameover_sound_played, game_over_img, cat_bye_img, screen_stage
    screen.blit(background_img, (0, 0))  # 繪製背景
    game_over_img = pygame.transform.scale(game_over_img, (450, 330)) # 調整背景圖尺寸
    screen.blit(game_over_img, (235, 170))
    cat_bye_img = pygame.transform.scale(cat_bye_img, (150, 180)) # 調整貓bye圖尺寸
    screen.blit(cat_bye_img, (535, 320))
    pygame.draw.rect(screen, (180, 160, 140), start_button, border_radius=10)  # replay按鈕背景
    draw_text("Replay", WIDTH // 2 + 115, HEIGHT // 2 + 225, color=(255, 255, 255))  # replay按鈕文字
    pygame.draw.rect(screen, (180, 160, 140), prev_button, border_radius=10)  # quit按鈕背景
    draw_text("Quit", WIDTH // 2 - 180, HEIGHT // 2 + 225, color=(255, 255, 255))  # quit按鈕文字
    draw_text('You get 'f'{money}'' coin',245, 430, font_bye, (255, 127, 127))

    if not gameover_sound_played:
        gameover_sound.play()  # 播放遊戲結束音效
        gameover_sound_played = True
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if quit_button.collidepoint(pos):
                quit_game()
            if replay_button.collidepoint(pos):
                replay_game()
                return

# 遊戲迴圈
def run_gameplay():
    global money, game_over, current_order, paused, customer_order, wait_time, current_wait, last_update, base_wait_time, pause_start_ticks, total_paused_time
    global show_cat_no, cat_no_timer, cat_ok_shake_start_time, gameover_sound_played
    global ice_cream_flavors, ice_cream_flavors_add, screen_stage, settings_from_stage
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
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if paused:
                    if resume_button.collidepoint(pos):
                        click_sound.play()  # 播放點擊音效
                        paused = False
                        total_paused_time += pygame.time.get_ticks() - pause_start_ticks
                    elif settings_button.collidepoint(pos):
                        click_sound.play()  # 播放點擊音效
                        settings_from_stage = screen_stage
                        screen_stage = 3
                        return
                    elif main_menu_button.collidepoint(pos):
                        click_sound.play()
                        screen_stage = 0
                        return

                else:
                    if pause_button.collidepoint(pos):
                        click_sound.play()  # 播放點擊音效
                        paused = True
                        pause_start_ticks = pygame.time.get_ticks()
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
                                    if (current_order['topping'] and current_order['ice_creams'] and current_order[
                                        'base']):
                                        if (current_order['topping'] == customer_order['topping'] and
                                                sorted(current_order['ice_creams']) == sorted(
                                                    customer_order['ice_creams']) and
                                                current_order['base'] == customer_order['base']):
                                            money += 10
                                            coin_sound.play()  # 播放金幣音效
                                            cat_ok_shake_start_time = pygame.time.get_ticks()  # 觸發 cat_ok 晃動
                                            customer_order = generate_customer_order()
                                            base_wait_time = max(8, base_wait_time - 1)
                                            wait_time = base_wait_time
                                            current_wait = wait_time
                                            last_update = pygame.time.get_ticks()
                                            unlock_new_flavor()
                                        else:
                                            show_cat_no = True
                                            cat_no_timer = pygame.time.get_ticks()
                                            wrong_sound.play()  # 播放錯誤音效
                                        current_order = {'topping': None, 'ice_creams': [], 'base': None}
        if paused:
            draw_pause_menu()

        if remaining_seconds == 0:
            screen_stage = 4
            return

        pygame.display.flip()

# 主遊戲迴圈
def main():
    global screen_stage, settings_from_stage, first_start_clicked_time, first_start_clicked

    while True:
        if screen_stage == 0:
            draw_start_screen()  # 畫開始畫面
        elif screen_stage == 1:
            draw_rule_screen()  # 畫規則畫面
        elif screen_stage == 2:
            run_gameplay()  # 跑遊戲主體
        elif screen_stage == 3:
            draw_settings_menu() # 畫設定畫面
        elif screen_stage == 4:
            draw_gameover() # 跑GAMEOVER畫面

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if screen_stage == 0:
                    if next_button.collidepoint(pos):
                        click_sound.play()
                        screen_stage = 1
                    elif settings_0_button.collidepoint(pos):
                        click_sound.play()
                        settings_from_stage = screen_stage
                        screen_stage = 3
                    elif quit_button.collidepoint(pos):
                        quit_game()
                elif screen_stage == 1:
                    if prev_button.collidepoint(pos):
                        click_sound.play()
                        screen_stage = 0
                    elif start_button.collidepoint(pos):
                        click_sound.play()
                        if not first_start_clicked:
                            first_start_clicked_time = pygame.time.get_ticks()
                            first_start_clicked = True
                        screen_stage = 2

        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()