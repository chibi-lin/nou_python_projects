import pygame
import random
import sys
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 定義所有變數
# 視窗與遊戲設定
WIDTH = 800
HEIGHT = 600
FPS = 60
CAT_OK_SHAKE_DURATION = 500
CAT_NO_TREMBLE_DURATION = 2000
CAT_NO_DURATION = 2000

# 字體設定
FONT = pygame.font.SysFont(None, 36)
LARGE_FONT = pygame.font.SysFont(None, 72)
BUTTON_FONT = pygame.font.SysFont(None, 48)
SMALL_FONT = pygame.font.SysFont(None, 36)

# 音量初始值
MUSIC_VOLUME = 0.3
SOUND_VOLUME = 0.3

# 遊戲變數初始值
money = 0
game_over = False
paused = False
base_wait_time = 20
wait_time = base_wait_time
current_wait = wait_time
show_cat_no = False
cat_no_timer = 0
cat_ok_shake_start_time = None
gameover_sound_played = False

# 全局音量變數
music_volume = MUSIC_VOLUME
sound_volume = SOUND_VOLUME

# 滑桿初始位置
dragging_music_slider = False
dragging_sound_slider = False

# 按鈕與滑桿座標 (x, y) 格式
PAUSE_BUTTON_POS = (690, 10)  # (690, 10)
PAUSE_BUTTON_SIZE = (100, 40)
PAUSE_BUTTON_TEXT_POS = (705, 19)  # (705, 20)

RESUME_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 10)  # (275, 310)
RESUME_BUTTON_SIZE = (250, 60)
RESUME_BUTTON_TEXT_POS = (WIDTH // 2 - 65, HEIGHT // 2 + 25)  # (340, 320)

SETTINGS_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 90)  # (275, 390)
SETTINGS_BUTTON_SIZE = (250, 60)
SETTINGS_BUTTON_TEXT_POS = (WIDTH // 2 - 70, HEIGHT // 2 + 105)  # (340, 400)

MAIN_MENU_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 170)  # (275, 470)
MAIN_MENU_BUTTON_SIZE = (250, 60)
MAIN_MENU_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 185)  # (340, 480)

BACK_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 100)  # (275, 400)
BACK_BUTTON_SIZE = (250, 60)
BACK_BUTTON_TEXT_POS = (WIDTH // 2 - 40, HEIGHT // 2 + 115)  # (340, 410)

MUSIC_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 - 40)  # (300, 280)
MUSIC_SLIDER_SIZE = (200, 20)
MUSIC_SLIDER_LABEL_POS = (MUSIC_SLIDER_POS[0] - 180, MUSIC_SLIDER_POS[1] - 5)  # (120, 275)

SOUND_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 + 10)  # (300, 320)
SOUND_SLIDER_SIZE = (200, 20)
SOUND_SLIDER_LABEL_POS = (SOUND_SLIDER_POS[0] - 180, SOUND_SLIDER_POS[1] - 5)  # (120, 315)

PAUSED_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # (320, 50)
SETTINGS_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # (320, 50)

# 按鈕位置與懸浮狀態
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

# 顧客需求與當前製作位置
CUSTOMER_POSITIONS = {
    'base': {'pos': (75, 330)},
    'ice_cream_1': {'pos': (75, 300)},
    'ice_cream_2': {'pos': (75, 270)},
    'ice_cream_3': {'pos': (75, 240)},
    'topping': {'pos': (75, 200)}
}

CURRENT_POSITIONS = {
    'base': {'pos': (260, 420)},
    'ice_cream_1': {'pos': (260, 390)},
    'ice_cream_2': {'pos': (260, 360)},
    'ice_cream_3': {'pos': (260, 330)},
    'topping': {'pos': (260, 290)}
}

