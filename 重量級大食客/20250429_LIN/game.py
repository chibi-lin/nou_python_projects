# ------------------------------
# 套件導入
# ------------------------------
import pygame  # 用於遊戲引擎、圖形渲染與音效播放
import random  # 用於生成隨機顧客訂單
import sys  # 用於系統操作，例如退出程式
from pygame.locals import *  # 導入 Pygame 的事件常數

# ------------------------------
# 初始化 Pygame
# ------------------------------
pygame.init()  # 初始化 Pygame，設置遊戲引擎

# ------------------------------
# 變數定義
# ------------------------------

# 視窗與遊戲設定
WIDTH = 800  # 視窗寬度
HEIGHT = 600  # 視窗高度
FPS = 60  # 每秒幀數，控制遊戲更新速度
CAT_OK_SHAKE_DURATION = 500  # 滿意貓咪晃動效果持續時間 (毫秒)
CAT_NO_TREMBLE_DURATION = 2000  # 不滿貓咪顫抖效果持續時間 (毫秒)
CAT_NO_DURATION = 2000  # 不滿貓咪顯示持續時間 (毫秒)

# 字體設定
FONT = pygame.font.SysFont(None, 36)  # 一般 UI 文字字體，大小 36
LARGE_FONT = pygame.font.SysFont(None, 72)  # 暫停與設定選單標題字體，大小 72
BUTTON_FONT = pygame.font.SysFont(None, 48)  # 按鈕文字字體，大小 48
SMALL_FONT = pygame.font.SysFont(None, 36)  # 滑桿標籤字體，大小 36

# 音量初始值
MUSIC_VOLUME = 0.3  # 初始音樂音量
SOUND_VOLUME = 0.3  # 初始音效音量

# 遊戲變數初始值
money = 0  # 玩家金幣數量
game_over = False  # 遊戲是否結束
paused = False  # 遊戲是否暫停
base_wait_time = 20  # 基礎等待時間 (秒)
wait_time = base_wait_time  # 當前等待時間
current_wait = wait_time  # 當前剩餘等待時間
show_cat_no = False  # 是否顯示不滿貓咪圖片
cat_no_timer = 0  # 不滿貓咪顯示計時器
cat_ok_shake_start_time = None  # 滿意貓咪晃動效果開始時間
gameover_sound_played = False  # 遊戲結束音效是否已播放

# 全局音量變數
music_volume = MUSIC_VOLUME  # 當前音樂音量
sound_volume = SOUND_VOLUME  # 當前音效音量

# 滑桿初始位置與拖動狀態
dragging_music_slider = False  # 標記是否正在拖動音樂滑桿
dragging_sound_slider = False  # 標記是否正在拖動音效滑桿

# 按鈕與滑桿座標
PAUSE_BUTTON_POS = (690, 10)  # 暫停按鈕位置
PAUSE_BUTTON_SIZE = (100, 40)  # 暫停按鈕大小
PAUSE_BUTTON_TEXT_POS = (705, 19)  # 暫停按鈕文字位置

RESUME_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 10)  # 繼續按鈕位置
RESUME_BUTTON_SIZE = (250, 60)  # 繼續按鈕大小
RESUME_BUTTON_TEXT_POS = (WIDTH // 2 - 65, HEIGHT // 2 + 25)  # 繼續按鈕文字位置

SETTINGS_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 90)  # 設定按鈕位置
SETTINGS_BUTTON_SIZE = (250, 60)  # 設定按鈕大小
SETTINGS_BUTTON_TEXT_POS = (WIDTH // 2 - 70, HEIGHT // 2 + 105)  # 設定按鈕文字位置

MAIN_MENU_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 170)  # 返回主畫面按鈕位置
MAIN_MENU_BUTTON_SIZE = (250, 60)  # 返回主畫面按鈕大小
MAIN_MENU_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 185)  # 返回主畫面按鈕文字位置

