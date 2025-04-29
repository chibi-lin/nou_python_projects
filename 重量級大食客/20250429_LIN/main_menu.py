# ------------------------------
# 套件導入
# ------------------------------
import pygame  # 用於遊戲引擎、圖形渲染與音效播放
import sys  # 用於系統操作，例如退出程式
from pygame.locals import *  # 導入 Pygame 的事件常數
import game  # 導入遊戲模組以進入遊戲主畫面

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

# 字體設定
FONT = pygame.font.SysFont(None, 48)  # 按鈕文字字體，大小 48
LARGE_FONT = pygame.font.SysFont(None, 72)  # 設定選單標題字體，大小 72
SMALL_FONT = pygame.font.SysFont(None, 36)  # 滑桿標籤字體，大小 36

# 音量初始值
MUSIC_VOLUME = 0.3  # 初始背景音樂音量
SOUND_VOLUME = 0.3  # 初始音效音量

# 按鈕與滑桿座標
START_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 10)  # "Start Game" 按鈕位置
START_BUTTON_SIZE = (250, 60)  # "Start Game" 按鈕大小
START_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 25)  # "Start Game" 文字位置

SETTINGS_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 90)  # "Settings" 按鈕位置
SETTINGS_BUTTON_SIZE = (250, 60)  # "Settings" 按鈕大小
SETTINGS_BUTTON_TEXT_POS = (WIDTH // 2 - 70, HEIGHT // 2 + 105)  # "Settings" 文字位置

EXIT_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 170)  # "Exit Game" 按鈕位置
EXIT_BUTTON_SIZE = (250, 60)  # "Exit Game" 按鈕大小
EXIT_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 185)  # "Exit Game" 文字位置

MAIN_MENU_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 100)  # "Main Menu" 按鈕位置
MAIN_MENU_BUTTON_SIZE = (250, 60)  # "Main Menu" 按鈕大小
MAIN_MENU_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 115)  # "Main Menu" 文字位置

MUSIC_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 - 40)  # 音樂滑桿位置
MUSIC_SLIDER_SIZE = (200, 20)  # 音樂滑桿大小
MUSIC_SLIDER_LABEL_POS = (MUSIC_SLIDER_POS[0] - 180, MUSIC_SLIDER_POS[1] - 5)  # 音樂滑桿標籤位置

SOUND_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 + 10)  # 音效滑桿位置
SOUND_SLIDER_SIZE = (200, 20)  # 音效滑桿大小
SOUND_SLIDER_LABEL_POS = (SOUND_SLIDER_POS[0] - 180, SOUND_SLIDER_POS[1] - 5)  # 音效滑桿標籤位置

SETTINGS_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # 設定選單標題位置

# 全局音量變數
music_volume = MUSIC_VOLUME  # 當前背景音樂音量
sound_volume = SOUND_VOLUME  # 當前音效音量

# 滑桿初始位置與拖動狀態
music_slider_pos = MUSIC_SLIDER_POS[0] + (music_volume * MUSIC_SLIDER_SIZE[0])  # 音樂滑桿初始位置
sound_slider_pos = SOUND_SLIDER_POS[0] + (sound_volume * SOUND_SLIDER_SIZE[0])  # 音效滑桿初始位置
dragging_music_slider = False  # 標記是否正在拖動音樂滑桿
dragging_sound_slider = False  # 標記是否正在拖動音效滑桿

# 設定遊戲視窗與基本元件
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 設定視窗大小
pygame.display.set_caption("Heavy Eater - Main Menu")  # 設定視窗標題
clock = pygame.time.Clock()  # 用於控制遊戲幀率，確保平滑運行

# 初始化音效模組
pygame.mixer.init()  # 初始化 Pygame 音效模組

# 載入並播放背景音樂
pygame.mixer.music.load('sound/bgm.mp3')  # 載入背景音樂檔案
pygame.mixer.music.set_volume(MUSIC_VOLUME)  # 設定初始音樂音量
pygame.mixer.music.play(-1)  # 無限循環播放背景音樂