# UI 元素位置
COIN_POS = (20, 0)  # (20, 0)
MONEY_TEXT_POS = (100, 35)  # (100, 35)
CLOCK_POS = (330, 0)  # (330, 0)
TIMER_TEXT_POS = (410, 35)  # (410, 35)
GAME_OVER_POS = (WIDTH // 2 - 200, HEIGHT // 2 - 100)  # (200, 200)
WRONG_TEXT_POS = (CURRENT_POSITIONS['ice_cream_1']['pos'][0] - 20, CURRENT_POSITIONS['base']['pos'][1] + 50)  # (240, 470)

# 設定遊戲視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heavy Eater")
clock = pygame.time.Clock()

# 初始化音效模組
pygame.mixer.init()

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
        print(f"Image {name} failed to load: Invalid surface")
        sys.exit()
    expected_width, expected_height = WIDTH, HEIGHT
    if name in ['background', 'cat_ok', 'cat_no', 'counter'] and (surface.get_width() != expected_width or surface.get_height() != expected_height):
        print(f"Warning: Image {name} size is {surface.get_width()}x{surface.get_height()}, expected {expected_width}x{expected_height}")
    return surface

# 載入圖片資源
try:
    coin_img = check_surface(pygame.image.load('assest/coin.png').convert_alpha(), 'coin')
    clock_img = check_surface(pygame.image.load('assest/clock.png').convert_alpha(), 'clock')
    game_over_img = check_surface(pygame.image.load('assest/GAMEOVER.svg').convert_alpha(), 'game_over')
    background_img = check_surface(pygame.image.load('assest/background_1.png').convert(), 'background')
    cat_ok_img = check_surface(pygame.image.load('assest/cat_ok.png').convert_alpha(), 'cat_ok')
    cat_no_img = check_surface(pygame.image.load('assest/cat_no.png').convert_alpha(), 'cat_no')
    counter_img = check_surface(pygame.image.load('assest/counter.png').convert_alpha(), 'counter')
except FileNotFoundError as e:
    print(f"Failed to load image: {e}")
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
    print(f"Failed to load image: {e}")
    sys.exit()

# 遊戲變數
customer_order = None
current_order = {'topping': None, 'ice_creams': [], 'base': None}
last_update = pygame.time.get_ticks()

# 滑桿初始位置
music_slider_pos = MUSIC_SLIDER_POS[0] + (music_volume * MUSIC_SLIDER_SIZE[0])
sound_slider_pos = SOUND_SLIDER_POS[0] + (sound_volume * SOUND_SLIDER_SIZE[0])

# 定義按鈕與滑桿區域
buttons = {
    item: {
        'rect': pygame.Rect(*data['pos'], *data['size']),
        'hover': data['hover'],
        'type': data['type'],
        'value': data.get('value')
    } for item, data in BUTTONS_POS.items()
}

pause_button = pygame.Rect(*PAUSE_BUTTON_POS, *PAUSE_BUTTON_SIZE)
resume_button = pygame.Rect(*RESUME_BUTTON_POS, *RESUME_BUTTON_SIZE)
settings_button = pygame.Rect(*SETTINGS_BUTTON_POS, *SETTINGS_BUTTON_SIZE)
main_menu_button = pygame.Rect(*MAIN_MENU_BUTTON_POS, *MAIN_MENU_BUTTON_SIZE)
back_button = pygame.Rect(*BACK_BUTTON_POS, *BACK_BUTTON_SIZE)

music_slider_rect = pygame.Rect(*MUSIC_SLIDER_POS, *MUSIC_SLIDER_SIZE)
sound_slider_rect = pygame.Rect(*SOUND_SLIDER_POS, *SOUND_SLIDER_SIZE)

# 繪製文字的函數
def draw_text(text, pos, font=FONT, color=(0, 0, 0)):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# 繪製滑桿
def draw_slider(rect, pos, label, label_pos, font=SMALL_FONT):
    pygame.draw.rect(screen, (150, 150, 150), rect, border_radius=5)
    pygame.draw.circle(screen, (50, 100, 150), (int(pos), rect.centery), 10)
    draw_text(label, label_pos, font, (255, 255, 255))

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
    customer_sound.play()
    return order

# 繪製顧客需求
def draw_customer_order(order, shake=False):
    if not order:
        return

    shake_offset = (random.randint(-2, 2), random.randint(-2, 2)) if shake else (0, 0)

    base_img = items_img[order['base']]
    base_pos = CUSTOMER_POSITIONS['base']['pos']
    if order['base'] == '甜筒':
        base_pos = (75, 340)
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
        base_pos = CURRENT_POSITIONS['base']['pos']
        if current_order['base'] == '甜筒':
            base_pos = (260, 430)
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

# 繪製 counter 圖片
def draw_counter():
    screen.blit(counter_img, (0, 0))

# 繪製 cat_ok/cat_no 圖片，並加入晃動與顫抖效果
def draw_cat_images():
    cat_img = cat_no_img if show_cat_no else cat_ok_img
    current_time = pygame.time.get_ticks()
    
    if not show_cat_no and cat_ok_shake_start_time and (current_time - cat_ok_shake_start_time <= CAT_OK_SHAKE_DURATION):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(cat_img, (offset_x, offset_y))
    elif show_cat_no and (current_time - cat_no_timer <= CAT_NO_TREMBLE_DURATION):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        screen.blit(cat_img, (offset_x, offset_y))
    else:
        screen.blit(cat_img, (0, 0))

# 繪製 UI 元素（clock, coin, setting）
def draw_ui_decorations():
    screen.blit(coin_img, COIN_POS)
    draw_text(f'{money}', MONEY_TEXT_POS, color=(0, 0, 0))
    screen.blit(clock_img, CLOCK_POS)
    draw_text(f'{int(current_wait)}', TIMER_TEXT_POS, color=(0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), pause_button, border_radius=10)
    draw_text("Pause", PAUSE_BUTTON_TEXT_POS)

# 繪製暫停選單
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("Paused", PAUSED_TITLE_POS, LARGE_FONT, (255, 255, 255))
    
    mouse_pos = pygame.mouse.get_pos()
    resume_color = (100, 150, 200) if resume_button.collidepoint(mouse_pos) else (50, 100, 150)
    settings_color = (100, 150, 200) if settings_button.collidepoint(mouse_pos) else (50, 100, 150)
    main_menu_color = (100, 150, 200) if main_menu_button.collidepoint(mouse_pos) else (50, 100, 150)
    
    pygame.draw.rect(screen, resume_color, resume_button, border_radius=15)
    draw_text("Resume", RESUME_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))
    pygame.draw.rect(screen, settings_color, settings_button, border_radius=15)
    draw_text("Settings", SETTINGS_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))
    pygame.draw.rect(screen, main_menu_color, main_menu_button, border_radius=15)
    draw_text("Main Menu", MAIN_MENU_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))