BACK_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 100)  # 設定選單返回按鈕位置
BACK_BUTTON_SIZE = (250, 60)  # 設定選單返回按鈕大小
BACK_BUTTON_TEXT_POS = (WIDTH // 2 - 40, HEIGHT // 2 + 115)  # 設定選單返回按鈕文字位置

MUSIC_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 - 40)  # 音樂滑桿位置
MUSIC_SLIDER_SIZE = (200, 20)  # 音樂滑桿大小
MUSIC_SLIDER_LABEL_POS = (MUSIC_SLIDER_POS[0] - 180, MUSIC_SLIDER_POS[1] - 5)  # 音樂滑桿標籤位置

SOUND_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 + 10)  # 音效滑桿位置
SOUND_SLIDER_SIZE = (200, 20)  # 音效滑桿大小
SOUND_SLIDER_LABEL_POS = (SOUND_SLIDER_POS[0] - 180, SOUND_SLIDER_POS[1] - 5)  # 音效滑桿標籤位置

PAUSED_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # 暫停選單標題位置
SETTINGS_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # 設定選單標題位置

# 選擇按鈕位置與懸浮狀態
BUTTONS_POS = {
    '開心果': {'pos': (240, 150), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '芒果': {'pos': (325, 150), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '芋頭': {'pos': (410, 150), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '柳橙': {'pos': (495, 150), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '巧克力': {'pos': (580, 150), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '哈密瓜': {'pos': (410, 230), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '草莓': {'pos': (495, 230), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '香草': {'pos': (580, 230), 'size': (100, 100), 'hover': False, 'type': 'ice_cream'},
    '草莓裝飾': {'pos': (410, 310), 'size': (100, 100), 'hover': False, 'type': 'topping'},
    '花生': {'pos': (495, 300), 'size': (100, 100), 'hover': False, 'type': 'topping'},
    '櫻桃': {'pos': (580, 310), 'size': (100, 100), 'hover': False, 'type': 'topping'},
    '甜筒按鈕': {'pos': (440, 410), 'size': (100, 100), 'hover': False, 'type': 'base', 'value': '甜筒'},
    '杯子按鈕': {'pos': (560, 420), 'size': (100, 100), 'hover': False, 'type': 'base', 'value': '杯子'},
    'done': {'pos': (370, 500), 'size': (100, 100), 'hover': False, 'type': 'done'}
}

# 顧客需求圖片顯示位置
CUSTOMER_POSITIONS = {
    'base': {'pos': (75, 330)},  # 杯子/甜筒
    'ice_cream_1': {'pos': (75, 300)},  # 第一層冰淇淋
    'ice_cream_2': {'pos': (75, 270)},  # 第二層冰淇淋
    'ice_cream_3': {'pos': (75, 240)},  # 第三層冰淇淋
    'topping': {'pos': (75, 200)}  # Topping
}

# 當前製作冰淇淋圖片顯示位置
CURRENT_POSITIONS = {
    'base': {'pos': (260, 420)},  # 杯子/甜筒
    'ice_cream_1': {'pos': (260, 390)},  # 第一層冰淇淋
    'ice_cream_2': {'pos': (260, 360)},  # 第二層冰淇淋
    'ice_cream_3': {'pos': (260, 330)},  # 第三層冰淇淋
    'topping': {'pos': (260, 290)}  # Topping
}

# UI 元素位置
COIN_POS = (20, 0)  # 金幣圖標
MONEY_TEXT_POS = (100, 35)  # 金幣數量文字
CLOCK_POS = (330, 0)  # 時鐘圖標
TIMER_TEXT_POS = (410, 35)  # 計時器文字
GAME_OVER_POS = (WIDTH // 2 - 200, HEIGHT // 2 - 100)  # 遊戲結束圖片
WRONG_TEXT_POS = (CURRENT_POSITIONS['ice_cream_1']['pos'][0] - 20, CURRENT_POSITIONS['base']['pos'][1] + 50)  # 錯誤提示文字

# 遊戲變數
customer_order = None  # 顧客訂單
current_order = {'topping': None, 'ice_creams': [], 'base': None}  # 當前製作的冰淇淋訂單
last_update = pygame.time.get_ticks()  # 上次更新時間，用於計時

# 滑桿初始位置
music_slider_pos = MUSIC_SLIDER_POS[0] + (music_volume * MUSIC_SLIDER_SIZE[0])  # 音樂滑桿初始位置
sound_slider_pos = SOUND_SLIDER_POS[0] + (sound_volume * SOUND_SLIDER_SIZE[0])  # 音效滑桿初始位置

# 設定遊戲視窗與基本元件
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 設定視窗大小
pygame.display.set_caption("Heavy Eater")  # 設定視窗標題
clock = pygame.time.Clock()  # 用於控制遊戲幀率，確保平滑運行

# 初始化音效模組
pygame.mixer.init()  # 初始化 Pygame 音效模組

# 載入遊戲音效
customer_sound = pygame.mixer.Sound("sound/customer_appears.mp3")  # 顧客出現音效
ice_cream_sound = pygame.mixer.Sound("sound/ice_cream.mp3")  # 選擇冰淇淋音效
wrong_sound = pygame.mixer.Sound("sound/wrong.mp3")  # 錯誤音效
coin_sound = pygame.mixer.Sound("sound/coin.mp3")  # 獲得金幣音效
click_sound = pygame.mixer.Sound("sound/click.mp3")  # 按鈕點擊音效
bye_bye_sound = pygame.mixer.Sound("sound/bye_bye.mp3")  # 退出遊戲音效
gameover_sound = pygame.mixer.Sound("sound/gameover.mp3")  # 遊戲結束音效

# 定義按鈕與滑桿區域
buttons = {
    item: {
        'rect': pygame.Rect(*data['pos'], *data['size']),
        'hover': data['hover'],
        'type': data['type'],
        'value': data.get('value')
    } for item, data in BUTTONS_POS.items()
}

pause_button = pygame.Rect(*PAUSE_BUTTON_POS, *PAUSE_BUTTON_SIZE)  # 暫停按鈕區域
resume_button = pygame.Rect(*RESUME_BUTTON_POS, *RESUME_BUTTON_SIZE)  # 繼續按鈕區域
settings_button = pygame.Rect(*SETTINGS_BUTTON_POS, *SETTINGS_BUTTON_SIZE)  # 設定按鈕區域
main_menu_button = pygame.Rect(*MAIN_MENU_BUTTON_POS, *MAIN_MENU_BUTTON_SIZE)  # 返回主畫面按鈕區域
back_button = pygame.Rect(*BACK_BUTTON_POS, *BACK_BUTTON_SIZE)  # 設定選單返回按鈕區域
music_slider_rect = pygame.Rect(*MUSIC_SLIDER_POS, *MUSIC_SLIDER_SIZE)  # 音樂音量滑桿區域
sound_slider_rect = pygame.Rect(*SOUND_SLIDER_POS, *SOUND_SLIDER_SIZE)  # 音效音量滑桿區域

# ------------------------------
# 前端 - 圖形與資源處理
# ------------------------------

# 檢查圖片表面是否有效，確保圖片正確載入
def check_surface(surface, name):
    if surface.get_width() == 0 or surface.get_height() == 0:
        print(f"Image {name} failed to load: Invalid surface")
        sys.exit()
    expected_width, expected_height = WIDTH, HEIGHT
    if name in ['background', 'cat_ok', 'cat_no', 'counter'] and (surface.get_width() != expected_width or surface.get_height() != expected_height):
        print(f"Warning: Image (name size is {surface.get_width()}x{surface.get_height()}, expected {expected_width}x{expected_height}")
    return surface

# 載入遊戲基礎圖片資源
try:
    coin_img = check_surface(pygame.image.load('assest/coin.png').convert_alpha(), 'coin')  # 金幣圖片
    clock_img = check_surface(pygame.image.load('assest/clock.png').convert_alpha(), 'clock')  # 時鐘圖片
    game_over_img = check_surface(pygame.image.load('assest/GAMEOVER.svg').convert_alpha(), 'game_over')  # 遊戲結束圖片
    background_img = check_surface(pygame.image.load('assest/background_1.png').convert(), 'background')  # 遊戲背景圖片
    cat_ok_img = check_surface(pygame.image.load('assest/cat_ok.png').convert_alpha(), 'cat_ok')  # 滿意貓咪圖片
    cat_no_img = check_surface(pygame.image.load('assest/cat_no.png').convert_alpha(), 'cat_no')  # 不滿貓咪圖片
    counter_img = check_surface(pygame.image.load('assest/counter.png').convert_alpha(), 'counter')  # 櫃檯圖片
except FileNotFoundError as e:
    print(f"Failed to load image: {e}")
    sys.exit()

# 載入冰淇淋、杯子/甜筒與 Topping 圖片
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
    print(f"Failed to load image: {e}")
    sys.exit()

# 繪製文字的函數，用於顯示 UI 文字
def draw_text(text, pos, font=FONT, color=(0, 0, 0)):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# 繪製滑桿的函數，用於設定選單的音量調整
def draw_slider(rect, pos, label, label_pos, font=SMALL_FONT):
    pygame.draw.rect(screen, (150, 150, 150), rect, border_radius=5)  # 繪製滑桿背景
    pygame.draw.circle(screen, (50, 100, 150), (int(pos), rect.centery), 10)  # 繪製滑桿圓形指示器
    draw_text(label, label_pos, font, (255, 255, 255))  # 繪製滑桿標籤

# 繪製顧客訂單，顯示顧客需求的冰淇淋
def draw_customer_order(order, shake=False):
    if not order:
        return

    shake_offset = (random.randint(-2, 2), random.randint(-2, 2)) if shake else (0, 0)  # 抖動效果

    base_img = items_img[order['base']]
    base_pos = CUSTOMER_POSITIONS['base']['pos']
    if order['base'] == '甜筒':
        base_pos = (75, 340)  # 甜筒位置微調
    screen.blit(base_img, (base_pos[0] + shake_offset[0], base_pos[1] + shake_offset[1]))

    for i, flavor in enumerate(order['ice_creams']):
        scoop_img = items_img[flavor]
        if i == 0:
            pos = CUSTOMER_POSITIONS['ice_cream_1']['pos']
        elif i == 1:
            pos = CUSTOMER_POSITIONS['ice_cream_2']['pos']
        else:
            pos = CUSTOMER_POSITIONS['ice_cream_3']['pos']
        screen.blit(scoop_img, (pos[0] + shake_offset[0], pos[1] + shake_offset[1]))

    topping_img = items_img[order['topping']]
    topping_pos = CUSTOMER_POSITIONS['topping']['pos']
    num_ice_creams = len(order['ice_creams'])
    if num_ice_creams == 3:
        topping_pos = CUSTOMER_POSITIONS['topping']['pos']
    elif num_ice_creams == 2:
        topping_pos = CUSTOMER_POSITIONS['ice_cream_3']['pos']
    else:
        topping_pos = CUSTOMER_POSITIONS['ice_cream_2']['pos']
    screen.blit(topping_img, (topping_pos[0] + shake_offset[0], topping_pos[1] + shake_offset[1]))

# 繪製選擇按鈕，包含冰淇淋、Topping 和杯子/甜筒
def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    for item, data in buttons.items():
        rect = data['rect']
        data['hover'] = rect.collidepoint(mouse_pos)  # 檢查滑鼠是否懸浮在按鈕上
        offset = -5 if data['hover'] else 0  # 懸浮時向上偏移
        screen.blit(items_img[item], (rect.x + 15, rect.y + offset))

# 繪製當前製作的冰淇淋，顯示玩家選擇的冰淇淋
def draw_current_order():
    if current_order['base']:
        base_img = items_img[current_order['base']]
        base_pos = CURRENT_POSITIONS['base']['pos']
        if current_order['base'] == '甜筒':
            base_pos = (260, 430)  # 甜筒位置微調
        screen.blit(base_img, base_pos)

    for i, flavor in enumerate(current_order['ice_creams']):
        scoop_img = items_img[flavor]
        if i == 0:
            pos = CURRENT_POSITIONS['ice_cream_1']['pos']
        elif i == 1:
            pos = CURRENT_POSITIONS['ice_cream_2']['pos']
        else:
            pos = CURRENT_POSITIONS['ice_cream_3']['pos']
        screen.blit(scoop_img, pos)

    if current_order['topping']:
        topping_img = items_img[current_order['topping']]
        topping_pos = CURRENT_POSITIONS['topping']['pos']
        num_ice_creams = len(current_order['ice_creams'])
        if num_ice_creams == 3:
            topping_pos = CURRENT_POSITIONS['topping']['pos']
        elif num_ice_creams == 2:
            topping_pos = CURRENT_POSITIONS['ice_cream_3']['pos']
        else:
            topping_pos = CURRENT_POSITIONS['ice_cream_2']['pos']
        screen.blit(topping_img, topping_pos)

# 繪製櫃檯圖片，作為遊戲前景
def draw_counter():
    screen.blit(counter_img, (0, 0))

# 繪製貓咪圖片，根據訂單正確與否顯示滿意或不滿，並加入晃動效果
def draw_cat_images():
    cat_img = cat_no_img if show_cat_no else cat_ok_img
    current_time = pygame.time.get_ticks()
    
    if not show_cat_no and cat_ok_shake_start_time and (current_time - cat_ok_shake_start_time <= CAT_OK_SHAKE_DURATION):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(cat_img, (offset_x, offset_y))  # 滿意貓咪晃動效果
    elif show_cat_no and (current_time - cat_no_timer <= CAT_NO_TREMBLE_DURATION):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        screen.blit(cat_img, (offset_x, offset_y))  # 不滿貓咪顫抖效果
    else:
        screen.blit(cat_img, (0, 0))  # 正常顯示貓咪圖片

# 繪製 UI 元素，包含金幣、時鐘與暫停按鈕
def draw_ui_decorations():
    screen.blit(coin_img, COIN_POS)  # 顯示金幣圖標
    draw_text(f'{money}', MONEY_TEXT_POS, color=(0, 0, 0))  # 顯示金幣數量
    screen.blit(clock_img, CLOCK_POS)  # 顯示時鐘圖標
    draw_text(f'{int(current_wait)}', TIMER_TEXT_POS, color=(0, 0, 0))  # 顯示剩餘時間
    pygame.draw.rect(screen, (100, 100, 100), pause_button, border_radius=10)  # 繪製暫停按鈕
    draw_text("Pause", PAUSE_BUTTON_TEXT_POS)  # 繪製暫停按鈕文字

# 繪製暫停選單，包含繼續、設定與返回主畫面按鈕
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # 創建半透明遮罩
    overlay.fill((0, 0, 0, 180))  # 設置遮罩顏色與透明度
    screen.blit(overlay, (0, 0))  # 顯示遮罩
    
    draw_text("Paused", PAUSED_TITLE_POS, LARGE_FONT, (255, 255, 255))  # 顯示標題
    
    mouse_pos = pygame.mouse.get_pos()
    resume_color = (100, 150, 200) if resume_button.collidepoint(mouse_pos) else (50, 100, 150)
    settings_color = (100, 150, 200) if settings_button.collidepoint(mouse_pos) else (50, 100, 150)
    main_menu_color = (100, 150, 200) if main_menu_button.collidepoint(mouse_pos) else (50, 100, 150)
    
    pygame.draw.rect(screen, resume_color, resume_button, border_radius=15)  # 繪製繼續按鈕
    draw_text("Resume", RESUME_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))
    pygame.draw.rect(screen, settings_color, settings_button, border_radius=15)  # 繪製設定按鈕
    draw_text("Settings", SETTINGS_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))
    pygame.draw.rect(screen, main_menu_color, main_menu_button, border_radius=15)  # 繪製返回主畫面按鈕
    draw_text("Main Menu", MAIN_MENU_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))

# 繪製設定選單，包含音量滑桿與返回按鈕
def draw_settings_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # 創建半透明遮罩
    overlay.fill((0, 0, 0, 180))  # 設置遮罩顏色與透明度
    screen.blit(overlay, (0, 0))  # 顯示遮罩
    
    draw_text("Settings", SETTINGS_TITLE_POS, LARGE_FONT, (255, 255, 255))  # 顯示標題
    
    draw_slider(music_slider_rect, music_slider_pos, "Music Volume", MUSIC_SLIDER_LABEL_POS)  # 繪製音樂音量滑桿
    draw_slider(sound_slider_rect, sound_slider_pos, "Sound Volume", SOUND_SLIDER_LABEL_POS)  # 繪製音效音量滑桿
    
    mouse_pos = pygame.mouse.get_pos()
    back_color = (100, 150, 200) if back_button.collidepoint(mouse_pos) else (50, 100, 150)
    pygame.draw.rect(screen, back_color, back_button, border_radius=15)  # 繪製返回按鈕
    draw_text("Back", BACK_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))

# ------------------------------
# 後端 - 邏輯處理
# ------------------------------

# 生成新的顧客訂單，隨機選擇冰淇淋、Topping 和杯子/甜筒
def generate_customer_order():
    ice_cream_flavors = ['巧克力', '芒果', '哈密瓜', '柳橙', '開心果', '草莓', '芋頭', '香草']
    toppings = ['花生', '草莓裝飾', '櫻桃']
    bases = ['杯子', '甜筒']
    
    order = {
        'topping': random.choice(toppings),
        'ice_creams': random.sample(ice_cream_flavors, random.randint(1, 3)),
        'base': random.choice(bases)
    }
    customer_sound.play()  # 播放顧客出現音效
    return order

# 主遊戲迴圈，處理遊戲邏輯與畫面更新
def main(initial_music_volume, initial_sound_volume):
    global money, game_over, current_order, paused, customer_order, wait_time, current_wait, last_update, base_wait_time
    global show_cat_no, cat_no_timer, cat_ok_shake_start_time, gameover_sound_played
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos, dragging_music_slider, dragging_sound_slider

    # 初始化音量，從主畫面傳入
    music_volume = initial_music_volume
    sound_volume = initial_sound_volume
    music_slider_pos = MUSIC_SLIDER_POS[0] + (music_volume * MUSIC_SLIDER_SIZE[0])
    sound_slider_pos = SOUND_SLIDER_POS[0] + (sound_volume * SOUND_SLIDER_SIZE[0])
    pygame.mixer.music.set_volume(music_volume)
    for sound in [customer_sound, ice_cream_sound, wrong_sound, coin_sound, click_sound, bye_bye_sound, gameover_sound]:
        sound.set_volume(sound_volume)

    # 重置遊戲變數
    customer_order = None
    money = 0
    game_over = False
    paused = False
    in_settings = False
    current_order = {'topping': None, 'ice_creams': [], 'base': None}
    base_wait_time = 20
    wait_time = base_wait_time
    current_wait = wait_time
    last_update = pygame.time.get_ticks()
    show_cat_no = False
    cat_no_timer = 0
    cat_ok_shake_start_time = None
    gameover_sound_played = False

    if customer_order is None:
        customer_order = generate_customer_order()  # 生成初始顧客訂單

    while True:
        if show_cat_no:  # 處理不滿貓咪顯示邏輯
            current_time = pygame.time.get_ticks()
            if current_time - cat_no_timer >= CAT_NO_DURATION:
                show_cat_no = False
                customer_order = generate_customer_order()
                current_order = {'topping': None, 'ice_creams': [], 'base': None}
                wait_time = base_wait_time
                current_wait = wait_time
                last_update = pygame.time.get_ticks()
        else:
            if not paused:  # 處理計時器邏輯
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

        screen.blit(background_img, (0, 0))  # 繪製背景

        if not paused:  # 繪製遊戲畫面
            draw_cat_images()
            draw_counter()
            shake = current_wait <= 5
            draw_customer_order(customer_order, shake)
            draw_buttons()
            draw_current_order()
            draw_ui_decorations()

        for event in pygame.event.get():
            if event.type == QUIT:  # 處理視窗關閉事件
                return
            elif event.type == MOUSEBUTTONDOWN:  # 處理滑鼠按下事件
                pos = pygame.mouse.get_pos()
                if paused:
                    if in_settings:
                        music_slider_circle = pygame.Rect(music_slider_pos - 10, music_slider_rect.y - 10, 20, 20)
                        sound_slider_circle = pygame.Rect(sound_slider_pos - 10, sound_slider_rect.y - 10, 20, 20)
                        if music_slider_circle.collidepoint(pos):
                            dragging_music_slider = True
                        elif sound_slider_circle.collidepoint(pos):
                            dragging_sound_slider = True
                        elif back_button.collidepoint(pos):
                            click_sound.play()
                            in_settings = False
                    else:
                        if resume_button.collidepoint(pos):
                            click_sound.play()
                            paused = False
                        elif settings_button.collidepoint(pos):
                            click_sound.play()
                            in_settings = True
                        elif main_menu_button.collidepoint(pos):
                            click_sound.play()
                            return
                else:
                    if pause_button.collidepoint(pos):  # 點擊暫停按鈕
                        click_sound.play()
                        paused = True
                    elif not game_over:
                        for item, data in buttons.items():
                            if data['rect'].collidepoint(pos):
                                if data['type'] == 'ice_cream' and len(current_order['ice_creams']) < 3:
                                    ice_cream_sound.play()
                                    current_order['ice_creams'].append(item)
                                elif data['type'] == 'base' and not current_order['base']:
                                    ice_cream_sound.play()
                                    current_order['base'] = data['value']
                                elif data['type'] == 'topping' and not current_order['topping']:
                                    ice_cream_sound.play()
                                    current_order['topping'] = item
                                elif data['type'] == 'done':
                                    if (current_order['topping'] and current_order['ice_creams'] and current_order['base']):
                                        if (current_order['topping'] == customer_order['topping'] and
                                            sorted(current_order['ice_creams']) == sorted(customer_order['ice_creams']) and
                                            current_order['base'] == customer_order['base']):
                                            money += 10
                                            coin_sound.play()
                                            cat_ok_shake_start_time = pygame.time.get_ticks()
                                            customer_order = generate_customer_order()
                                            base_wait_time = max(8, base_wait_time - 1)
                                            wait_time = base_wait_time
                                            current_wait = wait_time
                                            last_update = pygame.time.get_ticks()
                                        else:
                                            show_cat_no = True
                                            cat_no_timer = pygame.time.get_ticks()
                                            wrong_sound.play()
                                            draw_text("Wrong! Try Again", WRONG_TEXT_POS, color=(255, 0, 0))
                                            pygame.display.flip()
                                        current_order = {'topping': None, 'ice_creams': [], 'base': None}
            elif event.type == MOUSEBUTTONUP:  # 處理滑鼠放開事件
                dragging_music_slider = False
                dragging_sound_slider = False
            elif event.type == MOUSEMOTION and paused and in_settings:  # 處理滑鼠移動事件
                if dragging_music_slider:
                    new_pos = event.pos[0]
                    new_pos = max(music_slider_rect.x, min(new_pos, music_slider_rect.x + music_slider_rect.width))
                    music_slider_pos = new_pos
                    music_volume = (music_slider_pos - music_slider_rect.x) / music_slider_rect.width
                    pygame.mixer.music.set_volume(music_volume)
                elif dragging_sound_slider:
                    new_pos = event.pos[0]
                    new_pos = max(sound_slider_rect.x, min(new_pos, sound_slider_rect.x + music_slider_rect.width))
                    sound_slider_pos = new_pos
                    sound_volume = (sound_slider_pos - sound_slider_rect.x) / sound_slider_rect.width
                    for sound in [customer_sound, ice_cream_sound, wrong_sound, coin_sound, click_sound, bye_bye_sound, gameover_sound]:
                        sound.set_volume(sound_volume)

        if paused:
            if in_settings:
                draw_settings_menu()
            else:
                draw_pause_menu()

        if game_over:
            screen.blit(game_over_img, GAME_OVER_POS)
            if not gameover_sound_played:
                gameover_sound.play()
                gameover_sound_played = True

        pygame.display.flip()  # 更新畫面
        clock.tick(FPS)  # 控制幀率