# 載入按鈕音效
click_sound = pygame.mixer.Sound("sound/click.mp3")  # 按鈕點擊音效
bye_bye_sound = pygame.mixer.Sound("sound/bye_bye.mp3")  # 退出遊戲音效
click_sound.set_volume(SOUND_VOLUME)  # 設定初始音效音量
bye_bye_sound.set_volume(SOUND_VOLUME)  # 設定初始音效音量

# 定義按鈕與滑桿區域
start_button = pygame.Rect(*START_BUTTON_POS, *START_BUTTON_SIZE)  # "Start Game" 按鈕區域
settings_button = pygame.Rect(*SETTINGS_BUTTON_POS, *SETTINGS_BUTTON_SIZE)  # "Settings" 按鈕區域
exit_button = pygame.Rect(*EXIT_BUTTON_POS, *EXIT_BUTTON_SIZE)  # "Exit Game" 按鈕區域
main_menu_button = pygame.Rect(*MAIN_MENU_BUTTON_POS, *MAIN_MENU_BUTTON_SIZE)  # "Main Menu" 按鈕區域
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
    if name in ['loading'] and (surface.get_width() != expected_width or surface.get_height() != expected_height):
        print(f"Warning: Image {name} size is {surface.get_width()}x{surface.get_height()}, expected {expected_width}x{expected_height}")
    return surface

# 載入主畫面背景圖片
try:
    loading_img = check_surface(pygame.image.load('assest/loading.png').convert_alpha(), 'loading')
except FileNotFoundError as e:
    print(f"Failed to load image: {e}")
    sys.exit()

# 繪製文字的函數，用於顯示按鈕文字與標籤
def draw_text(text, pos, font=FONT, color=(0, 0, 0)):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# 繪製滑桿的函數，用於設定選單的音量調整
def draw_slider(rect, pos, label, label_pos, font=SMALL_FONT):
    pygame.draw.rect(screen, (150, 150, 150), rect, border_radius=5)  # 繪製滑桿背景
    pygame.draw.circle(screen, (50, 100, 150), (int(pos), rect.centery), 10)  # 繪製滑桿圓形指示器
    draw_text(label, label_pos, font, (255, 255, 255))  # 繪製滑桿標籤

# 繪製主畫面，包含背景與按鈕
def draw_main_menu():
    screen.blit(loading_img, (0, 0))  # 顯示主畫面背景圖片
    
    mouse_pos = pygame.mouse.get_pos()  # 獲取滑鼠位置
    # 根據滑鼠懸浮狀態設定按鈕顏色
    start_color = (100, 150, 200) if start_button.collidepoint(mouse_pos) else (50, 100, 150)
    settings_color = (100, 150, 200) if settings_button.collidepoint(mouse_pos) else (50, 100, 150)
    exit_color = (100, 150, 200) if exit_button.collidepoint(mouse_pos) else (50, 100, 150)

    # 繪製按鈕與文字
    pygame.draw.rect(screen, start_color, start_button, border_radius=15)
    draw_text("Start Game", START_BUTTON_TEXT_POS, color=(255, 255, 255))
    pygame.draw.rect(screen, settings_color, settings_button, border_radius=15)
    draw_text("Settings", SETTINGS_BUTTON_TEXT_POS, color=(255, 255, 255))
    pygame.draw.rect(screen, exit_color, exit_button, border_radius=15)
    draw_text("Exit Game", EXIT_BUTTON_TEXT_POS, color=(255, 255, 255))

# 繪製設定選單，包含音量滑桿與返回按鈕
def draw_settings_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # 創建半透明遮罩
    overlay.fill((0, 0, 0, 180))  # 設置遮罩顏色與透明度
    screen.blit(overlay, (0, 0))  # 顯示遮罩
    
    draw_text("Settings", SETTINGS_TITLE_POS, LARGE_FONT, (255, 255, 255))  # 顯示標題
    
    draw_slider(music_slider_rect, music_slider_pos, "Music Volume", MUSIC_SLIDER_LABEL_POS)  # 繪製音樂音量滑桿
    draw_slider(sound_slider_rect, sound_slider_pos, "Sound Volume", SOUND_SLIDER_LABEL_POS)  # 繪製音效音量滑桿
    
    mouse_pos = pygame.mouse.get_pos()  # 獲取滑鼠位置
    main_menu_color = (100, 150, 200) if main_menu_button.collidepoint(mouse_pos) else (50, 100, 150)  # 設定按鈕懸浮顏色
    pygame.draw.rect(screen, main_menu_color, main_menu_button, border_radius=15)  # 繪製返回按鈕
    draw_text("Main Menu", MAIN_MENU_BUTTON_TEXT_POS, color=(255, 255, 255))  # 繪製按鈕文字