# 繪製設定選單
def draw_settings_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("Settings", SETTINGS_TITLE_POS, LARGE_FONT, (255, 255, 255))
    
    draw_slider(music_slider_rect, music_slider_pos, "Music Volume", MUSIC_SLIDER_LABEL_POS)
    draw_slider(sound_slider_rect, sound_slider_pos, "Sound Volume", SOUND_SLIDER_LABEL_POS)
    
    mouse_pos = pygame.mouse.get_pos()
    back_color = (100, 150, 200) if back_button.collidepoint(mouse_pos) else (50, 100, 150)
    pygame.draw.rect(screen, back_color, back_button, border_radius=15)
    draw_text("Back", BACK_BUTTON_TEXT_POS, BUTTON_FONT, (255, 255, 255))

# 主遊戲迴圈
def main(initial_music_volume, initial_sound_volume):
    global money, game_over, current_order, paused, customer_order, wait_time, current_wait, last_update, base_wait_time
    global show_cat_no, cat_no_timer, cat_ok_shake_start_time, gameover_sound_played
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos, dragging_music_slider, dragging_sound_slider

    # 初始化音量
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
        customer_order = generate_customer_order()

    while True:
        if show_cat_no:
            current_time = pygame.time.get_ticks()
            if current_time - cat_no_timer >= CAT_NO_DURATION:
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
            draw_cat_images()
            draw_counter()
            shake = current_wait <= 5
            draw_customer_order(customer_order, shake)
            draw_buttons()
            draw_current_order()
            draw_ui_decorations()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
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
                    if pause_button.collidepoint(pos):
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
            elif event.type == MOUSEBUTTONUP:
                dragging_music_slider = False
                dragging_sound_slider = False
            elif event.type == MOUSEMOTION and paused and in_settings:
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

        pygame.display.flip()
        clock.tick(FPS)