# ------------------------------
# 後端 - 邏輯處理
# ------------------------------

# 主畫面迴圈，處理主畫面與設定選單的邏輯
def main_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos, dragging_music_slider, dragging_sound_slider

    in_main_menu = True  # 標記是否在主畫面
    in_settings = False  # 標記是否在設定選單

    while in_main_menu:
        if in_settings:
            draw_settings_menu()  # 顯示設定選單
        else:
            draw_main_menu()  # 顯示主畫面

        for event in pygame.event.get():
            if event.type == QUIT:  # 處理視窗關閉事件
                bye_bye_sound.play()  # 播放退出音效
                pygame.time.delay(int(bye_bye_sound.get_length() * 1000))  # 等待音效播放完成
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:  # 處理滑鼠按下事件
                pos = pygame.mouse.get_pos()
                if in_settings:
                    music_slider_circle = pygame.Rect(music_slider_pos - 10, music_slider_rect.y - 10, 20, 20)
                    sound_slider_circle = pygame.Rect(sound_slider_pos - 10, sound_slider_rect.y - 10, 20, 20)
                    if music_slider_circle.collidepoint(pos):  # 檢查是否點擊音樂滑桿
                        dragging_music_slider = True
                    elif sound_slider_circle.collidepoint(pos):  # 檢查是否點擊音效滑桿
                        dragging_sound_slider = True
                    elif main_menu_button.collidepoint(pos):  # 點擊返回按鈕
                        click_sound.play()
                        in_settings = False
                else:
                    if start_button.collidepoint(pos):  # 點擊開始遊戲按鈕
                        click_sound.play()
                        in_main_menu = False
                        game.main(music_volume, sound_volume)  # 進入遊戲主畫面
                        in_main_menu = True
                    elif settings_button.collidepoint(pos):  # 點擊設定按鈕
                        click_sound.play()
                        in_settings = True
                    elif exit_button.collidepoint(pos):  # 點擊退出按鈕
                        click_sound.play()
                        bye_bye_sound.play()
                        pygame.time.delay(int(bye_bye_sound.get_length() * 1000))
                        pygame.quit()
                        sys.exit()
            elif event.type == MOUSEBUTTONUP:  # 處理滑鼠放開事件
                dragging_music_slider = False
                dragging_sound_slider = False
            elif event.type == MOUSEMOTION and in_settings:  # 處理滑鼠移動事件
                if dragging_music_slider:  # 拖動音樂滑桿
                    new_pos = event.pos[0]
                    new_pos = max(music_slider_rect.x, min(new_pos, music_slider_rect.x + music_slider_rect.width))
                    music_slider_pos = new_pos
                    music_volume = (music_slider_pos - music_slider_rect.x) / music_slider_rect.width
                    pygame.mixer.music.set_volume(music_volume)
                elif dragging_sound_slider:  # 拖動音效滑桿
                    new_pos = event.pos[0]
                    new_pos = max(sound_slider_rect.x, min(new_pos, sound_slider_rect.x + sound_slider_rect.width))
                    sound_slider_pos = new_pos
                    sound_volume = (sound_slider_pos - sound_slider_rect.x) / sound_slider_rect.width
                    click_sound.set_volume(sound_volume)
                    bye_bye_sound.set_volume(sound_volume)

        pygame.display.flip()  # 更新畫面
        clock.tick(FPS)  # 控制幀率

# 程式入口
if __name__ == "__main__":
    main_menu()